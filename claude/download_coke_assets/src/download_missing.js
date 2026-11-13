#!/usr/bin/env node
/**
 * Download all missing digital-twin files from digital_twin_missing.json.
 * Small files (png/pdf/jpg) first at concurrency 10, then ZIPs at concurrency 3.
 */

const axios = require("axios");
const { S3Client } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();

const S3_BUCKET = "foundry-tccc-enterprise-adobe-assets";
const S3_PREFIX = "digital_twins_from_dam";
const AWS_REGION = "us-west-2";

const s3 = new S3Client({ region: AWS_REGION });
const headers = { Authorization: `Bearer ${AEM_TOKEN}` };

let uploaded = 0, failed = 0;
const failures = [];

function getS3Key(damPath) {
  return `${S3_PREFIX}/${damPath.replace("/content/dam/tccc/digital-twin/", "")}`;
}

async function streamToS3(damPath, total, startTime, attempt = 1) {
  const name = damPath.split("/").pop();
  const s3Key = getS3Key(damPath);

  try {
    const resp = await axios.get(`${AEM_BASE}${damPath}`, {
      headers,
      responseType: "stream",
      maxContentLength: Infinity,
      timeout: 600000,
      validateStatus: (s) => s >= 200 && s < 300,
    });

    const contentType = resp.headers["content-type"] || "application/octet-stream";
    const contentLength = parseInt(resp.headers["content-length"] || "0", 10);

    const uploader = new Upload({
      client: s3,
      params: { Bucket: S3_BUCKET, Key: s3Key, Body: resp.data, ContentType: contentType },
      queueSize: 4,
      partSize: 10 * 1024 * 1024,
      leavePartsOnError: false,
    });

    await uploader.done();
    uploaded++;

    if (uploaded % 50 === 0 || uploaded <= 3) {
      const pct = (uploaded / total * 100).toFixed(1);
      const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
      const rate = (uploaded / (Date.now() - startTime) * 60000).toFixed(1);
      const sizeMB = contentLength ? `${(contentLength / 1024 / 1024).toFixed(1)}MB` : "?";
      console.log(`  ✓ [${uploaded}/${total} ${pct}%] ${name} (${sizeMB}) | ${elapsed}m | ~${rate}/min`);
    }
  } catch (err) {
    const reason = err.response?.status ? `HTTP ${err.response.status}` : (err.code || err.message);
    if (attempt <= 2 && (reason.includes('ENOTFOUND') || reason.includes('ECONNRESET') || reason.includes('EPIPE') || reason.includes('EADDRNOTAVAIL'))) {
      await new Promise(r => setTimeout(r, 3000));
      return streamToS3(damPath, total, startTime, attempt + 1);
    }
    failed++;
    if (failed <= 30) console.error(`  ✗ ${name}: ${reason}`);
    failures.push({ path: damPath, reason });
  }
}

async function runBatch(paths, concurrency, label) {
  const total = paths.length;
  if (total === 0) return;

  uploaded = 0; failed = 0;
  const startTime = Date.now();

  console.log(`\n── ${label}: ${total} files, concurrency ${concurrency} ──\n`);

  let idx = 0;
  const ticker = setInterval(() => {
    const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
    const pct = ((uploaded + failed) / total * 100).toFixed(1);
    const rate = uploaded > 0 ? (uploaded / (Date.now() - startTime) * 60000).toFixed(1) : "0";
    const eta = uploaded > 0 ? (((total - uploaded - failed) / (uploaded / (Date.now() - startTime))) / 60000).toFixed(0) : "?";
    console.log(`── ${elapsed}m | ${uploaded} ok / ${failed} fail of ${total} (${pct}%) | ~${rate}/min | ETA ~${eta}m ──`);
  }, 60000);

  const workers = Array.from({ length: concurrency }, async () => {
    while (idx < total) {
      const i = idx++;
      await streamToS3(paths[i], total, startTime);
    }
  });
  await Promise.all(workers);
  clearInterval(ticker);

  const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
  console.log(`\n  ${label} done in ${elapsed}m: ${uploaded} ok, ${failed} failed\n`);
}

async function main() {
  const missingPath = path.join(ROOT, "digital_twin_missing.json");
  const allMissing = JSON.parse(fs.readFileSync(missingPath, "utf8"));

  const small = allMissing.filter(p => !p.endsWith(".zip"));
  const zips = allMissing.filter(p => p.endsWith(".zip"));

  console.log(`\n🔄 Downloading ${allMissing.length} missing files`);
  console.log(`   Small files (png/pdf/jpg/webp): ${small.length}`);
  console.log(`   ZIP files (USD 3D models): ${zips.length}`);

  // Phase 1: Small files at higher concurrency
  await runBatch(small, 10, "Small files");

  // Phase 2: ZIPs at low concurrency
  await runBatch(zips, 3, "ZIP files");

  console.log(`\n${"─".repeat(60)}`);
  console.log(`✅ All done.`);

  if (failures.length > 0) {
    const failPath = path.join(ROOT, "digital_twin_still_missing.json");
    fs.writeFileSync(failPath, JSON.stringify(failures, null, 2));
    console.log(`⚠️  ${failures.length} still failing → digital_twin_still_missing.json`);
  }

  process.exit(failures.length > 0 ? 2 : 0);
}

main().catch(err => {
  console.error("Fatal:", err);
  process.exit(1);
});
