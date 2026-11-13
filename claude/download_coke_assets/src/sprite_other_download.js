#!/usr/bin/env node
/**
 * Download non-image Sprite assets (videos, zips, wav, etc.) from AEM to S3.
 * Skips files already present in S3 (idempotent / resumable).
 */
const axios = require("axios");
const { S3Client, HeadObjectCommand } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = process.env.AEM_BASE_URL || "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const S3_BUCKET = process.env.S3_BUCKET || "foundry-tccc-enterprise-adobe-assets";
const S3_PREFIX = process.env.S3_PREFIX || "dam_assets_downloaded_by_hs_sprite/orig_assets";
const AWS_REGION = process.env.AWS_REGION || "us-west-2";
const CONCURRENCY = parseInt(process.env.UPLOAD_CONCURRENCY || "8", 10);
const HARD_TIMEOUT_MS = parseInt(process.env.HARD_TIMEOUT_MS || "3600000", 10); // 60min per file
const IDLE_TIMEOUT_MS = parseInt(process.env.IDLE_TIMEOUT_MS || "120000", 10);  // 2min idle

const s3 = new S3Client({ region: AWS_REGION });

let uploaded = 0, failed = 0, skipped = 0;
const failures = [];
const start = Date.now();

async function existsOnS3(key) {
  try {
    await s3.send(new HeadObjectCommand({ Bucket: S3_BUCKET, Key: key }));
    return true;
  } catch (e) {
    if (e.$metadata?.httpStatusCode === 404 || e.name === "NotFound") return false;
    throw e;
  }
}

async function streamToS3(asset, total) {
  const downloadUrl = `${AEM_BASE}${asset.damPath}`;
  const relativePath = asset.damPath.replace("/content/dam/", "");
  const s3Key = `${S3_PREFIX}/${relativePath}`;

  if (await existsOnS3(s3Key)) {
    skipped++;
    return;
  }

  const ctrl = new AbortController();
  const hard = setTimeout(() => ctrl.abort(), HARD_TIMEOUT_MS);
  const t0 = Date.now();

  try {
    const resp = await axios.get(downloadUrl, {
      headers: { Authorization: `Bearer ${AEM_TOKEN}` },
      responseType: "stream",
      maxContentLength: Infinity, maxBodyLength: Infinity,
      signal: ctrl.signal,
      validateStatus: (s) => s >= 200 && s < 300,
    });
    const ct = resp.headers["content-type"] || "application/octet-stream";
    const cl = parseInt(resp.headers["content-length"] || "0", 10);

    let idle;
    const reset = () => { clearTimeout(idle); idle = setTimeout(() => ctrl.abort(), IDLE_TIMEOUT_MS); };
    resp.data.on("data", reset);
    reset();

    const up = new Upload({
      client: s3,
      params: { Bucket: S3_BUCKET, Key: s3Key, Body: resp.data, ContentType: ct },
      queueSize: 4,
      partSize: 50 * 1024 * 1024, // 50 MB parts for big files
      leavePartsOnError: false,
    });
    await up.done();
    clearTimeout(idle);
    uploaded++;
    const sec = ((Date.now() - t0) / 1000).toFixed(0);
    const mb = cl ? (cl / 1024 / 1024).toFixed(1) : "?";
    if (uploaded % 50 === 0 || uploaded <= 5) {
      const pct = ((uploaded + skipped) / total * 100).toFixed(1);
      const mbps = cl > 0 ? (cl / 1024 / 1024 / Math.max(1, (Date.now() - t0) / 1000)).toFixed(1) : "?";
      console.log(`  ✓ [${uploaded + skipped}/${total} ${pct}%] ${asset.name} (${mb}MB, ${sec}s, ${mbps}MB/s)`);
    }
  } catch (err) {
    failed++;
    const r = err.code === "ERR_CANCELED" ? "timeout/aborted" : (err.response?.status ? `HTTP ${err.response.status}` : err.message);
    if (failed <= 50) console.error(`  ✗ ${asset.name}: ${r}`);
    failures.push({ asset: asset.damPath, reason: r });
  } finally {
    clearTimeout(hard);
  }
}

async function uploadAll(assets) {
  let idx = 0;
  const total = assets.length;
  await Promise.all(Array.from({ length: CONCURRENCY }, async () => {
    while (idx < total) {
      const i = idx++;
      await streamToS3(assets[i], total);
    }
  }));
}

(async () => {
  const items = JSON.parse(fs.readFileSync(path.join(ROOT, "sprite_other_manifest.json"), "utf8"));

  // Sort smaller files first so quick wins land before huge zips
  items.sort((a, b) => (a.size || 0) - (b.size || 0));

  console.log(`\n🚀 AEM → S3: Sprite videos+zips+misc`);
  console.log(`   Target: s3://${S3_BUCKET}/${S3_PREFIX}/`);
  console.log(`   Items: ${items.length}, total: ${(items.reduce((s,a)=>s+(a.size||0),0)/1024/1024/1024).toFixed(1)} GB`);
  console.log(`   Concurrency: ${CONCURRENCY}, hard timeout: ${HARD_TIMEOUT_MS/1000}s, idle: ${IDLE_TIMEOUT_MS/1000}s\n`);

  const ticker = setInterval(() => {
    const m = ((Date.now() - start) / 1000 / 60).toFixed(1);
    const pct = ((uploaded + skipped) / items.length * 100).toFixed(1);
    console.log(`── ${m}m | uploaded=${uploaded} skipped=${skipped} failed=${failed} (${pct}%) ──`);
  }, 60000);

  await uploadAll(items);
  clearInterval(ticker);

  const m = ((Date.now() - start) / 1000 / 60).toFixed(1);
  console.log(`\n${"─".repeat(60)}`);
  console.log(`✅ Done in ${m} min. Uploaded=${uploaded}, Skipped=${skipped}, Failed=${failed}`);

  if (failures.length > 0) {
    fs.writeFileSync(path.join(ROOT, "sprite_other_failures.json"), JSON.stringify(failures, null, 2));
    console.log(`⚠️  ${failures.length} failures → sprite_other_failures.json`);
  }
  process.exit(failures.length > 0 ? 2 : 0);
})().catch(e => { console.error("Fatal:", e); process.exit(1); });
