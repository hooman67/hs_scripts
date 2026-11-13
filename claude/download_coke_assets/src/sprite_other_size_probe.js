#!/usr/bin/env node
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const CONC = 30;

async function head(asset) {
  try {
    const r = await axios.head(`${AEM_BASE}${asset.damPath}`, {
      headers: { Authorization: `Bearer ${AEM_TOKEN}` }, timeout: 15000, maxRedirects: 5,
    });
    asset.size = parseInt(r.headers["content-length"] || "0", 10);
  } catch (e) { asset.size = 0; asset.headError = e.response?.status || e.message; }
}

(async () => {
  const items = JSON.parse(fs.readFileSync(path.join(ROOT, "sprite_other_manifest.json"), "utf8"));
  console.log(`HEAD-probing ${items.length} items @ conc=${CONC}`);
  let idx = 0, done = 0;
  const start = Date.now();
  await Promise.all(Array.from({ length: CONC }, async () => {
    while (idx < items.length) {
      const i = idx++;
      await head(items[i]);
      done++;
      if (done % 500 === 0) console.log(`  ${done}/${items.length} (${(done / ((Date.now() - start) / 1000)).toFixed(0)}/s)`);
    }
  }));
  fs.writeFileSync(path.join(ROOT, "sprite_other_manifest.json"), JSON.stringify(items, null, 2));

  const total = items.reduce((s, a) => s + (a.size || 0), 0);
  const errs = items.filter(a => a.headError).length;
  console.log(`\nTotal: ${(total / 1024 / 1024 / 1024).toFixed(2)} GB | HEAD errors: ${errs}`);

  const byExt = {};
  for (const a of items) {
    const e = a.name.split(".").pop().toLowerCase();
    if (!byExt[e]) byExt[e] = { count: 0, bytes: 0 };
    byExt[e].count++;
    byExt[e].bytes += a.size || 0;
  }
  console.log("\nBy extension:");
  for (const [e, s] of Object.entries(byExt).sort((a, b) => b[1].bytes - a[1].bytes)) {
    console.log(`  ${e.padEnd(6)} ${s.count.toString().padStart(5)}  ${(s.bytes / 1024 / 1024 / 1024).toFixed(2)} GB`);
  }
})();
