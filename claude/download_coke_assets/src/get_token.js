#!/usr/bin/env node
/**
 * Generate AEM bearer token from service account credentials.
 * Reads: ../creds/service_account.json
 * Writes: ../bearer_token.txt
 *
 * Usage: node src/get_token.js
 */

const jwt = require("jsonwebtoken");
const https = require("https");
const querystring = require("querystring");
const path = require("path");
const fs = require("fs");

const ROOT = path.resolve(__dirname, "..");
const credsPath = path.join(ROOT, "creds", "service_account.json");
const tokenPath = path.join(ROOT, "bearer_token.txt");

if (!fs.existsSync(credsPath)) {
  console.error(`Missing service account file: ${credsPath}`);
  console.error("Copy Firefly_Foundry_AEM_PROD.json to creds/service_account.json");
  process.exit(1);
}

const creds = require(credsPath).integration;

const IMS = creds.imsEndpoint;
const ORG = creds.org;
const TECH_ACCT = creds.id;
const CLIENT_ID = creds.technicalAccount.clientId;
const CLIENT_SECRET = creds.technicalAccount.clientSecret;
const PRIVATE_KEY = creds.privateKey;
const META_SCOPE = creds.metascopes;

// Build JWT payload
const payload = {
  exp: Math.floor(Date.now() / 1000) + 86400, // 24h
  iss: ORG,
  sub: TECH_ACCT,
  aud: `https://${IMS}/c/${CLIENT_ID}`,
  [`https://${IMS}/s/${META_SCOPE}`]: true,
};

// Sign JWT
const token = jwt.sign(payload, PRIVATE_KEY, { algorithm: "RS256" });
console.log("JWT generated successfully");

// Exchange JWT for access token
const postData = querystring.stringify({
  client_id: CLIENT_ID,
  client_secret: CLIENT_SECRET,
  jwt_token: token,
});

const options = {
  hostname: IMS,
  path: "/ims/exchange/jwt/",
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": Buffer.byteLength(postData),
  },
};

const req = https.request(options, (res) => {
  let data = "";
  res.on("data", (chunk) => (data += chunk));
  res.on("end", () => {
    try {
      const parsed = JSON.parse(data);
      if (parsed.access_token) {
        console.log("Access token obtained!");
        console.log("Expires in:", Math.round(parsed.expires_in / 1000 / 3600), "hours");
        fs.writeFileSync(tokenPath, parsed.access_token);
        console.log(`Token saved to ${tokenPath}`);
      } else {
        console.error("Error response:", data);
        process.exit(1);
      }
    } catch (e) {
      console.error("Failed to parse response:", data);
      process.exit(1);
    }
  });
});

req.on("error", (e) => {
  console.error("Request error:", e.message);
  process.exit(1);
});
req.write(postData);
req.end();
