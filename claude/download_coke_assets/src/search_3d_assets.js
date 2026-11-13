#!/usr/bin/env node
/**
 * Search the entire Coca-Cola DAM for 3D assets.
 * Uses multiple approaches:
 *   1. AEM QueryBuilder API to search by file extension
 *   2. AEM Assets API to crawl key folders looking for 3D file types
 *
 * Usage: node src/search_3d_assets.js
 */

const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = process.env.AEM_BASE_URL || "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();

const headers = { Authorization: `Bearer ${AEM_TOKEN}` };

// Common 3D file extensions
const EXTENSIONS_3D = [
  "obj", "fbx", "glb", "gltf", "stl", "3ds", "blend", "usdz", "usda", "usdc", "usd",
  "dae", "c4d", "max", "ma", "mb", "ply", "step", "stp", "iges", "igs",
  "3dm", "dwg", "dxf", "skp", "wrl", "x3d", "abc", "zpr"
];

// Also search by dc:format (MIME types for 3D)
const MIME_TYPES_3D = [
  "model/gltf-binary", "model/gltf+json", "model/obj", "model/stl",
  "model/vnd.usdz+zip", "model/x-fbx", "application/x-blender",
  "model/vnd.collada+xml", "model/3mf", "model/step",
  "application/octet-stream" // sometimes 3D files get this generic type
];

let totalFound = 0;
const allResults = [];

// ── Approach 1: QueryBuilder search by extension ─────────────────────────

async function queryBuilderSearch(extension) {
  const params = new URLSearchParams({
    "path": "/content/dam/tccc",
    "type": "dam:Asset",
    "nodename": `*.${extension}`,
    "p.limit": "100",
    "p.hits": "full",
    "p.properties": "jcr:path jcr:content/metadata/dc:title jcr:content/metadata/dc:format jcr:content/metadata/dam:size",
  });

  try {
    const resp = await axios.get(`${AEM_BASE}/bin/querybuilder.json?${params}`, {
      headers,
      timeout: 30000,
    });
    return resp.data;
  } catch (err) {
    if (err.response?.status === 404 || err.response?.status === 403) {
      return null; // endpoint not available
    }
    throw err;
  }
}

async function searchByExtensions() {
  console.log("\n━━━ Approach 1: QueryBuilder search by file extension ━━━\n");

  for (const ext of EXTENSIONS_3D) {
    try {
      const result = await queryBuilderSearch(ext);
      if (!result) {
        console.log(`  [QueryBuilder not available - switching to Assets API only]`);
        return false;
      }
      const hits = result.hits || [];
      if (hits.length > 0) {
        console.log(`  ✓ .${ext}: ${result.total || hits.length} results`);
        for (const hit of hits) {
          const entry = {
            path: hit["jcr:path"] || hit.path,
            name: (hit["jcr:path"] || hit.path || "").split("/").pop(),
            format: hit["jcr:content"]?.metadata?.["dc:format"] || "unknown",
            extension: ext,
            source: "querybuilder",
          };
          allResults.push(entry);
          console.log(`    → ${entry.path}`);
        }
      }
    } catch (err) {
      const status = err.response?.status || err.code || err.message;
      console.log(`  ✗ .${ext}: ${status}`);
    }
  }
  return true;
}

// ── Approach 2: Search using fulltext/omnisearch ─────────────────────────

async function omnisearch(query) {
  const params = new URLSearchParams({
    "fulltext": query,
    "path": "/content/dam/tccc",
    "type": "dam:Asset",
    "p.limit": "50",
    "p.hits": "full",
  });

  try {
    const resp = await axios.get(`${AEM_BASE}/bin/querybuilder.json?${params}`, {
      headers,
      timeout: 30000,
    });
    return resp.data;
  } catch {
    return null;
  }
}

async function searchByKeywords() {
  console.log("\n━━━ Approach 2: Fulltext keyword search ━━━\n");

  const keywords = ["3D", "3d model", "3d render", "three-dimensional", "CGI", "product render"];

  for (const kw of keywords) {
    try {
      const result = await omnisearch(kw);
      if (!result) {
        console.log(`  [Fulltext search not available]`);
        return;
      }
      const hits = result.hits || [];
      console.log(`  "${kw}": ${result.total || hits.length} results`);
      for (const hit of hits.slice(0, 10)) {
        const p = hit["jcr:path"] || hit.path;
        console.log(`    → ${p}`);
        allResults.push({
          path: p,
          name: (p || "").split("/").pop(),
          extension: (p || "").split(".").pop(),
          source: `fulltext:"${kw}"`,
        });
      }
    } catch (err) {
      console.log(`  "${kw}": error - ${err.message}`);
    }
  }
}

// ── Approach 3: Assets API - check specific likely folders ───────────────

async function listFolder(damPath, depth = 0, maxDepth = 2) {
  const apiPath = `/api/assets${damPath.replace("/content/dam/", "/")}.json`;
  let offset = 0;
  const found = [];

  while (true) {
    const url = `${AEM_BASE}${apiPath}?limit=200&offset=${offset}`;
    let data;
    try {
      const resp = await axios.get(url, { headers, timeout: 15000 });
      data = resp.data;
    } catch (err) {
      if (err.response?.status === 404) break;
      break;
    }

    const entities = data.entities || [];
    if (entities.length === 0) break;

    for (const entity of entities) {
      const cls = (entity.class || [])[0] || "";
      const name = entity.properties?.name || "";
      const nameLower = name.toLowerCase();

      if (cls === "assets/asset") {
        const ext = name.split(".").pop().toLowerCase();
        if (EXTENSIONS_3D.includes(ext)) {
          found.push({
            path: `${damPath}/${name}`,
            name,
            extension: ext,
            source: "assets-api-crawl",
          });
        }
        // Also flag if the name suggests 3D content
        if (nameLower.match(/3d|render|cgi|model|three.?dim/i) && !EXTENSIONS_3D.includes(ext)) {
          found.push({
            path: `${damPath}/${name}`,
            name,
            extension: ext,
            source: "assets-api-crawl (name match)",
          });
        }
      } else if (cls === "assets/folder" && depth < maxDepth) {
        const folderName = name.toLowerCase();
        // Recurse into folders that might contain 3D content
        if (folderName.match(/3d|render|cgi|model|packag|product|bottle|can|asset/i) || depth < 1) {
          const subResults = await listFolder(`${damPath}/${name}`, depth + 1, maxDepth);
          found.push(...subResults);
        }
      }
    }

    const paging = data.properties?.srn?.paging || data.properties?.["srn:paging"];
    if (!paging) break;
    offset += entities.length;
    if (offset >= (paging.total || 0)) break;
  }

  return found;
}

async function searchKeyFolders() {
  console.log("\n━━━ Approach 3: Crawl key DAM folders for 3D files ━━━\n");

  // Top-level folders to check
  const foldersToCheck = [
    "/content/dam/tccc",              // root - shallow scan
    "/content/dam/tccc/products",     // product images might have 3D renders
    "/content/dam/tccc/marketing",    // marketing assets
    "/content/dam/tccc/3d",           // dedicated 3D folder?
    "/content/dam/tccc/3D",           // case variant
    "/content/dam/tccc/renderings",   // renderings folder?
    "/content/dam/tccc/models",       // models folder?
    "/content/dam/tccc/cgi",          // CGI assets?
    "/content/dam/tccc/packaging",    // packaging might have 3D
    "/content/dam/tccc/brand-assets", // brand assets
  ];

  for (const folder of foldersToCheck) {
    console.log(`  Scanning: ${folder}`);
    try {
      const results = await listFolder(folder, 0, 3);
      if (results.length > 0) {
        console.log(`    ✓ Found ${results.length} potential 3D assets!`);
        for (const r of results) {
          console.log(`      → ${r.path} (${r.source})`);
          allResults.push(r);
        }
      } else {
        console.log(`    (no 3D assets found)`);
      }
    } catch (err) {
      console.log(`    ✗ ${err.response?.status || err.message}`);
    }
  }
}

// ── Approach 4: List all top-level folders to find 3D-related ones ───────

async function discoverTopFolders() {
  console.log("\n━━━ Approach 4: Discover all top-level DAM folders ━━━\n");

  const apiPath = `/api/assets/tccc.json`;
  let offset = 0;
  const folders = [];

  while (true) {
    const url = `${AEM_BASE}${apiPath}?limit=200&offset=${offset}`;
    let data;
    try {
      const resp = await axios.get(url, { headers, timeout: 15000 });
      data = resp.data;
    } catch (err) {
      console.log(`  ✗ Could not list top-level folders: ${err.response?.status || err.message}`);
      return;
    }

    const entities = data.entities || [];
    if (entities.length === 0) break;

    for (const entity of entities) {
      const cls = (entity.class || [])[0] || "";
      const name = entity.properties?.name || "";
      if (cls === "assets/folder") {
        folders.push(name);
      }
    }

    const paging = data.properties?.srn?.paging || data.properties?.["srn:paging"];
    if (!paging) break;
    offset += entities.length;
    if (offset >= (paging.total || 0)) break;
  }

  console.log(`  Found ${folders.length} top-level folders under /content/dam/tccc/:`);
  for (const f of folders.sort()) {
    const is3d = f.toLowerCase().match(/3d|render|cgi|model|packag/i);
    console.log(`    ${is3d ? "★" : " "} ${f}`);
  }

  // Deep-scan any folder whose name suggests 3D content
  const interesting = folders.filter(f =>
    f.toLowerCase().match(/3d|render|cgi|model|packag|asset|creative|production|toolkit/i)
  );

  if (interesting.length > 0) {
    console.log(`\n  Deep-scanning ${interesting.length} interesting folders...`);
    for (const f of interesting) {
      console.log(`\n  Scanning: /content/dam/tccc/${f}`);
      const results = await listFolder(`/content/dam/tccc/${f}`, 0, 4);
      if (results.length > 0) {
        console.log(`    ✓ Found ${results.length} potential 3D assets!`);
        for (const r of results) {
          console.log(`      → ${r.path}`);
          allResults.push(r);
        }
      }
    }
  }
}

// ── Approach 5: Search via AEM's property-based queries ──────────────────

async function searchByMimeType() {
  console.log("\n━━━ Approach 5: Search by MIME type / dc:format ━━━\n");

  for (const mime of MIME_TYPES_3D) {
    if (mime === "application/octet-stream") continue; // too generic

    const params = new URLSearchParams({
      "path": "/content/dam/tccc",
      "type": "dam:Asset",
      "property": "jcr:content/metadata/dc:format",
      "property.value": mime,
      "p.limit": "50",
      "p.hits": "full",
    });

    try {
      const resp = await axios.get(`${AEM_BASE}/bin/querybuilder.json?${params}`, {
        headers,
        timeout: 30000,
      });
      const hits = resp.data?.hits || [];
      if (hits.length > 0) {
        console.log(`  ✓ ${mime}: ${resp.data.total || hits.length} results`);
        for (const hit of hits) {
          const p = hit["jcr:path"] || hit.path;
          console.log(`    → ${p}`);
          allResults.push({
            path: p,
            name: (p || "").split("/").pop(),
            format: mime,
            source: `mime:${mime}`,
          });
        }
      }
    } catch (err) {
      if (err.response?.status === 403 || err.response?.status === 404) {
        console.log(`  [QueryBuilder not available for MIME search]`);
        return;
      }
      console.log(`  ✗ ${mime}: ${err.response?.status || err.message}`);
    }
  }
}

// ── Main ─────────────────────────────────────────────────────────────────

async function main() {
  console.log("╔══════════════════════════════════════════════════════════╗");
  console.log("║   TCCC DAM: 3D Asset Search                            ║");
  console.log("╚══════════════════════════════════════════════════════════╝");
  console.log(`\nAEM: ${AEM_BASE}`);
  console.log(`Searching for extensions: ${EXTENSIONS_3D.join(", ")}`);
  console.log(`Token: ${AEM_TOKEN.substring(0, 20)}...`);

  // Run all approaches
  const qbWorked = await searchByExtensions();
  if (qbWorked) {
    await searchByKeywords();
    await searchByMimeType();
  }
  await discoverTopFolders();
  await searchKeyFolders();

  // Deduplicate results
  const seen = new Set();
  const unique = allResults.filter(r => {
    if (seen.has(r.path)) return false;
    seen.add(r.path);
    return true;
  });

  // Summary
  console.log("\n" + "═".repeat(60));
  console.log(`\n📊 SEARCH COMPLETE`);
  console.log(`   Total unique results: ${unique.length}`);

  if (unique.length > 0) {
    console.log("\n   All 3D assets found:");
    for (const r of unique) {
      console.log(`   • ${r.path}`);
      console.log(`     ext: .${r.extension || "?"} | source: ${r.source}${r.format ? ` | format: ${r.format}` : ""}`);
    }
  } else {
    console.log("\n   ❌ No 3D assets found in the DAM.");
    console.log("   The search covered:");
    console.log(`     - ${EXTENSIONS_3D.length} 3D file extensions`);
    console.log(`     - ${MIME_TYPES_3D.length} 3D MIME types`);
    console.log("     - Keyword/fulltext search");
    console.log("     - All top-level folder discovery");
    console.log("     - Targeted folder crawling");
  }

  // Save results
  const outPath = path.join(ROOT, "3d_asset_search_results.json");
  fs.writeFileSync(outPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    aem_base: AEM_BASE,
    extensions_searched: EXTENSIONS_3D,
    mime_types_searched: MIME_TYPES_3D,
    results: unique,
    total: unique.length,
  }, null, 2));
  console.log(`\n   Results saved to: ${outPath}`);
}

main().catch(err => {
  console.error("Fatal:", err.message || err);
  if (err.response?.status === 401) {
    console.error("\n⚠️  Token expired. Run: npm run token");
  }
  process.exit(1);
});
