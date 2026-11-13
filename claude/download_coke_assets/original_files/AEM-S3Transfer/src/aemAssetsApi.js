const axios = require("axios");
const path = require("path");
const { requireEnv } = require("./utils");
const { logger } = require("./logger");

function ensureLeadingSlash(p) {
  const s = String(p || "").trim();
  if (!s) return s;
  return s.startsWith("/") ? s : `/${s}`;
}

function lastSegment(damPath) {
  const clean = String(damPath).replace(/\/+$/g, "");
  const seg = clean.split("/").pop();
  return seg || "dam-folder";
}

function joinUrl(baseUrl, maybeRelativeUrl) {
  const u = String(maybeRelativeUrl || "").trim();
  if (!u) return u;
  if (u.startsWith("http://") || u.startsWith("https://")) return u;
  return `${baseUrl.replace(/\/+$/g, "")}/${u.replace(/^\/+/g, "")}`;
}

function stripJcrContent(p) {
  return String(p || "").replace(/\/jcr:content.*$/g, "");
}

async function listAssetsUnderDamPath({ damPath }) {
  const baseUrl = requireEnv("AEM_BASE_URL").replace(/\/+$/g, "");
  const token = requireEnv("AEM_BEARER_TOKEN");

  const rootDamPath = ensureLeadingSlash(damPath);
  if (!rootDamPath.startsWith("/content/dam/")) {
    throw new Error(`DAM path must start with /content/dam/. Got: ${rootDamPath}`);
  }

  const url = `${baseUrl}/bin/querybuilder.json`;
  const pageSize = Number(process.env.QB_PAGE_SIZE || 200);

  const assets = [];
  const seen = new Set();

  let offset = 0;

  logger.info("Listing DAM assets using QueryBuilder.", {
    damPath: rootDamPath,
    pageSize
  });

  while (true) {
    logger.debug("QueryBuilder request.", { url, offset, pageSize });

    const res = await axios.get(url, {
      headers: { Authorization: `Bearer ${token}` },
      params: {
        path: rootDamPath,
        type: "dam:Asset",
        "p.limit": String(pageSize),
        "p.offset": String(offset)
      },
      validateStatus: (s) => s >= 200 && s < 300
    });

    const hits = Array.isArray(res.data?.hits) ? res.data.hits : [];
    const total = Number(res.data?.results || NaN);

    logger.debug("QueryBuilder response.", {
      offset,
      hits: hits.length,
      total: Number.isFinite(total) ? total : undefined
    });

    for (const h of hits) {
      const assetPath = stripJcrContent(h.path);
      if (!assetPath) continue;

      const downloadUrl = joinUrl(baseUrl, assetPath);
      const relPath = path
        .relative(rootDamPath, assetPath)
        .split(path.sep)
        .join("/");

      const k = `${downloadUrl}__${relPath}`;
      if (!seen.has(k)) {
        seen.add(k);
        assets.push({ downloadUrl, relPath });
      }
    }

    offset += pageSize;

    if (hits.length < pageSize) break;
    if (Number.isFinite(total) && offset >= total) break;

    if (offset > 2_000_000) {
      throw new Error("QueryBuilder pagination safety stop triggered (offset > 2,000,000).");
    }
  }

  logger.info("QueryBuilder listing complete.", { damPath: rootDamPath, assets: assets.length });

  return { damRootName: lastSegment(rootDamPath), assets, mode: "querybuilder" };
}

module.exports = { listAssetsUnderDamPath };
