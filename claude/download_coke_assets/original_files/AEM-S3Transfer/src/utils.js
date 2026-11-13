const { logger } = require("./logger");

function requireEnv(name) {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env var: ${name}`);
  return v;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function withTimeout(promise, ms, label) {
  if (!ms || ms <= 0) return promise;

  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error(`Timeout after ${ms}ms: ${label}`)), ms)
    )
  ]);
}

function isRetryableError(err) {
  const msg = String(err?.message || "").toLowerCase();

  return (
    msg.includes("aborted") ||
    msg.includes("econnreset") ||
    msg.includes("etimedout") ||
    msg.includes("socket hang up") ||
    msg.includes("timeout") ||
    msg.includes("network") ||
    msg.includes("temporarily") ||
    msg.includes("connection")
  );
}

async function retry(fn, { retries = 3, baseDelayMs = 1000, label = "operation" } = {}) {
  let lastErr;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      if (attempt > 0) logger.info(`Retrying ${label} (attempt ${attempt + 1} of ${retries + 1}).`);
      return await fn();
    } catch (err) {
      lastErr = err;

      if (attempt === retries || !isRetryableError(err)) {
        throw err;
      }

      const delay = baseDelayMs * Math.pow(2, attempt);
      logger.warn(`Transient error during ${label}. Will retry after ${delay}ms.`, {
        message: err.message
      });
      await sleep(delay);
    }
  }

  throw lastErr;
}

function filenameFromUrl(url) {
  const clean = String(url).split("?")[0];
  return clean.split("/").pop() || "asset";
}

function stripExtension(name) {
  return name.replace(/\.[^/.]+$/, "");
}

function buildKey(...parts) {
  const cleaned = parts
    .filter(Boolean)
    .map((p) => String(p).replace(/^\/+|\/+$/g, ""))
    .filter(Boolean);
  return cleaned.join("/").replace(/\/+/g, "/");
}

function splitRelPath(relPath) {
  const p = String(relPath || "").replace(/^\/+|\/+$/g, "");
  if (!p) return { dir: "", file: "" };
  const parts = p.split("/");
  const file = parts.pop() || "";
  const dir = parts.join("/");
  return { dir, file };
}

module.exports = {
  requireEnv,
  sleep,
  withTimeout,
  retry,
  filenameFromUrl,
  stripExtension,
  buildKey,
  splitRelPath
};
