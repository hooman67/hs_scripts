#!/usr/bin/env node
/**
 * Download the 22 3D assets found in the TCCC DAM and upload to S3.
 * Target: s3://foundry-tccc-enterprise-adobe-assets/3D_assets_from_DAM/
 */

const axios = require("axios");
const { S3Client } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AEM_BASE = "https://author-p64403-e609778.adobeaemcloud.com";
const AEM_TOKEN = fs.readFileSync(path.join(ROOT, "bearer_token.txt"), "utf8").trim();

const S3_BUCKET = "foundry-tccc-enterprise-adobe-assets";
const S3_PREFIX = "3D_assets_from_DAM";
const AWS_REGION = "us-west-2";

const s3 = new S3Client({ region: AWS_REGION });

// All 22 3D assets found in the DAM
const ASSETS = [
  // FBX - "One Coke Away" campaign characters
  "/content/dam/tccc/marketing/coca-cola/one-coke-away-from-each-other/none/hero_elf.fbx",
  "/content/dam/tccc/marketing/coca-cola/one-coke-away-from-each-other/none/hero_orc.fbx",
  // GLB
  "/content/dam/tccc/marketing/none/none/none/2020/10/moj.glb",
  // C4D - Diet Coke can + multipack animations
  "/content/dam/tccc/marketing/coca-cola-light-diet-coke/none/base/2020/08/dc_can_octane.c4d",
  "/content/dam/tccc/marketing/coca-cola-light-diet-coke/none/none/2020/01/multipack_3flavours_1x1-folder/extractedZipsFolder/Multipack_3Flavours_1x1 folder/(Footage)/Assets/C4D/CokeLight_Final_Animation_NullForAE_Import.c4d",
  "/content/dam/tccc/marketing/coca-cola-light-diet-coke/none/none/2020/01/multipack_3flavours_9x16-folder/extractedZipsFolder/Multipack_3Flavours_9x16 folder/(Footage)/Assets/C4D/CokeLight_Final_Animation_NullForAE_Import.c4d",
  "/content/dam/tccc/marketing/coca-cola-light-diet-coke/none/none/2020/01/multipack_4flavours_9x16-folder/extractedZipsFolder/Multipack_4Flavours_9x16 folder/(Footage)/Assets/C4D/CokeLight_Final_Animation_NullForAE_Import.c4d",
  "/content/dam/tccc/marketing/coca-cola-light-diet-coke/none/none/multipack_4flavours_1x1-folder/extractedZipsFolder/Multipack_4Flavours_1x1 folder/(Footage)/Assets/C4D/CokeLight_Final_Animation_NullForAE_Import.c4d",
  // Maya Binary - Heritage center product models + characters
  "/content/dam/tccc/heritage-center/coca-cola/component-graphic-elements/2015/bottle.mb",
  "/content/dam/tccc/heritage-center/coca-cola/component-graphic-elements/2015/global_bottle_rig.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_coke_bottle_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_coke_glass_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_coke_lid_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_female_wave_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_flower_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_male_head_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_male_kiss_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_male_pose_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_male_recline_geo.mb",
  "/content/dam/tccc/heritage-center/coca-cola/tvcs/2015/ccl_monster_geo.mb",
  // Alembic - Coca-Cola Energy 3D passes
  "/content/dam/tccc/marketing/coca-cola-energy/none/none/3d-passes-cinemascope/extractedZipsFolder/3D Passes - CINEMASCOPE/Shot_010-2/Alembics/Coke_Shot_010_Cam_v018_baked.abc",
  "/content/dam/tccc/marketing/coca-cola-energy/none/none/3d-passes-cinemascope/extractedZipsFolder/3D Passes - CINEMASCOPE/Shot_010-2/Alembics/Coke_Shot_010_Can_v017.abc",
];

// Group mapping for nice folder structure on S3
function getS3Key(damPath) {
  const name = damPath.split("/").pop();
  const ext = name.split(".").pop().toLowerCase();

  if (damPath.includes("heritage-center") && damPath.includes("component-graphic-elements"))
    return `${S3_PREFIX}/maya_product_models/${name}`;
  if (damPath.includes("heritage-center") && damPath.includes("tvcs"))
    return `${S3_PREFIX}/maya_tvc_models/${name}`;
  if (damPath.includes("one-coke-away"))
    return `${S3_PREFIX}/fbx_campaign_characters/${name}`;
  if (damPath.includes("coca-cola-light-diet-coke") && ext === "c4d") {
    // Disambiguate the duplicate names
    if (damPath.includes("dc_can_octane")) return `${S3_PREFIX}/c4d_diet_coke/${name}`;
    if (damPath.includes("3flavours_1x1")) return `${S3_PREFIX}/c4d_diet_coke/multipack_3flavours_1x1.c4d`;
    if (damPath.includes("3flavours_9x16")) return `${S3_PREFIX}/c4d_diet_coke/multipack_3flavours_9x16.c4d`;
    if (damPath.includes("4flavours_9x16")) return `${S3_PREFIX}/c4d_diet_coke/multipack_4flavours_9x16.c4d`;
    if (damPath.includes("4flavours_1x1")) return `${S3_PREFIX}/c4d_diet_coke/multipack_4flavours_1x1.c4d`;
    return `${S3_PREFIX}/c4d_diet_coke/${name}`;
  }
  if (ext === "abc")
    return `${S3_PREFIX}/alembic_energy_passes/${name}`;
  if (ext === "glb")
    return `${S3_PREFIX}/glb/${name}`;

  return `${S3_PREFIX}/other/${name}`;
}

let uploaded = 0, failed = 0;

async function downloadAndUpload(damPath) {
  const s3Key = getS3Key(damPath);
  const name = damPath.split("/").pop();

  try {
    const resp = await axios.get(`${AEM_BASE}${damPath}`, {
      headers: { Authorization: `Bearer ${AEM_TOKEN}` },
      responseType: "stream",
      maxContentLength: Infinity,
      timeout: 120000,
    });

    const contentType = resp.headers["content-type"] || "application/octet-stream";
    const contentLength = parseInt(resp.headers["content-length"] || "0", 10);

    const uploader = new Upload({
      client: s3,
      params: { Bucket: S3_BUCKET, Key: s3Key, Body: resp.data, ContentType: contentType },
      queueSize: 4,
      partSize: 10 * 1024 * 1024,
    });

    await uploader.done();
    uploaded++;
    const sizeMB = contentLength ? ` (${(contentLength / 1024 / 1024).toFixed(1)}MB)` : "";
    console.log(`  ✓ [${uploaded}/${ASSETS.length}] ${name}${sizeMB} → ${s3Key}`);
    return { name, s3Key, size: contentLength, damPath };
  } catch (err) {
    failed++;
    const reason = err.response?.status ? `HTTP ${err.response.status}` : err.message;
    console.error(`  ✗ ${name}: ${reason}`);
    return null;
  }
}

async function main() {
  console.log(`\n🔽 Downloading ${ASSETS.length} 3D assets from AEM → S3`);
  console.log(`   Target: s3://${S3_BUCKET}/${S3_PREFIX}/\n`);

  const results = [];
  // Download 5 at a time
  for (let i = 0; i < ASSETS.length; i += 5) {
    const batch = ASSETS.slice(i, i + 5);
    const batchResults = await Promise.all(batch.map(downloadAndUpload));
    results.push(...batchResults.filter(Boolean));
  }

  console.log(`\n✅ Done: ${uploaded} uploaded, ${failed} failed`);

  // Save manifest for gallery
  const manifest = results.map(r => ({
    name: r.name,
    s3Key: r.s3Key,
    size: r.size,
    damPath: r.damPath,
    folder: r.s3Key.split("/").slice(1, -1).join("/"),
  }));
  const manifestPath = path.join(ROOT, "3d_asset_manifest.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`   Manifest: ${manifestPath}`);
}

main().catch(err => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
