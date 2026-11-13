#!/usr/bin/env node
/**
 * Deep-scan the "digital-twin" folder in the TCCC DAM for 3D assets.
 * Also scan heritage-center and any other promising folders.
 */

const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const headers = { Authorization: `Bearer ${AEM_TOKEN}` };

const EXTENSIONS_3D = new Set([
  "obj", "fbx", "glb", "gltf", "stl", "3ds", "blend", "usdz", "usda", "usdc", "usd",
  "dae", "c4d", "max", "ma", "mb", "ply", "step", "stp", "iges", "igs",
  "3dm", "dwg", "dxf", "skp", "wrl", "x3d", "abc", "zpr"
]);

let foldersScanned = 0;
const allAssets = [];
const allFolders = [];

async function crawlFolder(damPath, depth = 0) {
  const apiPath = `/api/assets${damPath.replace("/content/dam/", "/")}.json`;
  let offset = 0;

  while (true) {
    const url = `${AEM_BASE}${apiPath}?limit=200&offset=${offset}`;
    let data;
    try {
      const resp = await axios.get(url, { headers, timeout: 15000 });
      data = resp.data;
    } catch (err) {
      if (err.response?.status === 404) return;
      console.error(`  ✗ ${damPath}: ${err.response?.status || err.message}`);
      return;
    }

    const entities = data.entities || [];
    if (entities.length === 0) break;

    for (const entity of entities) {
      const cls = (entity.class || [])[0] || "";
      const name = entity.properties?.name || "";

      if (cls === "assets/folder") {
        allFolders.push(`${damPath}/${name}`);
        // Recurse into all subfolders
        await crawlFolder(`${damPath}/${name}`, depth + 1);
      } else if (cls === "assets/asset") {
        const ext = name.split(".").pop().toLowerCase();
        if (EXTENSIONS_3D.has(ext)) {
          const asset = { path: `${damPath}/${name}`, name, extension: ext };
          allAssets.push(asset);
          console.log(`  ★ 3D ASSET: ${asset.path}`);
        }
      }
    }

    const paging = data.properties?.srn?.paging || data.properties?.["srn:paging"];
    if (!paging) break;
    offset += entities.length;
    if (offset >= (paging.total || 0)) break;
  }

  foldersScanned++;
  if (foldersScanned % 50 === 0) {
    console.log(`  ... ${foldersScanned} folders scanned, ${allAssets.length} 3D assets found`);
  }
}

async function main() {
  const targets = [
    "/content/dam/tccc/digital-twin",
    "/content/dam/tccc/heritage-center",
    "/content/dam/tccc/common",
    "/content/dam/tccc/resources",
    "/content/dam/tccc/Workfront",
  ];

  for (const target of targets) {
    console.log(`\n━━━ Deep-scanning: ${target} ━━━`);
    foldersScanned = 0;
    const before = allAssets.length;
    await crawlFolder(target);
    const found = allAssets.length - before;
    console.log(`  Done: ${foldersScanned} folders scanned, ${found} 3D assets found\n`);
  }

  // List all unique subfolders found
  console.log("\n═══ ALL SUBFOLDERS DISCOVERED ═══");
  for (const f of allFolders.sort()) {
    console.log(`  ${f}`);
  }

  console.log(`\n═══ ALL 3D ASSETS ═══`);
  if (allAssets.length > 0) {
    for (const a of allAssets) {
      console.log(`  ${a.path} (.${a.extension})`);
    }
  } else {
    console.log("  None found in these folders.");
  }

  console.log(`\n  Total folders: ${allFolders.length}`);
  console.log(`  Total 3D assets: ${allAssets.length}`);
}

main().catch(err => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
