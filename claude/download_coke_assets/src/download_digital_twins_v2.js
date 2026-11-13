#!/usr/bin/env node
/**
 * Download ALL digital-twin assets from TCCC DAM to S3.
 * v2: Higher concurrency, better progress, sorted by extension (PNGs first).
 *
 * Usage:
 *   node src/download_digital_twins_v2.js              # Full download
 *   node src/download_digital_twins_v2.js --png-only    # PNGs only
 *   node src/download_digital_twins_v2.js --zip-only    # ZIPs only
 *   node src/download_digital_twins_v2.js --pdf-only    # PDFs only
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

const CONCURRENCY = 25;
const DOWNLOAD_TIMEOUT = 300000; // 5 min per file

const s3 = new S3Client({ region: AWS_REGION });
const headers = { Authorization: `Bearer ${AEM_TOKEN}` };

let uploaded = 0, failed = 0;
const failures = [];
const startTime = Date.now();

function getS3Key(damPath) {
  return `${S3_PREFIX}/${damPath.replace("/content/dam/tccc/digital-twin/", "")}`;
}

async function streamToS3(damPath, total) {
  const name = damPath.split("/").pop();
  const s3Key = getS3Key(damPath);

  try {
    const resp = await axios.get(`${AEM_BASE}${damPath}`, {
      headers,
      responseType: "stream",
      maxContentLength: Infinity,
      timeout: DOWNLOAD_TIMEOUT,
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

    if (uploaded % 100 === 0 || uploaded <= 3) {
      const pct = (uploaded / total * 100).toFixed(1);
      const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
      const rate = (uploaded / (Date.now() - startTime) * 60000).toFixed(0);
      const sizeMB = contentLength ? `${(contentLength / 1024 / 1024).toFixed(1)}MB` : "?";
      console.log(`  ✓ [${uploaded}/${total} ${pct}%] ${name} (${sizeMB}) | ${elapsed}m | ~${rate}/min`);
    }
  } catch (err) {
    failed++;
    const reason = err.response?.status ? `HTTP ${err.response.status}` : err.message;
    if (failed <= 50) console.error(`  ✗ ${name}: ${reason}`);
    failures.push({ path: damPath, reason });
  }
}

async function main() {
  const manifestPath = path.join(ROOT, "digital_twin_manifest.json");
  if (!fs.existsSync(manifestPath)) {
    console.error("Run download_digital_twins.js --crawl-only first to build manifest");
    process.exit(1);
  }

  let allPaths = JSON.parse(fs.readFileSync(manifestPath, "utf8"));

  // Filter by extension if requested
  const pngOnly = process.argv.includes("--png-only");
  const zipOnly = process.argv.includes("--zip-only");
  const pdfOnly = process.argv.includes("--pdf-only");

  if (pngOnly) allPaths = allPaths.filter(p => p.endsWith(".png"));
  else if (zipOnly) allPaths = allPaths.filter(p => p.endsWith(".zip"));
  else if (pdfOnly) allPaths = allPaths.filter(p => p.endsWith(".pdf"));

  // Sort: PNGs first (small), then PDFs, then ZIPs (potentially large)
  allPaths.sort((a, b) => {
    const extOrder = { png: 0, jpg: 0, webp: 0, pdf: 1, zip: 2 };
    const ea = extOrder[a.split('.').pop().toLowerCase()] ?? 1;
    const eb = extOrder[b.split('.').pop().toLowerCase()] ?? 1;
    return ea - eb;
  });

  const total = allPaths.length;
  const exts = {};
  allPaths.forEach(p => {
    const ext = p.split('.').pop().toLowerCase();
    exts[ext] = (exts[ext] || 0) + 1;
  });

  console.log(`\n🔽 Digital Twin Download v2`);
  console.log(`   Assets: ${total}`);
  console.log(`   Types: ${JSON.stringify(exts)}`);
  console.log(`   Concurrency: ${CONCURRENCY}`);
  console.log(`   Target: s3://${S3_BUCKET}/${S3_PREFIX}/\n`);

  // Worker pool
  let idx = 0;
  const ticker = setInterval(() => {
    const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
    const pct = (uploaded / total * 100).toFixed(1);
    const rate = (uploaded / (Date.now() - startTime) * 60000).toFixed(0);
    const eta = uploaded > 0 ? (((total - uploaded) / (uploaded / (Date.now() - startTime))) / 60000).toFixed(0) : "?";
    console.log(`── ${elapsed}m | ${uploaded}/${total} (${pct}%) | ${failed} failed | ~${rate}/min | ETA ~${eta}m ──`);
  }, 30000);

  const workers = Array.from({ length: CONCURRENCY }, async () => {
    while (idx < total) {
      const i = idx++;
      await streamToS3(allPaths[i], total);
    }
  });
  await Promise.all(workers);
  clearInterval(ticker);

  const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
  console.log(`\n${"─".repeat(60)}`);
  console.log(`✅ Done in ${elapsed} min.`);
  console.log(`   Uploaded: ${uploaded}  |  Failed: ${failed}`);

  if (failures.length > 0) {
    const failPath = path.join(ROOT, "digital_twin_failures.json");
    fs.writeFileSync(failPath, JSON.stringify(failures, null, 2));
    console.log(`⚠️  ${failures.length} failures → digital_twin_failures.json`);
  }

  process.exit(failures.length > 0 ? 2 : 0);
}

main().catch(err => {
  console.error("Fatal:", err);
  process.exit(1);
});
