#!/usr/bin/env node
/**
 * HEAD request each Sprite asset to capture content-length, update manifest with sizes.
 */
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = process.env.AEM_BASE_URL || "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const CONCURRENCY = parseInt(process.env.HEAD_CONCURRENCY || "30", 10);

async function head(asset) {
  const url = `${AEM_BASE}${asset.damPath}`;
  try {
    const resp = await axios.head(url, {
      headers: { Authorization: `Bearer ${AEM_TOKEN}` },
      timeout: 15000,
      maxRedirects: 5,
    });
    asset.size = parseInt(resp.headers["content-length"] || "0", 10);
  } catch (err) {
    asset.size = 0;
    asset.headError = err.response?.status || err.message;
  }
}

async function main() {
  const manifestPath = path.join(ROOT, "sprite_image_manifest.json");
  const assets = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  console.log(`Probing ${assets.length} assets with concurrency=${CONCURRENCY}...`);

  let idx = 0, done = 0;
  const start = Date.now();
  const workers = Array.from({ length: CONCURRENCY }, async () => {
    while (idx < assets.length) {
      const i = idx++;
      await head(assets[i]);
      done++;
      if (done % 500 === 0) {
        const rate = done / ((Date.now() - start) / 1000);
        console.log(`  ${done}/${assets.length} (${rate.toFixed(0)}/s)`);
      }
    }
  });
  await Promise.all(workers);

  fs.writeFileSync(manifestPath, JSON.stringify(assets, null, 2));

  const totalBytes = assets.reduce((s, a) => s + (a.size || 0), 0);
  const errs = assets.filter(a => a.headError).length;
  console.log(`\n✅ Done. Total: ${(totalBytes / 1024 / 1024 / 1024).toFixed(2)} GB | HEAD errors: ${errs}`);

  // Per-root + extension summary
  const SPRITE_ROOTS = JSON.parse(fs.readFileSync(path.join(ROOT, "sprite_discovery.json"), "utf8"))
    .sprite_brand_paths.concat([
      "/content/dam/tccc/marketing/sprite",
      "/content/dam/tccc/marketing/sprite-zero-diet-light",
      "/content/dam/tccc/marketing/absolut-vodka---sprite",
    ]);
  function rootOf(damPath) {
    let best = null;
    for (const r of SPRITE_ROOTS) {
      if (damPath.startsWith(r + "/") && (!best || r.length > best.length)) best = r;
    }
    return best || "(unknown)";
  }
  const byRoot = {};
  for (const a of assets) {
    const r = rootOf(a.damPath);
    if (!byRoot[r]) byRoot[r] = { count: 0, bytes: 0, byExt: {} };
    byRoot[r].count++;
    byRoot[r].bytes += a.size || 0;
    const ext = a.name.split(".").pop().toLowerCase();
    byRoot[r].byExt[ext] = (byRoot[r].byExt[ext] || 0) + 1;
  }
  fs.writeFileSync(path.join(ROOT, "sprite_path_summary.json"), JSON.stringify(byRoot, null, 2));
}

main().catch(e => { console.error(e); process.exit(1); });
