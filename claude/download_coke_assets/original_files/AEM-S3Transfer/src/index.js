require("dotenv").config();

const fs = require("fs");
const { logger } = require("./logger");

const { readCSV, findAuthorLinkColumn, findDamPathColumn } = require("./csv");
const { getAemStream } = require("./aem");
const { listAssetsUnderDamPath } = require("./aemAssetsApi");
const { streamZipEntries } = require("./zipPipeline");
const {
  retry,
  withTimeout,
  filenameFromUrl,
  stripExtension,
  buildKey,
  splitRelPath
} = require("./utils");
const { getS3ConfigFromEnv, createS3Client, uploadStreamToS3 } = require("./s3Uploader");

// Global handlers to prevent silent failures
process.on("unhandledRejection", (reason) => {
  logger.error("Unhandled promise rejection.", { reason: String(reason) });
  process.exitCode = 1;
});

process.on("uncaughtException", (err) => {
  logger.error("Uncaught exception.", { message: err.message, stack: err.stack });
  process.exit(1);
});

process.on("SIGTERM", () => {
  logger.error("Received SIGTERM. Exiting.");
  process.exit(1);
});

process.on("SIGINT", () => {
  logger.error("Received SIGINT. Exiting.");
  process.exit(1);
});

function looksLikeZipByNameOrType(sourceName, contentType) {
  const name = String(sourceName || "").toLowerCase();
  if (name.endsWith(".zip")) return true;
  if (String(contentType || "").toLowerCase().includes("zip")) return true;
  return false;
}

// Idle timeout: if no data arrives for idleMs, destroy stream
function withIdleTimeout(readable, idleMs, label) {
  if (!idleMs || idleMs <= 0) return readable;

  let timer = null;

  const reset = () => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      logger.error("Stream idle timeout reached. Aborting stream.", { idleMs, label });
      try {
        readable.destroy(new Error(`Idle timeout: ${label}`));
      } catch {
        // ignore
      }
    }, idleMs);
  };

  reset();

  readable.on("data", reset);
  readable.on("end", () => timer && clearTimeout(timer));
  readable.on("close", () => timer && clearTimeout(timer));
  readable.on("error", () => timer && clearTimeout(timer));

  return readable;
}

// Only used in DEBUG mode
function attachProgressLogging(stream, totalBytes, label) {
  if (logger.level !== "debug") return;

  let read = 0;
  const start = Date.now();
  let lastLog = 0;

  stream.on("data", (chunk) => {
    read += chunk.length;
    const now = Date.now();
    if (now - lastLog > 5000) {
      const secs = Math.max(1, (now - start) / 1000);
      const mb = (read / (1024 * 1024)).toFixed(2);
      const rate = (read / (1024 * 1024) / secs).toFixed(2);
      const pct = totalBytes ? ((read / totalBytes) * 100).toFixed(1) : null;

      if (pct) {
        logger.debug("Download progress.", { file: label, mbRead: mb, pct, mbPerSec: rate });
      } else {
        logger.debug("Download progress.", { file: label, mbRead: mb, mbPerSec: rate });
      }

      lastLog = now;
    }
  });

  stream.on("end", () => logger.debug("Download completed.", { file: label }));
  stream.on("error", (e) => logger.warn("Download stream emitted an error.", { file: label, message: e.message }));
}

async function processSingleAssetUrl({ s3, bucket, basePrefixKey, assetUrl, failures, context }) {
  const IDLE_TIMEOUT_MS = Number(process.env.AEM_IDLE_TIMEOUT_MS || 600000);
  const UPLOAD_TIMEOUT_MS = Number(process.env.S3_UPLOAD_TIMEOUT_MS || 3600000);
  const AEM_RETRIES = Number(process.env.AEM_RETRIES || 3);

  const fileName = filenameFromUrl(assetUrl);

  const label = context?.relPath ? `${context.relPath}` : fileName;
  logger.info("Processing asset.", { label, url: logger.level === "debug" ? assetUrl : undefined });

  return retry(
    async () => {
      const { stream, contentType, contentLength } = await getAemStream(assetUrl);

      // Ensure we never hang on dead streams
      const guarded = withIdleTimeout(stream, IDLE_TIMEOUT_MS, assetUrl);

      // Log stream-level aborts/errors (these often show "aborted")
      guarded.on("error", (err) => {
        logger.warn("AEM stream error.", { file: fileName, message: err.message });
      });

      attachProgressLogging(guarded, contentLength, fileName);

      const isZip = looksLikeZipByNameOrType(fileName, contentType);

      if (!isZip) {
        const key = buildKey(basePrefixKey, fileName);
        logger.info("Uploading file to S3.", { key });

        await withTimeout(
          uploadStreamToS3({
            s3,
            bucket,
            key,
            bodyStream: guarded,
            contentType
          }),
          UPLOAD_TIMEOUT_MS,
          `S3 upload ${key}`
        );

        logger.info("Upload completed.", { key });
        return;
      }

      const zipBase = stripExtension(fileName) || "zip";
      logger.info("ZIP detected. Uploading extracted contents.", { zipBase });

      await streamZipEntries({
        zipStream: guarded,
        prefix: basePrefixKey,
        zipBase,
        uploadFn: async (entryStream, key) => {
          await withTimeout(
            uploadStreamToS3({ s3, bucket, key, bodyStream: entryStream }),
            UPLOAD_TIMEOUT_MS,
            `S3 upload ${key}`
          );

          if (logger.level === "debug") {
            logger.debug("Uploaded ZIP entry.", { key });
          }
        },
        onError: (err, ctx2) => {
          failures.push({
            level: "zip-inner-file",
            ...context,
            assetUrl,
            entryPath: ctx2.entryPath,
            key: ctx2.key,
            reason: err.message
          });
          logger.warn("ZIP entry upload failed.", { key: ctx2.key, message: err.message });
        }
      });

      logger.info("ZIP processing completed.", { file: fileName });
    },
    { retries: AEM_RETRIES, label: `AEM download for ${fileName}` }
  );
}

async function main() {
  const csvPath = process.argv[2];
  if (!csvPath) {
    logger.error("Missing CSV path. Usage: node src/index.js ./assets.csv");
    process.exit(1);
  }
  if (!fs.existsSync(csvPath)) {
    logger.error("CSV file not found.", { csvPath });
    process.exit(1);
  }

  logger.info("Starting uploader.", { logLevel: logger.level });

  const { region, bucket, prefix } = getS3ConfigFromEnv();
  const s3 = createS3Client(region);

  logger.info("Reading CSV.", { csvPath });
  const rows = await readCSV(csvPath);
  logger.info("CSV loaded.", { rows: rows.length });

  const failures = [];

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];

    const authorCol = findAuthorLinkColumn(row);
    const damCol = findDamPathColumn(row);

    const authorLink = authorCol ? String(row[authorCol] || "").trim() : "";
    const damPath = damCol ? String(row[damCol] || "").trim() : "";

    if (!authorCol && !damCol) {
      failures.push({
        level: "row",
        rowIndex: i,
        reason: 'Row has neither "AUTHOR LINK" nor "DAM_PATH/CONTENT_PATH".'
      });
      logger.warn("Skipping row: required columns not found.", { rowIndex: i });
      continue;
    }

    // Prefer DAM_PATH mode when present
    if (damPath) {
      logger.info("Processing DAM path row.", { rowIndex: i, damPath });

      try {
        const { damRootName, assets, mode } = await listAssetsUnderDamPath({ damPath });
        logger.info("DAM listing completed.", { rowIndex: i, mode, assets: assets.length });

        for (let j = 0; j < assets.length; j++) {
          const { downloadUrl, relPath } = assets[j];
          const { dir } = splitRelPath(relPath);

          const basePrefixKey = buildKey(prefix, damRootName, dir);

          try {
            logger.info("Starting asset from DAM listing.", {
              rowIndex: i,
              index: j + 1,
              total: assets.length,
              relPath
            });

            await processSingleAssetUrl({
              s3,
              bucket,
              basePrefixKey,
              assetUrl: downloadUrl,
              failures,
              context: { rowIndex: i, damPath, relPath }
            });
          } catch (errAsset) {
            failures.push({
              level: "asset",
              rowIndex: i,
              damPath,
              relPath,
              downloadUrl,
              reason: errAsset.message
            });
            logger.error("Asset failed.", { relPath, message: errAsset.message });
          }
        }
      } catch (err) {
        failures.push({
          level: "dam-path",
          rowIndex: i,
          damPath,
          reason: err.message
        });
        logger.error("DAM path listing failed.", { rowIndex: i, damPath, message: err.message });
      }

      continue;
    }

    // AUTHOR LINK mode
    if (authorLink) {
      logger.info("Processing AUTHOR LINK row.", { rowIndex: i });

      try {
        const basePrefixKey = buildKey(prefix);
        await processSingleAssetUrl({
          s3,
          bucket,
          basePrefixKey,
          assetUrl: authorLink,
          failures,
          context: { rowIndex: i }
        });
      } catch (err) {
        failures.push({
          level: "row",
          rowIndex: i,
          authorLink,
          reason: err.message
        });
        logger.error("AUTHOR LINK row failed.", { rowIndex: i, message: err.message });
      }
    } else {
      failures.push({ level: "row", rowIndex: i, reason: "Empty AUTHOR LINK and no DAM_PATH" });
      logger.warn("Skipping row: empty AUTHOR LINK and no DAM_PATH.", { rowIndex: i });
    }
  }

  logger.info("Run complete.", { failures: failures.length });

  if (failures.length) {
    // Always print failures clearly
    console.log(JSON.stringify(failures, null, 2));
    process.exitCode = 2;
  } else {
    logger.info("All uploads succeeded.");
  }
}

main().catch((e) => {
  logger.error("Fatal error in main.", { message: e.message, stack: e.stack });
  process.exit(1);
});
