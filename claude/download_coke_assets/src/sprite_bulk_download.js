#!/usr/bin/env node
/**
 * AEM → S3: Download Sprite product + marketing images.
 * Roots come from sprite_discovery.json (built by discover_sprite.js).
 *
 * Phase 1: Crawl all folders, collect image asset paths + sizes.
 * Phase 2: Upload all images to S3 with concurrency pool.
 *
 * Output:
 *   sprite_image_manifest.json   — flat list of {damPath, name, size}
 *   sprite_path_summary.json     — per-root summary {path, count, totalBytes}
 *
 * Usage:
 *   node src/sprite_bulk_download.js                # crawl + upload
 *   node src/sprite_bulk_download.js --crawl-only   # just build manifest, no upload
 *   node src/sprite_bulk_download.js --skip-crawl   # use cached manifest, upload only
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

const API_PAGE_SIZE = 200;
const LIST_TIMEOUT_MS = parseInt(process.env.LIST_TIMEOUT_MS || "20000", 10);
const UPLOAD_CONCURRENCY = parseInt(process.env.UPLOAD_CONCURRENCY || "15", 10);

const IMAGE_EXTENSIONS = new Set([
  ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".gif", ".webp",
  ".bmp", ".svg", ".psd", ".ai", ".eps", ".heic", ".heif",
]);

// Load discovered roots
const discovery = JSON.parse(fs.readFileSync(path.join(ROOT, "sprite_discovery.json"), "utf8"));
const ROOTS = [
  ...discovery.sprite_brand_paths,
  // Marketing top-level Sprite subtrees
  "/content/dam/tccc/marketing/sprite",
  "/content/dam/tccc/marketing/sprite-zero-diet-light",
  "/content/dam/tccc/marketing/absolut-vodka---sprite",
];

const s3 = new S3Client({ region: AWS_REGION });
let uploaded = 0, failed = 0, skippedNonImage = 0, crawledFolders = 0;
const failures = [];
const startTime = Date.now();
const perRootStats = {}; // root -> {count, bytes}

function isImage(filename) {
  const ext = "." + filename.split(".").pop().toLowerCase();
  return IMAGE_EXTENSIONS.has(ext);
}

function rootOf(damPath) {
  // Map an asset path back to one of the seed roots (longest prefix)
  let best = null;
  for (const r of ROOTS) {
    if (damPath.startsWith(r + "/") && (!best || r.length > best.length)) best = r;
  }
  return best || "(unknown)";
}

async function listFolder(damPath) {
  const apiBase = `/api/assets${damPath.replace("/content/dam/", "/")}.json`;
  let offset = 0;
  const folders = [];
  const assets = [];

  while (true) {
    const url = `${AEM_BASE}${apiBase}?limit=${API_PAGE_SIZE}&offset=${offset}`;
    let data;
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), LIST_TIMEOUT_MS);
      const resp = await axios.get(url, {
        headers: { Authorization: `Bearer ${AEM_TOKEN}` },
        timeout: LIST_TIMEOUT_MS,
        signal: controller.signal,
      });
      clearTimeout(timer);
      data = resp.data;
    } catch (err) {
      if (err.response?.status === 404) break;
      const msg = err.code === "ERR_CANCELED" ? "timeout" : err.message;
      console.error(`  ✗ list ${damPath}: ${msg}`);
      break;
    }

    const entities = data.entities || [];
    if (entities.length === 0) break;

    for (const entity of entities) {
      const cls = (entity.class || [])[0] || "";
      const name = entity.properties?.name;
      if (!name) continue;
      if (cls === "assets/folder") {
        const lower = name.toLowerCase();
        if (["none", "no", "null", "n-a"].includes(lower)) continue;
        folders.push(`${damPath}/${name}`);
      } else if (cls === "assets/asset") {
        if (isImage(name)) {
          // size: try to read jcr:content/jcr:data length or asset size from metadata
          const props = entity.properties || {};
          const meta = props.metadata || {};
          const size =
            props["jcr:content"]?.["jcr:data"]?.length ||
            meta["dam:size"] ||
            props.size ||
            0;
          assets.push({ damPath: `${damPath}/${name}`, name, size });
        } else {
          skippedNonImage++;
        }
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
  const folderQueue = [...ROOTS];
  let activeWorkers = 0;
  let resolveAll;
  const donePromise = new Promise(r => { resolveAll = r; });

  const CRAWL_WORKERS = 10;

  async function worker() {
    while (true) {
      const p = folderQueue.shift();
      if (!p) break;
      activeWorkers++;
      const { folders, assets } = await listFolder(p);
      allAssets.push(...assets);
      folderQueue.push(...folders);
      if (crawledFolders % 200 === 0) {
        console.log(`   crawl: ${crawledFolders} folders | ${allAssets.length} images | ${folderQueue.length} remaining`);
      }
      activeWorkers--;
    }
  }

  const interval = setInterval(() => {
    if (folderQueue.length === 0 && activeWorkers === 0) {
      clearInterval(interval);
      resolveAll();
      return;
    }
    while (folderQueue.length > 0 && activeWorkers < CRAWL_WORKERS) worker();
  }, 100);

  for (let i = 0; i < Math.min(CRAWL_WORKERS, folderQueue.length); i++) worker();

  await donePromise;
  return allAssets;
}

async function streamToS3(asset) {
  const downloadUrl = `${AEM_BASE}${asset.damPath}`;
  const relativePath = asset.damPath.replace("/content/dam/", "");
  const s3Key = `${S3_PREFIX}/${relativePath}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 180000);

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

    let idleTimer;
    const resetIdle = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => controller.abort(), 30000);
    };
    resp.data.on("data", resetIdle);
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
    const reason = err.code === "ERR_CANCELED" ? "timeout/aborted" : (err.response?.status ? `HTTP ${err.response.status}` : err.message);
    if (failed <= 50) console.error(`  ✗ ${asset.name}: ${reason}`);
    failures.push({ asset: asset.damPath, reason });
  } finally {
    clearTimeout(timer);
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

function summarize(assets) {
  const byRoot = {};
  for (const a of assets) {
    const r = rootOf(a.damPath);
    if (!byRoot[r]) byRoot[r] = { count: 0, bytes: 0, byExt: {} };
    byRoot[r].count++;
    byRoot[r].bytes += a.size || 0;
    const ext = a.name.split(".").pop().toLowerCase();
    byRoot[r].byExt[ext] = (byRoot[r].byExt[ext] || 0) + 1;
  }
  return byRoot;
}

async function main() {
  console.log(`\n🔍 AEM → S3: SPRITE Images`);
  console.log(`   Target: s3://${S3_BUCKET}/${S3_PREFIX}/`);
  console.log(`   Seed roots: ${ROOTS.length}`);
  console.log(`   Upload concurrency: ${UPLOAD_CONCURRENCY}\n`);

  const manifestPath = path.join(ROOT, "sprite_image_manifest.json");
  const summaryPath = path.join(ROOT, "sprite_path_summary.json");

  let assets;
  if (fs.existsSync(manifestPath) && process.argv.includes("--skip-crawl")) {
    assets = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    console.log(`── Loaded ${assets.length} images from existing manifest (--skip-crawl) ──\n`);
  } else {
    console.log(`── Phase 1: Crawling folder tree ──`);
    assets = await crawlAll();
    const crawlTime = ((Date.now() - startTime) / 1000).toFixed(0);
    console.log(`\n📦 Crawl done in ${crawlTime}s: ${crawledFolders} folders | ${assets.length} images | ${skippedNonImage} non-images skipped\n`);
    fs.writeFileSync(manifestPath, JSON.stringify(assets, null, 2));
    console.log(`   Manifest saved → sprite_image_manifest.json`);
  }

  // Summary
  const summary = summarize(assets);
  fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
  const totalBytes = Object.values(summary).reduce((s, r) => s + r.bytes, 0);
  console.log(`\n📊 Per-root summary (saved to sprite_path_summary.json)`);
  console.log(`   Total: ${assets.length} images, ${(totalBytes / 1024 / 1024 / 1024).toFixed(2)} GB`);
  for (const [r, s] of Object.entries(summary).sort((a, b) => b[1].count - a[1].count).slice(0, 25)) {
    console.log(`   ${s.count.toString().padStart(6)} | ${(s.bytes / 1024 / 1024).toFixed(1).padStart(8)} MB | ${r}`);
  }

  if (process.argv.includes("--crawl-only")) {
    console.log("\n⏸  --crawl-only set, skipping upload.");
    return;
  }

  if (assets.length === 0) {
    console.log("No images found. Exiting.");
    return;
  }

  console.log(`\n── Phase 2: Uploading ${assets.length} images (concurrency=${UPLOAD_CONCURRENCY}) ──\n`);
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
  console.log(`   Uploaded: ${uploaded}  |  Failed: ${failed}  |  Non-images skipped: ${skippedNonImage}`);
  console.log(`   Folders crawled: ${crawledFolders}`);

  if (failures.length > 0) {
    const failPath = path.join(ROOT, "sprite_download_failures.json");
    fs.writeFileSync(failPath, JSON.stringify(failures, null, 2));
    console.log(`⚠️  ${failures.length} failures → sprite_download_failures.json`);
  }

  process.exit(failures.length > 0 ? 2 : 0);
}

main().catch(err => { console.error("Fatal:", err); process.exit(1); });
