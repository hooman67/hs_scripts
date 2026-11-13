#!/usr/bin/env node
/**
 * Crawl the same Sprite DAM roots, but tally VIDEO assets.
 */
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = process.env.AEM_BASE_URL || "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const PAGE = 200;
const TIMEOUT = 20000;

const VIDEO_EXTS = new Set([".mp4", ".mov", ".avi", ".webm", ".m4v", ".mkv", ".mpg", ".mpeg", ".wmv", ".flv", ".ts", ".3gp", ".m2v", ".f4v", ".ogv"]);

const discovery = JSON.parse(fs.readFileSync(path.join(ROOT, "sprite_discovery.json"), "utf8"));
const ROOTS = [
  ...discovery.sprite_brand_paths,
  "/content/dam/tccc/marketing/sprite",
  "/content/dam/tccc/marketing/sprite-zero-diet-light",
  "/content/dam/tccc/marketing/absolut-vodka---sprite",
];

let crawled = 0;
const videos = [];
const otherExts = {}; // tally everything non-image, non-video

function isVideo(name) {
  const ext = "." + name.split(".").pop().toLowerCase();
  return VIDEO_EXTS.has(ext);
}

async function listFolder(damPath) {
  const apiBase = `/api/assets${damPath.replace("/content/dam/", "/")}.json`;
  let offset = 0;
  const folders = [];
  const found = [];
  while (true) {
    const url = `${AEM_BASE}${apiBase}?limit=${PAGE}&offset=${offset}`;
    let data;
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), TIMEOUT);
      const r = await axios.get(url, { headers: { Authorization: `Bearer ${AEM_TOKEN}` }, timeout: TIMEOUT, signal: ctrl.signal });
      clearTimeout(t);
      data = r.data;
    } catch (e) {
      if (e.response?.status === 404) break;
      console.error(`  ✗ ${damPath}: ${e.message}`);
      break;
    }
    const ents = data.entities || [];
    if (ents.length === 0) break;
    for (const e of ents) {
      const cls = (e.class || [])[0] || "";
      const name = e.properties?.name;
      if (!name) continue;
      if (cls === "assets/folder") {
        if (["none", "no", "null", "n-a"].includes(name.toLowerCase())) continue;
        folders.push(`${damPath}/${name}`);
      } else if (cls === "assets/asset") {
        if (isVideo(name)) {
          const meta = e.properties?.metadata || {};
          const size = e.properties?.["jcr:content"]?.["jcr:data"]?.length || meta["dam:size"] || 0;
          found.push({ damPath: `${damPath}/${name}`, name, size });
        } else {
          // Track non-image, non-video extensions for awareness
          const ext = (name.split(".").pop() || "").toLowerCase();
          const imageExts = ["jpg","jpeg","png","tiff","tif","gif","webp","bmp","svg","psd","ai","eps","heic","heif"];
          if (!imageExts.includes(ext)) otherExts[ext] = (otherExts[ext] || 0) + 1;
        }
      }
    }
    const paging = data.properties?.srn?.paging || data.properties?.["srn:paging"];
    if (!paging) break;
    offset += ents.length;
    if (offset >= (paging.total || 0)) break;
  }
  crawled++;
  return { folders, found };
}

async function main() {
  const queue = [...ROOTS];
  let active = 0;
  let resolveAll;
  const done = new Promise(r => { resolveAll = r; });
  const WORKERS = 10;

  async function worker() {
    while (true) {
      const p = queue.shift();
      if (!p) break;
      active++;
      const { folders, found } = await listFolder(p);
      videos.push(...found);
      queue.push(...folders);
      if (crawled % 200 === 0) {
        console.log(`  crawl: ${crawled} folders | ${videos.length} videos | ${queue.length} queued`);
      }
      active--;
    }
  }
  const itv = setInterval(() => {
    if (queue.length === 0 && active === 0) { clearInterval(itv); resolveAll(); return; }
    while (queue.length > 0 && active < WORKERS) worker();
  }, 100);
  for (let i = 0; i < Math.min(WORKERS, queue.length); i++) worker();
  await done;

  console.log(`\n✅ Crawl done: ${crawled} folders scanned, ${videos.length} videos found.\n`);
  // Count by extension
  const byExt = {};
  for (const v of videos) {
    const e = v.name.split(".").pop().toLowerCase();
    byExt[e] = (byExt[e] || 0) + 1;
  }
  console.log("By extension:", byExt);

  // Group by root
  const byRoot = {};
  for (const v of videos) {
    let best = null;
    for (const r of ROOTS) {
      if (v.damPath.startsWith(r + "/") && (!best || r.length > best.length)) best = r;
    }
    const k = best || "(other)";
    byRoot[k] = (byRoot[k] || 0) + 1;
  }
  console.log("\nBy root (videos):");
  for (const [k, n] of Object.entries(byRoot).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${n.toString().padStart(4)}  ${k}`);
  }

  console.log("\nOther non-image, non-video extensions seen (file types we'd skip):", otherExts);

  fs.writeFileSync(path.join(ROOT, "sprite_video_manifest.json"), JSON.stringify(videos, null, 2));
  console.log(`\nSaved → sprite_video_manifest.json`);
  if (videos.length > 0) {
    console.log("\nFirst 10:");
    for (const v of videos.slice(0, 10)) console.log(`  ${v.damPath}`);
  }
}
main().catch(e => { console.error(e); process.exit(1); });
