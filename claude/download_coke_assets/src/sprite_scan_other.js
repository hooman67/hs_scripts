#!/usr/bin/env node
/**
 * Crawl Sprite roots, build manifest of all non-image assets we want to download:
 * INCLUDE: videos (mov, mp4, ...), zips, wav, mp3, srt, pptx, docx, doc
 * EXCLUDE: pdf, psb, aep, image extensions (already done)
 */
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = process.env.AEM_BASE_URL || "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const PAGE = 200;
const TIMEOUT = 20000;

const INCLUDE_EXTS = new Set([
  // video
  "mp4", "mov", "avi", "webm", "m4v", "mkv", "mpg", "mpeg", "wmv", "flv", "ts", "3gp", "m2v", "f4v", "ogv",
  // bundles
  "zip", "rar", "7z", "tar", "gz",
  // audio + captions + office
  "wav", "mp3", "srt", "pptx", "ppt", "docx", "doc", "xls", "xlsx",
]);

const discovery = JSON.parse(fs.readFileSync(path.join(ROOT, "sprite_discovery.json"), "utf8"));
const ROOTS = [
  ...discovery.sprite_brand_paths,
  "/content/dam/tccc/marketing/sprite",
  "/content/dam/tccc/marketing/sprite-zero-diet-light",
  "/content/dam/tccc/marketing/absolut-vodka---sprite",
];

let crawled = 0;
const found = [];

function include(name) {
  return INCLUDE_EXTS.has(name.split(".").pop().toLowerCase());
}

async function listFolder(damPath) {
  const apiBase = `/api/assets${damPath.replace("/content/dam/", "/")}.json`;
  let offset = 0;
  const folders = [];
  const items = [];
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
      } else if (cls === "assets/asset" && include(name)) {
        items.push({ damPath: `${damPath}/${name}`, name });
      }
    }
    const paging = data.properties?.srn?.paging || data.properties?.["srn:paging"];
    if (!paging) break;
    offset += ents.length;
    if (offset >= (paging.total || 0)) break;
  }
  crawled++;
  return { folders, items };
}

async function main() {
  const queue = [...ROOTS];
  let active = 0, resolveAll;
  const done = new Promise(r => { resolveAll = r; });
  const W = 10;
  async function worker() {
    while (true) {
      const p = queue.shift();
      if (!p) break;
      active++;
      const { folders, items } = await listFolder(p);
      found.push(...items);
      queue.push(...folders);
      if (crawled % 200 === 0) {
        console.log(`  crawl: ${crawled} folders | ${found.length} items | ${queue.length} queued`);
      }
      active--;
    }
  }
  const itv = setInterval(() => {
    if (queue.length === 0 && active === 0) { clearInterval(itv); resolveAll(); return; }
    while (queue.length > 0 && active < W) worker();
  }, 100);
  for (let i = 0; i < Math.min(W, queue.length); i++) worker();
  await done;

  console.log(`\n✅ Crawl done: ${crawled} folders, ${found.length} items.\n`);

  const byExt = {};
  for (const v of found) {
    const e = v.name.split(".").pop().toLowerCase();
    byExt[e] = (byExt[e] || 0) + 1;
  }
  console.log("By ext:", byExt);

  fs.writeFileSync(path.join(ROOT, "sprite_other_manifest.json"), JSON.stringify(found, null, 2));
  console.log(`Saved → sprite_other_manifest.json`);
}
main().catch(e => { console.error(e); process.exit(1); });
