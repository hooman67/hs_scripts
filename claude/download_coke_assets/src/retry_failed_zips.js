#!/usr/bin/env node
/**
 * Retry failed ZIP downloads from digital_twin_failures.json.
 * Lower concurrency to avoid overwhelming AEM/DNS.
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

const CONCURRENCY = 3; // Very gentle — AEM drops connections at higher concurrency
const DOWNLOAD_TIMEOUT = 600000; // 10 min per file for large ZIPs

const s3 = new S3Client({ region: AWS_REGION });
const headers = { Authorization: `Bearer ${AEM_TOKEN}` };

let uploaded = 0, failed = 0;
const newFailures = [];
const startTime = Date.now();

function getS3Key(damPath) {
  return `${S3_PREFIX}/${damPath.replace("/content/dam/tccc/digital-twin/", "")}`;
}

async function streamToS3(damPath, total, attempt = 1) {
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
      const rate = (uploaded / (Date.now() - startTime) * 60000).toFixed(1);
      const sizeMB = contentLength ? `${(contentLength / 1024 / 1024).toFixed(1)}MB` : "?";
      console.log(`  ✓ [${uploaded}/${total} ${pct}%] ${name} (${sizeMB}) | ${elapsed}m | ~${rate}/min`);
    }
  } catch (err) {
    const reason = err.response?.status ? `HTTP ${err.response.status}` : (err.code || err.message);
    // Retry once on DNS/network errors
    if (attempt === 1 && (reason.includes('ENOTFOUND') || reason.includes('ECONNRESET') || reason.includes('EADDRNOTAVAIL'))) {
      await new Promise(r => setTimeout(r, 2000)); // brief pause
      return streamToS3(damPath, total, 2);
    }
    failed++;
    if (failed <= 50) console.error(`  ✗ ${name}: ${reason}`);
    newFailures.push({ path: damPath, reason });
  }
}

async function main() {
  const failPath = path.join(ROOT, "digital_twin_failures.json");
  if (!fs.existsSync(failPath)) {
    console.error("No failures file found");
    process.exit(1);
  }

  const failures = JSON.parse(fs.readFileSync(failPath, "utf8"));
  // Only retry ZIP failures
  const zipFailures = failures.filter(f => f.path.endsWith(".zip"));
  const total = zipFailures.length;

  console.log(`\n🔄 Retrying ${total} failed ZIP downloads`);
  console.log(`   Concurrency: ${CONCURRENCY}`);
  console.log(`   Timeout: ${DOWNLOAD_TIMEOUT / 1000}s per file\n`);

  let idx = 0;
  const ticker = setInterval(() => {
    const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
    const pct = ((uploaded + failed) / total * 100).toFixed(1);
    const rate = uploaded > 0 ? (uploaded / (Date.now() - startTime) * 60000).toFixed(1) : "0";
    console.log(`── ${elapsed}m | ${uploaded} ok / ${failed} fail (${pct}% processed) | ~${rate}/min ──`);
  }, 60000);

  const workers = Array.from({ length: CONCURRENCY }, async () => {
    while (idx < total) {
      const i = idx++;
      await streamToS3(zipFailures[i].path, total);
    }
  });
  await Promise.all(workers);
  clearInterval(ticker);

  const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
  console.log(`\n${"─".repeat(60)}`);
  console.log(`✅ Retry done in ${elapsed} min.`);
  console.log(`   Uploaded: ${uploaded}  |  Failed: ${failed}`);
  console.log(`   Total ZIPs on S3: ${577 + uploaded} / 9482`);

  if (newFailures.length > 0) {
    const retryFailPath = path.join(ROOT, "digital_twin_retry_failures.json");
    fs.writeFileSync(retryFailPath, JSON.stringify(newFailures, null, 2));
    console.log(`⚠️  ${newFailures.length} still failing → digital_twin_retry_failures.json`);
  }

  process.exit(newFailures.length > 0 ? 2 : 0);
}

main().catch(err => {
  console.error("Fatal:", err);
  process.exit(1);
});
