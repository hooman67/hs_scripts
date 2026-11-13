const path = require("path");
const fs = require("fs");

const { readCSV, findAuthorLinkColumn, findDamPathColumn } = require("../src/csv");
const { getAemStream } = require("../src/aem");
const { listAssetsUnderDamPath } = require("../src/aemAssetsApi");

// Read first N bytes from a stream to prove the connection works
async function readFirstBytes(stream, maxBytes = 256 * 1024) {
  return new Promise((resolve, reject) => {
    let total = 0;
    const chunks = [];

    function cleanup() {
      stream.off("data", onData);
      stream.off("end", onEnd);
      stream.off("error", onErr);
    }

    function onErr(err) {
      cleanup();
      reject(err);
    }

    function onEnd() {
      cleanup();
      resolve(Buffer.concat(chunks, total));
    }

    function onData(chunk) {
      chunks.push(chunk);
      total += chunk.length;

      if (total >= maxBytes) {
        cleanup();
        if (typeof stream.destroy === "function") stream.destroy();
        resolve(Buffer.concat(chunks, total));
      }
    }

    stream.on("error", onErr);
    stream.on("data", onData);
    stream.on("end", onEnd);
  });
}

describe("AEM integration (real network, no S3)", () => {
  const shouldRun = process.env.RUN_AEM_INTEGRATION_TEST === "1";
  const t = shouldRun ? test : test.skip;

  t(
    "streams a real asset from AEM OR lists assets under a DAM_PATH",
    async () => {
      if (!process.env.AEM_BEARER_TOKEN) throw new Error("Missing AEM_BEARER_TOKEN");

      const csvPath =
        process.env.ASSETS_CSV_PATH ||
        path.join(__dirname, "fixtures", "assets.csv");

      if (!fs.existsSync(csvPath)) throw new Error(`CSV not found: ${csvPath}`);

      const rows = await readCSV(csvPath);
      if (!rows.length) throw new Error(`CSV has no rows: ${csvPath}`);

      const authorCol = findAuthorLinkColumn(rows[0]);
      const damCol = findDamPathColumn(rows[0]);

      if (!authorCol && !damCol) {
        throw new Error('CSV must contain "AUTHOR LINK" or "DAM_PATH/CONTENT_PATH".');
      }

      const firstRow = rows.find((r) => {
        const a = authorCol ? String(r[authorCol] || "").trim() : "";
        const d = damCol ? String(r[damCol] || "").trim() : "";
        return a || d;
      });

      if (!firstRow) throw new Error("No usable row found.");

      const authorLink = authorCol ? String(firstRow[authorCol] || "").trim() : "";
      const damPath = damCol ? String(firstRow[damCol] || "").trim() : "";

      if (damPath) {
        if (!process.env.AEM_BASE_URL) throw new Error("Missing AEM_BASE_URL for DAM_PATH listing");

        const { assets } = await listAssetsUnderDamPath({ damPath });
        expect(assets.length).toBeGreaterThan(0);

        // Stream first asset found
        const firstAsset = assets[0];
        const { stream } = await getAemStream(firstAsset.downloadUrl);
        const buf = await readFirstBytes(stream, 128 * 1024);
        expect(buf.length).toBeGreaterThan(0);
        return;
      }

      // AUTHOR LINK mode
      const { stream } = await getAemStream(authorLink);
      const buf = await readFirstBytes(stream, 128 * 1024);
      expect(buf.length).toBeGreaterThan(0);
    },
    120000
  );
});
