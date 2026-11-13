#!/usr/bin/env node
/**
 * Check what file formats exist in the digital-twin folder,
 * and also run broader QueryBuilder searches for 3D-related content.
 */

const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const headers = { Authorization: `Bearer ${AEM_TOKEN}` };

async function query(params) {
  const qs = new URLSearchParams(params);
  const resp = await axios.get(`${AEM_BASE}/bin/querybuilder.json?${qs}`, {
    headers, timeout: 60000
  });
  return resp.data;
}

async function main() {
  // 1. What file types exist in digital-twin?
  console.log("━━━ What's in /content/dam/tccc/digital-twin? ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc/digital-twin",
      "type": "dam:Asset",
      "p.limit": "20",
      "p.hits": "full",
      "p.properties": "jcr:path jcr:content/metadata/dc:format",
      "orderby": "@jcr:content/jcr:lastModified",
      "orderby.sort": "desc",
    });
    console.log(`  Total assets in digital-twin: ${result.total}`);
    const formats = {};
    for (const hit of (result.hits || [])) {
      const p = hit["jcr:path"] || hit.path || "";
      const ext = p.split(".").pop().toLowerCase();
      const fmt = hit["jcr:content"]?.metadata?.["dc:format"] || "?";
      formats[ext] = (formats[ext] || 0) + 1;
      console.log(`  ${p.split("/").slice(-3).join("/")} (${fmt})`);
    }
    console.log(`  File extensions seen: ${JSON.stringify(formats)}`);
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 2. Search for any "3d" in asset names across entire DAM
  console.log("\n━━━ Assets with '3d' in name (entire DAM) ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "dam:Asset",
      "nodename": "*3d*",
      "p.limit": "50",
      "p.hits": "full",
    });
    console.log(`  Total: ${result.total}`);
    for (const hit of (result.hits || [])) {
      const p = hit["jcr:path"] || hit.path;
      console.log(`  → ${p}`);
    }
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 3. Search for folders with "3d" in name
  console.log("\n━━━ Folders with '3d' in name ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "sling:OrderedFolder",
      "nodename": "*3d*",
      "p.limit": "50",
      "p.hits": "full",
    });
    console.log(`  Total: ${result.total}`);
    for (const hit of (result.hits || [])) {
      const p = hit["jcr:path"] || hit.path;
      console.log(`  → ${p}`);
    }
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 4. Search for assets with "render" in name
  console.log("\n━━━ Assets with 'render' in name ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "dam:Asset",
      "nodename": "*render*",
      "p.limit": "30",
      "p.hits": "full",
    });
    console.log(`  Total: ${result.total}`);
    for (const hit of (result.hits || []).slice(0, 15)) {
      const p = hit["jcr:path"] || hit.path;
      const name = p.split("/").pop();
      console.log(`  → ${name} — ${p}`);
    }
    if ((result.total || 0) > 15) console.log(`  ... and ${result.total - 15} more`);
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 5. Search for assets with "model" in name
  console.log("\n━━━ Assets with 'model' in name ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "dam:Asset",
      "nodename": "*model*",
      "p.limit": "30",
      "p.hits": "full",
    });
    console.log(`  Total: ${result.total}`);
    for (const hit of (result.hits || []).slice(0, 15)) {
      const p = hit["jcr:path"] || hit.path;
      console.log(`  → ${p}`);
    }
    if ((result.total || 0) > 15) console.log(`  ... and ${result.total - 15} more`);
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 6. Search for "cgi" in folder names
  console.log("\n━━━ Folders with 'cgi' in name ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "sling:OrderedFolder",
      "nodename": "*cgi*",
      "p.limit": "50",
      "p.hits": "full",
    });
    console.log(`  Total: ${result.total}`);
    for (const hit of (result.hits || [])) {
      const p = hit["jcr:path"] || hit.path;
      console.log(`  → ${p}`);
    }
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 7. Search for ZIP files that might contain 3D assets
  console.log("\n━━━ ZIP files with '3d' in name ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "dam:Asset",
      "1_property": "jcr:content/metadata/dc:format",
      "1_property.value": "application/zip",
      "nodename": "*3d*",
      "p.limit": "20",
      "p.hits": "full",
    });
    console.log(`  Total: ${result.total}`);
    for (const hit of (result.hits || [])) {
      const p = hit["jcr:path"] || hit.path;
      console.log(`  → ${p}`);
    }
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 8. Also check all non-standard MIME types (model/*)
  console.log("\n━━━ Assets with model/* MIME type ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "dam:Asset",
      "property": "jcr:content/metadata/dc:format",
      "property.operation": "like",
      "property.value": "model/%",
      "p.limit": "50",
      "p.hits": "full",
    });
    console.log(`  Total: ${result.total}`);
    for (const hit of (result.hits || [])) {
      const p = hit["jcr:path"] || hit.path;
      console.log(`  → ${p}`);
    }
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }

  // 9. All unique dc:format values in the DAM (sample)
  console.log("\n━━━ Unique MIME types in DAM (sampling) ━━━\n");
  try {
    const result = await query({
      "path": "/content/dam/tccc",
      "type": "dam:Asset",
      "property": "jcr:content/metadata/dc:format",
      "property.operation": "exists",
      "p.limit": "500",
      "p.hits": "selective",
      "p.properties": "jcr:content/metadata/dc:format",
      "p.nodedepth": "3",
    });
    const mimeSet = new Set();
    for (const hit of (result.hits || [])) {
      const fmt = hit["jcr:content"]?.metadata?.["dc:format"];
      if (fmt) mimeSet.add(fmt);
    }
    console.log(`  Unique MIME types found (from ${result.total} total assets):`);
    for (const m of [...mimeSet].sort()) {
      console.log(`    ${m}`);
    }
  } catch (err) {
    console.log(`  Error: ${err.response?.status || err.message}`);
  }
}

main().catch(err => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
