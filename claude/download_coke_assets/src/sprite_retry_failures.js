#!/usr/bin/env node
/**
 * Retry failed Sprite uploads with no idle timeout (large PSD/TIF files).
 * Reads sprite_download_failures.json, streams from AEM → S3.
 */
const axios = require("axios");
const { S3Client } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = process.env.AEM_BASE_URL || "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const S3_BUCKET = process.env.S3_BUCKET || "foundry-tccc-enterprise-adobe-assets";
const S3_PREFIX = process.env.S3_PREFIX || "dam_assets_downloaded_by_hs_sprite/orig_assets";
const AWS_REGION = process.env.AWS_REGION || "us-west-2";
const HARD_TIMEOUT_MS = parseInt(process.env.HARD_TIMEOUT_MS || "1800000", 10); // 30 min
const CONCURRENCY = parseInt(process.env.CONCURRENCY || "6", 10);

const s3 = new S3Client({ region: AWS_REGION });
let uploaded = 0, failed = 0;
const stillFailed = [];

async function streamToS3(damPath) {
  const downloadUrl = `${AEM_BASE}${damPath}`;
  const relativePath = damPath.replace("/content/dam/", "");
  const s3Key = `${S3_PREFIX}/${relativePath}`;
  const name = damPath.split("/").pop();
  const start = Date.now();

  const controller = new AbortController();
  const hard = setTimeout(() => controller.abort(), HARD_TIMEOUT_MS);

  try {
    const resp = await axios.get(downloadUrl, {
      headers: { Authorization: `Bearer ${AEM_TOKEN}` },
      responseType: "stream",
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      signal: controller.signal,
      validateStatus: (s) => s >= 200 && s < 300,
    });
    const contentType = resp.headers["content-type"] || "application/octet-stream";
    const contentLength = parseInt(resp.headers["content-length"] || "0", 10);

    const uploader = new Upload({
      client: s3,
      params: { Bucket: S3_BUCKET, Key: s3Key, Body: resp.data, ContentType: contentType },
      queueSize: 4,
      partSize: 25 * 1024 * 1024, // bigger parts for big files
      leavePartsOnError: false,
    });
    await uploader.done();
    uploaded++;
    const sec = ((Date.now() - start) / 1000).toFixed(1);
    const sizeMB = contentLength ? `${(contentLength / 1024 / 1024).toFixed(1)}MB` : "?";
    console.log(`  ✓ [${uploaded + failed}/${TOTAL}] ${name} (${sizeMB}, ${sec}s)`);
  } catch (err) {
    failed++;
    const reason = err.code === "ERR_CANCELED" ? "timeout" : (err.response?.status ? `HTTP ${err.response.status}` : err.message);
    console.error(`  ✗ ${name}: ${reason}`);
    stillFailed.push({ asset: damPath, reason });
  } finally {
    clearTimeout(hard);
  }
}

const failures = JSON.parse(fs.readFileSync(path.join(ROOT, "sprite_download_failures.json"), "utf8"));
const TOTAL = failures.length;

(async () => {
  console.log(`\n🔁 Retrying ${TOTAL} failed uploads (concurrency=${CONCURRENCY}, hard timeout=${HARD_TIMEOUT_MS / 1000}s)\n`);
  let idx = 0;
  await Promise.all(Array.from({ length: CONCURRENCY }, async () => {
    while (idx < TOTAL) {
      const i = idx++;
      await streamToS3(failures[i].asset);
    }
  }));

  console.log(`\n✅ Retry done. Recovered: ${uploaded}, Still failed: ${failed}`);
  if (stillFailed.length > 0) {
    fs.writeFileSync(path.join(ROOT, "sprite_download_failures.json"), JSON.stringify(stillFailed, null, 2));
    console.log(`⚠️  ${stillFailed.length} remain → sprite_download_failures.json (overwritten)`);
  } else {
    fs.unlinkSync(path.join(ROOT, "sprite_download_failures.json"));
    console.log(`✓ Cleared sprite_download_failures.json`);
  }
})();
