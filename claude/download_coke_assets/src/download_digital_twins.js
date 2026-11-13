#!/usr/bin/env node
/**
 * Crawl and download ALL digital-twin assets from the TCCC DAM to S3.
 * Structure: /content/dam/tccc/digital-twin/{country}/{brand}/{sub-brand}/{sku}/{files}
 *
 * Phase 1: Crawl entire tree, build manifest
 * Phase 2: Stream assets from AEM → S3
 *
 * Usage:
 *   node src/download_digital_twins.js              # Full crawl + download
 *   node src/download_digital_twins.js --skip-crawl  # Use cached manifest
 *   node src/download_digital_twins.js --crawl-only   # Crawl only, no download
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

const DAM_ROOT = "/content/dam/tccc/digital-twin";
const API_PAGE_SIZE = 200;
const CRAWL_CONCURRENCY = 8;
const UPLOAD_CONCURRENCY = 12;
const LIST_TIMEOUT_MS = 20000;

const s3 = new S3Client({ region: AWS_REGION });
const headers = { Authorization: `Bearer ${AEM_TOKEN}` };

let crawledFolders = 0;
let uploaded = 0, failed = 0, skipped = 0;
const failures = [];
const startTime = Date.now();

// ── PHASE 1: Crawl ────────────────────────────────────────────────────────

async function listFolder(damPath) {
  const apiBase = `/api/assets${damPath.replace("/content/dam/", "/")}.json`;
  let offset = 0;
  const folders = [];
  const assets = [];

  while (true) {
    const url = `${AEM_BASE}${apiBase}?limit=${API_PAGE_SIZE}&offset=${offset}`;
    let data;
    try {
      const resp = await axios.get(url, { headers, timeout: LIST_TIMEOUT_MS });
      data = resp.data;
    } catch (err) {
      if (err.response?.status === 404) break;
      // Retry once on timeout
      if (err.code === 'ECONNABORTED' || err.code === 'ERR_CANCELED') {
        try {
          const resp = await axios.get(url, { headers, timeout: LIST_TIMEOUT_MS * 2 });
          data = resp.data;
        } catch {
          break;
        }
      } else {
        break;
      }
    }

    const entities = data.entities || [];
    if (entities.length === 0) break;

    for (const entity of entities) {
      const cls = (entity.class || [])[0] || "";
      const name = entity.properties?.name;
      if (!name) continue;
      if (cls === "assets/folder") {
        folders.push(`${damPath}/${name}`);
      } else if (cls === "assets/asset") {
        assets.push({ damPath: `${damPath}/${name}`, name });
      }
    }

    const paging = data.properties?.srn?.paging || data.properties?.["srn:paging"];
    if (!paging) break;
    offset += entities.length;
    if (offset >= (paging.total || 0)) break;
  }

  crawledFolders++;
  return { folders, assets };
}

async function crawlAll() {
  const allAssets = [];
  const folderQueue = [DAM_ROOT];
  let activeWorkers = 0;
  let resolveAll;
  const donePromise = new Promise(r => { resolveAll = r; });

  async function worker() {
    while (true) {
      const p = folderQueue.shift();
      if (!p) break;
      activeWorkers++;
      const { folders, assets } = await listFolder(p);
      allAssets.push(...assets);
      folderQueue.push(...folders);
      activeWorkers--;
    }
  }

  const interval = setInterval(() => {
    if (folderQueue.length === 0 && activeWorkers === 0) {
      clearInterval(interval);
      resolveAll();
      return;
    }
    // Status update every tick
    if (crawledFolders % 500 === 0 && crawledFolders > 0) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);
      console.log(`   crawl: ${crawledFolders} folders | ${allAssets.length} assets | ${folderQueue.length} queued | ${elapsed}s`);
    }
    while (folderQueue.length > 0 && activeWorkers < CRAWL_CONCURRENCY) {
      worker();
    }
  }, 100);

  // Seed workers
  for (let i = 0; i < Math.min(CRAWL_CONCURRENCY, folderQueue.length); i++) {
    worker();
  }

  // Also print status regularly
  const statusInterval = setInterval(() => {
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);
    console.log(`   crawl: ${crawledFolders} folders | ${allAssets.length} assets | ${folderQueue.length} queued | ${elapsed}s`);
  }, 15000);

  await donePromise;
  clearInterval(statusInterval);
  return allAssets;
}

// ── PHASE 2: Upload ───────────────────────────────────────────────────────

function getS3Key(damPath) {
  // /content/dam/tccc/digital-twin/us/coca-cola/... → digital_twins_from_dam/us/coca-cola/...
  const relative = damPath.replace("/content/dam/tccc/digital-twin/", "");
  return `${S3_PREFIX}/${relative}`;
}

async function streamToS3(asset) {
  const downloadUrl = `${AEM_BASE}${asset.damPath}`;
  const s3Key = getS3Key(asset.damPath);

  try {
    const resp = await axios.get(downloadUrl, {
      headers,
      responseType: "stream",
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      timeout: 180000,
      validateStatus: (s) => s >= 200 && s < 300,
    });

    const contentType = resp.headers["content-type"] || "application/octet-stream";
    const contentLength = parseInt(resp.headers["content-length"] || "0", 10);

    // Idle timeout
    let idleTimer;
    const controller = new AbortController();
    const resetIdle = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        resp.data.destroy();
      }, 30000);
    };
    resp.data.on('data', resetIdle);
    resetIdle();

    const uploader = new Upload({
      client: s3,
      params: { Bucket: S3_BUCKET, Key: s3Key, Body: resp.data, ContentType: contentType },
      queueSize: 4,
      partSize: 10 * 1024 * 1024,
      leavePartsOnError: false,
    });

    await uploader.done();
    clearTimeout(idleTimer);
    uploaded++;

    if (uploaded % 200 === 0 || uploaded <= 5) {
      const pct = (uploaded / asset._total * 100).toFixed(1);
      const sizeMB = contentLength ? ` (${(contentLength / 1024 / 1024).toFixed(1)}MB)` : "";
      console.log(`  ✓ [${uploaded}/${asset._total} ${pct}%] ${asset.name}${sizeMB}`);
    }
  } catch (err) {
    failed++;
    const reason = err.response?.status ? `HTTP ${err.response.status}` : err.message;
    if (failed <= 100) console.error(`  ✗ ${asset.name}: ${reason}`);
    failures.push({ asset: asset.damPath, reason });
  }
}

async function uploadAll(assets) {
  let idx = 0;
  const total = assets.length;
  assets.forEach(a => a._total = total);

  const workers = Array.from({ length: UPLOAD_CONCURRENCY }, async () => {
    while (idx < total) {
      const i = idx++;
      await streamToS3(assets[i]);
    }
  });
  await Promise.all(workers);
}

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const skipCrawl = process.argv.includes("--skip-crawl");
  const crawlOnly = process.argv.includes("--crawl-only");
  const manifestPath = path.join(ROOT, "digital_twin_manifest.json");

  console.log(`\n🔍 Digital Twin Download: AEM → S3`);
  console.log(`   Source: ${AEM_BASE}${DAM_ROOT}`);
  console.log(`   Target: s3://${S3_BUCKET}/${S3_PREFIX}/`);
  console.log(`   Crawl concurrency: ${CRAWL_CONCURRENCY}`);
  console.log(`   Upload concurrency: ${UPLOAD_CONCURRENCY}\n`);

  let assets;
  if (skipCrawl && fs.existsSync(manifestPath)) {
    const paths = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    assets = paths.map(p => ({ damPath: p, name: p.split("/").pop() }));
    console.log(`── Loaded ${assets.length} assets from cached manifest ──\n`);
  } else {
    console.log(`── Phase 1: Crawling digital-twin folder tree ──`);
    assets = await crawlAll();
    const crawlTime = ((Date.now() - startTime) / 1000).toFixed(0);
    console.log(`\n📦 Crawl done in ${crawlTime}s: ${crawledFolders} folders, ${assets.length} assets\n`);

    // Save manifest
    fs.writeFileSync(manifestPath, JSON.stringify(assets.map(a => a.damPath), null, 2));
    console.log(`   Manifest saved (${assets.length} assets)`);

    // Stats
    const exts = {};
    assets.forEach(a => {
      const ext = a.name.split('.').pop().toLowerCase();
      exts[ext] = (exts[ext] || 0) + 1;
    });
    console.log(`   File types: ${JSON.stringify(exts)}`);
  }

  if (assets.length === 0) {
    console.log("No assets found. Exiting.");
    return;
  }

  if (crawlOnly) {
    console.log("\n   --crawl-only: skipping download.");
    return;
  }

  // Phase 2: Upload
  console.log(`\n── Phase 2: Uploading ${assets.length} assets (concurrency=${UPLOAD_CONCURRENCY}) ──\n`);

  const ticker = setInterval(() => {
    const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
    const pct = (uploaded / assets.length * 100).toFixed(1);
    console.log(`── ${elapsed}m | ${uploaded}/${assets.length} uploaded (${pct}%) | ${failed} failed ──`);
  }, 30000);

  await uploadAll(assets);
  clearInterval(ticker);

  const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
  console.log(`\n${"─".repeat(60)}`);
  console.log(`✅ Done in ${elapsed} min.`);
  console.log(`   Uploaded: ${uploaded}  |  Failed: ${failed}`);
  console.log(`   Folders crawled: ${crawledFolders}`);

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
