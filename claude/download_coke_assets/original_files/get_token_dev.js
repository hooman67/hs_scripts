const jwt = require("jsonwebtoken");
const https = require("https");
const querystring = require("querystring");

const creds = require("./Firefly_Foundry_AEM_PROD.json").integration;

const IMS = creds.imsEndpoint; // ims-na1.adobelogin.com
const ORG = creds.org;
const TECH_ACCT = creds.id;
const CLIENT_ID = creds.technicalAccount.clientId;
const CLIENT_SECRET = creds.technicalAccount.clientSecret;
const PRIVATE_KEY = creds.privateKey;
const META_SCOPE = creds.metascopes; // ent_aem_cloud_api

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
        console.log("Access token obtained successfully!");
        console.log("Token (first 50 chars):", parsed.access_token.substring(0, 50) + "...");
        console.log("Expires in:", parsed.expires_in, "ms");
        // Write token to file for use by other scripts
        require("fs").writeFileSync(
          "./bearer_token.txt",
          parsed.access_token
        );
        console.log("Token saved to bearer_token.txt");
      } else {
        console.error("Error response:", data);
      }
    } catch (e) {
      console.error("Failed to parse response:", data);
    }
  });
});

req.on("error", (e) => console.error("Request error:", e.message));
req.write(postData);
req.end();
