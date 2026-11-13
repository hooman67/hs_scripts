/**
 * aem-authorlink-stream-to-s3.js
 * Usage: node aem-authorlink-stream-to-s3.js ./assets.csv
 *
 * CSV can have any columns, but must include "AUTHOR LINK" (case-insensitive).
 * Streams downloads from AEM, streams ZIP extraction, uploads to S3 with no local disk writes.
 */

require("dotenv").config();
const fs = require("fs");
const path = require("path");
const axios = require("axios");
const { parse } = require("csv-parse");
const unzipper = require("unzipper");

const { S3Client } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");

// -------------------- ENV --------------------

function requireEnv(name) {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env var: ${name}`);
  return v;
}

const AEM_BEARER_TOKEN = requireEnv("AEM_BEARER_TOKEN");
const AWS_REGION = requireEnv("AWS_REGION");
const S3_BUCKET = requireEnv("S3_BUCKET");
const S3_PREFIX = (process.env.S3_PREFIX || "").trim().replace(/^\/+|\/+$/g, "");

const s3 = new S3Client({ region: AWS_REGION });

// -------------------- HELPERS --------------------

function normalizePosix(p) {
  return String(p).split(path.sep).join("/");
}

function filenameFromUrl(url) {
  const clean = String(url).split("?")[0];
  return clean.split("/").pop() || "asset";
}

function stripExtension(name) {
  return name.replace(/\.[^/.]+$/, "");
}

function buildS3Key(...parts) {
  const cleaned = parts
    .filter(Boolean)
    .map((p) => String(p).replace(/^\/+|\/+$/g, ""))
    .filter(Boolean);
  return cleaned.join("/").replace(/\/+/g, "/");
}

/**
 * Prevent zip-slip and weird paths:
 * - remove drive letters
 * - remove leading slashes
 * - remove ../ segments
 */
function sanitizeZipEntryPath(p) {
  let s = normalizePosix(p).replace(/^[A-Za-z]:/, ""); // strip "C:"
  s = s.replace(/^\/+/, ""); // no leading "/"
  // remove any ../ or ./ segments safely
  const parts = s.split("/").filter((seg) => seg && seg !== "." && seg !== "..");
  return parts.join("/");
}

async function uploadStreamToS3(bodyStream, key, contentType) {
  const uploader = new Upload({
    client: s3,
    params: {
      Bucket: S3_BUCKET,
      Key: key,
      Body: bodyStream,
      ...(contentType ? { ContentType: contentType } : {}),
    },
    queueSize: 4,
    partSize: 10 * 1024 * 1024, // 10MB parts for multipart uploads
    leavePartsOnError: false,
  });

  await uploader.done();
}

// -------------------- CSV --------------------

function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const rows = [];
    fs.createReadStream(filePath)
      .pipe(
        parse({
          columns: true,
          trim: true,
          skip_empty_lines: true,
        })
      )
      .on("data", (r) => rows.push(r))
      .on("end", () => resolve(rows))
      .on("error", reject);
  });
}

function findAuthorLinkField(row) {
  // Case-insensitive match for "AUTHOR LINK" (handles extra spaces)
  const keys = Object.keys(row);
  const match = keys.find(
    (k) => k && k.toString().trim().toLowerCase() === "author link"
  );
  return match || null;
}

// -------------------- AEM STREAMING --------------------

async function getAemStream(url) {
  // NOTE: axios response.data will be a Node stream
  const res = await axios.get(url, {
    responseType: "stream",
    headers: {
      Authorization: `Bearer ${AEM_BEARER_TOKEN}`,
    },
    maxContentLength: Infinity,
    maxBodyLength: Infinity,
    validateStatus: (s) => s >= 200 && s < 300,
  });

  const contentType = res.headers["content-type"] || "";
  return { stream: res.data, contentType };
}

function looksLikeZipByNameOrType(url, contentType) {
  const name = filenameFromUrl(url).toLowerCase();
  if (name.endsWith(".zip")) return true;
  if (String(contentType).toLowerCase().includes("zip")) return true;
  return false;
}

// -------------------- PIPELINES --------------------

async function processNonZipToS3(authorLink) {
  const fileName = filenameFromUrl(authorLink);
  const { stream, contentType } = await getAemStream(authorLink);

  const key = buildS3Key(S3_PREFIX, fileName);
  await uploadStreamToS3(stream, key, contentType);
  return { uploaded: [{ key }] };
}

async function processZipStreamToS3(authorLink, failuresForRow) {
  const zipFileName = filenameFromUrl(authorLink);
  const zipBase = stripExtension(zipFileName) || "zip";

  const { stream } = await getAemStream(authorLink);

  const uploaded = [];
  const parser = stream.pipe(unzipper.Parse({ forceStream: true }));

  for await (const entry of parser) {
    const entryPathRaw = entry.path || entry.props?.path || "";
    const entryPath = sanitizeZipEntryPath(entryPathRaw);

    if (entry.type !== "File") {
      entry.autodrain();
      continue;
    }

    if (!entryPath) {
      // unnamed entry; drain it
      entry.autodrain();
      continue;
    }

    // Put zip contents under a folder named after the zip file (recommended)
    const key = buildS3Key(S3_PREFIX, zipBase, entryPath);

    try {
      // Upload entry stream directly to S3
      await uploadStreamToS3(entry, key);
      uploaded.push({ key });
    } catch (err) {
      failuresForRow.push({
        level: "zip-inner-file",
        authorLink,
        zipFileName,
        entryPath,
        key,
        reason: err.message,
      });

      // Important: drain the entry stream so the parser can continue
      try {
        entry.autodrain();
      } catch {}
    }
  }

  return { uploaded };
}

// -------------------- MAIN --------------------

(async () => {
  const csvPath = process.argv[2];
  if (!csvPath) {
    console.error("Usage: node aem-authorlink-stream-to-s3.js ./assets.csv");
    process.exit(1);
  }
  if (!fs.existsSync(csvPath)) {
    console.error("CSV not found:", csvPath);
    process.exit(1);
  }

  const failures = [];

  console.log("Reading CSV...");
  const rows = await readCSV(csvPath);
  console.log(`Loaded ${rows.length} row(s).`);

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const authorKey = findAuthorLinkField(row);

    if (!authorKey) {
      failures.push({
        level: "row",
        rowIndex: i,
        reason: 'CSV missing required column "AUTHOR LINK" (case-insensitive).',
      });
      console.error(`\n[${i + 1}/${rows.length}] ❌ Missing AUTHOR LINK column`);
      break; // no point continuing
    }

    const authorLink = String(row[authorKey] || "").trim();
    console.log(`\n[${i + 1}/${rows.length}] AUTHOR LINK: ${authorLink}`);

    if (!authorLink) {
      failures.push({ level: "row", rowIndex: i, reason: "Empty AUTHOR LINK cell" });
      console.error("  ❌ Empty AUTHOR LINK");
      continue;
    }

    const failuresForRow = [];

    try {
      // Peek content-type with a streaming GET (already needed) and decide if zip.
      // We’ll do one request only by streaming once; so we decide based on name first if possible.
      // If name says zip, go zip path. Otherwise we’ll do a lightweight header-based guess:
      // (We avoid doing 2 HTTP requests per row.)
      //
      // Strategy:
      // - If URL ends with .zip → treat as zip
      // - Else start a stream + look at content-type from response headers (we need headers anyway)
      //
      // To avoid downloading twice, we do a small "header fetch" by calling getAemStream and
      // then route the returned stream accordingly. For zip, we pass that stream into unzipper.
      // For non-zip, we upload that stream directly.
      const fileName = filenameFromUrl(authorLink).toLowerCase();
      const isZipByName = fileName.endsWith(".zip");

      if (isZipByName) {
        console.log("  Detected ZIP by filename. Streaming unzip → S3...");
        await processZipStreamToS3(authorLink, failuresForRow);
      } else {
        // We need the content-type to decide; do one streaming request,
        // and if it looks like zip we unzip, else upload as file.
        const { stream, contentType } = await getAemStream(authorLink);

        if (looksLikeZipByNameOrType(authorLink, contentType)) {
          console.log("  Detected ZIP by content-type. Streaming unzip → S3...");
          const parser = stream.pipe(unzipper.Parse({ forceStream: true }));
          const zipBase = stripExtension(filenameFromUrl(authorLink)) || "zip";

          for await (const entry of parser) {
            const entryPath = sanitizeZipEntryPath(entry.path || "");
            if (entry.type !== "File") {
              entry.autodrain();
              continue;
            }
            if (!entryPath) {
              entry.autodrain();
              continue;
            }

            const key = buildS3Key(S3_PREFIX, zipBase, entryPath);
            try {
              await uploadStreamToS3(entry, key);
            } catch (err) {
              failuresForRow.push({
                level: "zip-inner-file",
                rowIndex: i,
                authorLink,
                entryPath,
                key,
                reason: err.message,
              });
              try {
                entry.autodrain();
              } catch {}
            }
          }
        } else {
          console.log("  Detected non-zip. Streaming upload → S3...");
          const key = buildS3Key(S3_PREFIX, filenameFromUrl(authorLink));
          await uploadStreamToS3(stream, key, contentType);
        }
      }
    } catch (err) {
      failuresForRow.push({
        level: "row",
        rowIndex: i,
        authorLink,
        reason: err.message,
      });
      console.error("  ❌ Failed:", err.message);
      if (err.response?.status) console.error("  Status:", err.response.status);
    }

    failures.push(...failuresForRow);
  }

  console.log("\n==============================");
  console.log("Done.");
  console.log(`Rows processed: ${rows.length}`);
  console.log(`Failures:       ${failures.length}`);
  if (failures.length) {
    console.log("\nFailures (JSON):");
    console.log(JSON.stringify(failures, null, 2));
    process.exitCode = 2;
  } else {
    console.log("All uploads succeeded 🎉");
  }
})();

