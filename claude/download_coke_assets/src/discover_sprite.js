#!/usr/bin/env node
/**
 * Probe AEM DAM for Sprite-related paths.
 * 1. List /content/dam/tccc/products/ → collect country folders
 * 2. List /content/dam/tccc/products/{country}/ → find sprite* brand folders
 * 3. List /content/dam/tccc/marketing/ → find sprite* campaign folders
 * 4. Use AEM querybuilder to search for assets with "sprite" in path/metadata
 *
 * Output: sprite_discovery.json
 */

const axios = require("axios");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = process.env.AEM_BASE_URL || "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();
const PAGE = 200;
const TIMEOUT = 20000;

async function listFolder(damPath) {
  const apiBase = `/api/assets${damPath.replace("/content/dam/", "/")}.json`;
  let offset = 0;
  const folders = [];
  const assets = [];
  while (true) {
    const url = `${AEM_BASE}${apiBase}?limit=${PAGE}&offset=${offset}`;
    let data;
    try {
      const resp = await axios.get(url, {
        headers: { Authorization: `Bearer ${AEM_TOKEN}` },
        timeout: TIMEOUT,
      });
      data = resp.data;
    } catch (err) {
      if (err.response?.status === 404) return { folders, assets, error: "404" };
      return { folders, assets, error: err.message };
    }
    const entities = data.entities || [];
    if (entities.length === 0) break;
    for (const entity of entities) {
      const cls = (entity.class || [])[0] || "";
      const name = entity.properties?.name;
      if (!name) continue;
      if (cls === "assets/folder") folders.push(name);
      else if (cls === "assets/asset") assets.push(name);
    }
    const paging = data.properties?.srn?.paging || data.properties?.["srn:paging"];
    if (!paging) break;
    offset += entities.length;
    if (offset >= (paging.total || 0)) break;
  }
  return { folders, assets };
}

async function querybuilderSearch() {
  // AEM querybuilder: find dam:Asset under /content/dam/tccc whose path contains "sprite"
  const url = `${AEM_BASE}/bin/querybuilder.json` +
    `?path=/content/dam/tccc` +
    `&type=dam:Asset` +
    `&fulltext=sprite` +
    `&p.hits=full` +
    `&p.limit=50` +
    `&p.properties=jcr:path`;
  try {
    const resp = await axios.get(url, {
      headers: { Authorization: `Bearer ${AEM_TOKEN}` },
      timeout: TIMEOUT,
    });
    return resp.data;
  } catch (err) {
    return { error: err.message, status: err.response?.status };
  }
}

async function main() {
  const result = {
    products_root: {},
    marketing_root: {},
    sprite_brand_paths: [],   // /content/dam/tccc/products/{country}/sprite*
    sprite_marketing_paths: [], // /content/dam/tccc/marketing/sprite*
    other_sprite_paths: [],    // Any other sprite path discovered
    querybuilder: null,
  };

  // Step 1: Top of products tree → list countries
  console.log("→ Listing /content/dam/tccc/products/");
  const products = await listFolder("/content/dam/tccc/products");
  result.products_root = products;
  console.log(`  Found ${products.folders.length} country folders`);

  // Step 2: For each country, list sub-brands and find sprite*
  console.log("→ Searching for sprite* brand folders under each country...");
  const countries = products.folders;
  const brandSet = new Set();
  for (const country of countries) {
    const sub = await listFolder(`/content/dam/tccc/products/${country}`);
    if (sub.folders) {
      for (const brand of sub.folders) {
        brandSet.add(brand);
        if (brand.toLowerCase().startsWith("sprite")) {
          result.sprite_brand_paths.push(`/content/dam/tccc/products/${country}/${brand}`);
        }
      }
    }
  }
  result.all_brands_seen = [...brandSet].sort();
  console.log(`  Distinct brand folders observed: ${brandSet.size}`);
  console.log(`  Sprite brand folders found: ${result.sprite_brand_paths.length}`);

  // Step 3: List /content/dam/tccc/marketing/ → find sprite folders
  console.log("→ Listing /content/dam/tccc/marketing/");
  const marketing = await listFolder("/content/dam/tccc/marketing");
  result.marketing_root = marketing;
  for (const folder of marketing.folders || []) {
    if (folder.toLowerCase().includes("sprite")) {
      result.sprite_marketing_paths.push(`/content/dam/tccc/marketing/${folder}`);
    }
  }
  console.log(`  Marketing top folders: ${marketing.folders.length}`);
  console.log(`  Sprite marketing folders: ${result.sprite_marketing_paths.length}`);

  // Step 3b: Look inside /content/dam/tccc/marketing/sprite/ if exists
  if (marketing.folders.includes("sprite")) {
    const spriteCampaigns = await listFolder("/content/dam/tccc/marketing/sprite");
    result.sprite_marketing_subfolders = spriteCampaigns.folders;
  }

  // Step 4: querybuilder search
  console.log("→ Running querybuilder fulltext sprite search...");
  result.querybuilder = await querybuilderSearch();

  fs.writeFileSync(path.join(ROOT, "sprite_discovery.json"), JSON.stringify(result, null, 2));
  console.log("\n✅ Saved sprite_discovery.json");
  console.log(JSON.stringify({
    sprite_brand_paths: result.sprite_brand_paths.slice(0, 10),
    sprite_brand_count: result.sprite_brand_paths.length,
    sprite_marketing_paths: result.sprite_marketing_paths,
    sprite_marketing_subfolders: result.sprite_marketing_subfolders,
    countries_seen: countries.length,
    all_brand_count: brandSet.size,
    qb_status: result.querybuilder?.results !== undefined ? `OK (${result.querybuilder.total} hits)` : `error: ${JSON.stringify(result.querybuilder).slice(0,200)}`,
  }, null, 2));
}

main().catch(e => { console.error(e); process.exit(1); });
