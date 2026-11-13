#!/usr/bin/env node
/**
 * AEM → S3: Download Coca-Cola bottle/can images + soccer 2026 images.
 * Phase 1: Crawl all folders, collect image asset paths.
 * Phase 2: Upload all images to S3 with concurrency pool.
 */

const axios = require("axios");
const { S3Client } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");
const fs = require("fs");

// ── Config ──────────────────────────────────────────────────────────────────
const AEM_BASE = "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync("./bearer_token.txt", "utf8").trim();

const S3_BUCKET = "foundry-tccc-enterprise-adobe-assets";
const S3_PREFIX = "dam_assets_downloaded_by_hs";
const AWS_REGION = "us-west-2";

const API_PAGE_SIZE = 200;
const LIST_TIMEOUT_MS = 15000;
const UPLOAD_CONCURRENCY = 15;

const IMAGE_EXTENSIONS = new Set([
  '.jpg', '.jpeg', '.png', '.tiff', '.tif', '.gif', '.webp',
  '.bmp', '.svg', '.psd', '.ai', '.eps', '.heic', '.heif'
]);

// Countries with products in the DAM
const PRODUCT_COUNTRIES = [
  "ad","af","all-countries","ao","au","base","bd","be","br","ca","cz","dz",
  "eg","fr","gb","hk","id","in","it","ke","lx","ma","mx","ng","nl","nz",
  "sk","th","us","uz","za"
];
const COCA_COLA_BRANDS = [
  "coca-cola","coca-cola-energy","coca-cola-functional",
  "coca-cola-light-diet-coke","coca-cola-reduced-sugar","coca-cola-zero",
];
const PRODUCT_ROOTS = PRODUCT_COUNTRIES.flatMap(c =>
  COCA_COLA_BRANDS.map(b => `/content/dam/tccc/products/${c}/${b}`)
);

const ROOTS = [
  ...PRODUCT_ROOTS,
  "/content/dam/tccc/marketing/coca-cola/coca-cola-alwaysonsoccer-na-2026",
  "/content/dam/tccc/marketing/coca-cola/coca-cola-alwaysonsoccerroadtofifa-2025",
  "/content/dam/tccc/marketing/coca-cola/cocacola-fifa-worldcup2026",
  "/content/dam/tccc/marketing/coca-cola/coca-cola-real-magic-uplift-fifa-experiential-trophytour-2026",
  "/content/dam/tccc/marketing/coca-cola/fifa-club-world-cup-2025",
  "/content/dam/tccc/marketing/coca-cola/football-always-on",
  "/content/dam/tccc/marketing/coca-cola/football-always-on-2023",
];

// ── State ──────────────────────────────────────────────────────────────────
const s3 = new S3Client({ region: AWS_REGION });
let uploaded = 0, failed = 0, skippedNonImage = 0, crawledFolders = 0;
const failures = [];
const startTime = Date.now();

function isImage(filename) {
  const ext = '.' + filename.split('.').pop().toLowerCase();
  return IMAGE_EXTENSIONS.has(ext);
}

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
      if (err.response?.status === 404) break; // folder doesn't exist, skip silently
      const msg = err.code === 'ERR_CANCELED' ? 'timeout' : err.message;
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
        if (["none","no","null","n-a"].includes(lower)) continue;
        folders.push(`${damPath}/${name}`);
      } else if (cls === "assets/asset") {
        if (isImage(name)) {
          assets.push({ damPath: `${damPath}/${name}`, name });
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

/** Crawl with independent workers pulling from shared queue */
async function crawlAll() {
  const allAssets = [];
  const folderQueue = [...ROOTS];
  let activeWorkers = 0;
  let resolveAll;
  const donePromise = new Promise(r => { resolveAll = r; });

  const CRAWL_WORKERS = 10;

  async function worker() {
    while (true) {
      const path = folderQueue.shift();
      if (!path) break;
      activeWorkers++;

      const { folders, assets } = await listFolder(path);
      allAssets.push(...assets);
      folderQueue.push(...folders);

      if (crawledFolders % 200 === 0) {
        console.log(`   crawl: ${crawledFolders} folders | ${allAssets.length} images found | ${folderQueue.length} remaining`);
      }

      activeWorkers--;
    }
  }

  // Keep spawning workers while there's work
  const interval = setInterval(async () => {
    if (folderQueue.length === 0 && activeWorkers === 0) {
      clearInterval(interval);
      resolveAll();
      return;
    }
    // Spawn workers if we have capacity and work
    while (folderQueue.length > 0 && activeWorkers < CRAWL_WORKERS) {
      worker(); // fire and forget
    }
  }, 100);

  // Kick off initial workers
  for (let i = 0; i < Math.min(CRAWL_WORKERS, folderQueue.length); i++) {
    worker();
  }

  await donePromise;
  return allAssets;
}

// ── PHASE 2: Upload ───────────────────────────────────────────────────────

async function streamToS3(asset) {
  const downloadUrl = `${AEM_BASE}${asset.damPath}`;
  const relativePath = asset.damPath.replace("/content/dam/", "");
  const s3Key = `${S3_PREFIX}/${relativePath}`;

  const controller = new AbortController();
  // Hard 3-minute timeout per asset (covers download + upload)
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

    // Set an idle timeout on the stream itself — abort if no data for 30s
    let idleTimer;
    const resetIdle = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => controller.abort(), 30000);
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
    const sizeMB = contentLength ? ` (${(contentLength / 1024 / 1024).toFixed(1)}MB)` : "";
    if (uploaded % 100 === 0 || uploaded <= 5) {
      const pct = (uploaded / asset._total * 100).toFixed(1);
      console.log(`  ✓ [${uploaded}/${asset._total} ${pct}%] ${asset.name}${sizeMB}`);
    }
  } catch (err) {
    failed++;
    const reason = err.code === 'ERR_CANCELED' ? 'timeout/aborted' : (err.response?.status ? `HTTP ${err.response.status}` : err.message);
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

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  console.log(`\n🔍 AEM → S3: Coca-Cola Images (bottles/cans + soccer 2026)`);
  console.log(`   Target: s3://${S3_BUCKET}/${S3_PREFIX}/`);
  console.log(`   Seed roots: ${ROOTS.length}\n`);

  // Phase 1: Crawl (or load existing manifest)
  let assets;
  const manifestPath = "./image_manifest.json";
  if (fs.existsSync(manifestPath) && process.argv.includes("--skip-crawl")) {
    const paths = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    assets = paths.map(p => ({ damPath: p, name: p.split("/").pop() }));
    console.log(`── Loaded ${assets.length} images from existing manifest (--skip-crawl) ──\n`);
  } else {
    console.log(`── Phase 1: Crawling folder tree ──`);
    assets = await crawlAll();
    const crawlTime = ((Date.now() - startTime) / 1000).toFixed(0);
    console.log(`\n📦 Crawl done in ${crawlTime}s: ${crawledFolders} folders, ${assets.length} images, ${skippedNonImage} non-images skipped\n`);
  }

  if (assets.length === 0) {
    console.log("No images found. Exiting.");
    return;
  }

  // Save manifest
  fs.writeFileSync("./image_manifest.json", JSON.stringify(assets.map(a => a.damPath), null, 2));
  console.log(`   Manifest saved to image_manifest.json`);

  // Phase 2: Upload
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
  console.log(`   Uploaded: ${uploaded}  |  Failed: ${failed}  |  Skipped: ${skippedNonImage}`);
  console.log(`   Folders crawled: ${crawledFolders}`);

  if (failures.length > 0) {
    fs.writeFileSync("./bulk_download_failures.json", JSON.stringify(failures, null, 2));
    console.log(`⚠️  ${failures.length} failures → bulk_download_failures.json`);
  }

  process.exit(failures.length > 0 ? 2 : 0);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
