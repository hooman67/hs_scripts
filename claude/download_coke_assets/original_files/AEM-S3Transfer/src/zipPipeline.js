const path = require("path");
const unzipper = require("unzipper");
const { buildKey } = require("./utils");

function sanitizeZipEntryPath(p) {
  let s = String(p).split(path.sep).join("/").replace(/^[A-Za-z]:/, "");
  s = s.replace(/^\/+/, "");
  const parts = s.split("/").filter((seg) => seg && seg !== "." && seg !== "..");
  return parts.join("/");
}

async function streamZipEntries({ zipStream, prefix = "", zipBase = "zip", uploadFn, onError }) {
  const parser = zipStream.pipe(unzipper.Parse({ forceStream: true }));

  for await (const entry of parser) {
    const entryPath = sanitizeZipEntryPath(entry.path || "");

    if (entry.type !== "File" || !entryPath) {
      entry.autodrain();
      continue;
    }

    const key = buildKey(prefix, zipBase, entryPath);

    try {
      await uploadFn(entry, key);
    } catch (err) {
      if (onError) onError(err, { entryPath, key });
      try {
        entry.autodrain();
      } catch {
        // ignore
      }
    }
  }
}

module.exports = { streamZipEntries };
