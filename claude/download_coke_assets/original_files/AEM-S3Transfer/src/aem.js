const axios = require("axios");
const http = require("http");
const https = require("https");
const { requireEnv } = require("./utils");
const { logger } = require("./logger");

const httpAgent = new http.Agent({ keepAlive: true, maxSockets: 10 });
const httpsAgent = new https.Agent({ keepAlive: true, maxSockets: 10 });

async function getAemStream(url) {
  const token = requireEnv("AEM_BEARER_TOKEN");
  const REQUEST_TIMEOUT_MS = Number(process.env.AEM_REQUEST_TIMEOUT_MS ?? 0);

  logger.debug("Requesting asset stream from AEM.", { url });

  const res = await axios.get(url, {
    responseType: "stream",
    headers: { Authorization: `Bearer ${token}` },
    maxContentLength: Infinity,
    maxBodyLength: Infinity,
    //timeout: REQUEST_TIMEOUT_MS > 0 ? REQUEST_TIMEOUT_MS : 0, // 0 disables axios total timeout
    //httpAgent,
   // httpsAgent,
    validateStatus: (s) => s >= 200 && s < 300
  });

  return {
    stream: res.data,
    contentType: res.headers["content-type"] || "",
    contentLength: Number(res.headers["content-length"] || 0) || 0
  };
}

module.exports = { getAemStream };
