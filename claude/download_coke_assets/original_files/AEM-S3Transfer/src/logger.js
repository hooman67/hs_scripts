function nowIso() {
    return new Date().toISOString();
  }
  
  // Levels: error < warn < info < debug
  const LEVELS = { error: 0, warn: 1, info: 2, debug: 3 };
  
  function resolveLevel() {
    if (process.env.DEBUG === "1" || process.env.DEBUG === "true") return "debug";
    const ll = String(process.env.LOG_LEVEL || "").trim().toLowerCase();
    if (ll && LEVELS[ll] !== undefined) return ll;
    return "info";
  }
  
  const CURRENT_LEVEL = resolveLevel();
  
  function shouldLog(level) {
    return LEVELS[level] <= LEVELS[CURRENT_LEVEL];
  }
  
  function formatLine(level, message, meta) {
    const base = `${nowIso()} ${level.toUpperCase()}: ${message}`;
    if (!meta) return base;
    try {
      const m = typeof meta === "string" ? meta : JSON.stringify(meta);
      return `${base} ${m}`;
    } catch {
      return base;
    }
  }
  
  const logger = {
    level: CURRENT_LEVEL,
    debug(message, meta) {
      if (shouldLog("debug")) console.log(formatLine("debug", message, meta));
    },
    info(message, meta) {
      if (shouldLog("info")) console.log(formatLine("info", message, meta));
    },
    warn(message, meta) {
      if (shouldLog("warn")) console.warn(formatLine("warn", message, meta));
    },
    error(message, meta) {
      if (shouldLog("error")) console.error(formatLine("error", message, meta));
    }
  };
  
  module.exports = { logger };
  