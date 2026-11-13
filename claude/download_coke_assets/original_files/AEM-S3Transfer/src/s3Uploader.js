const { S3Client } = require("@aws-sdk/client-s3");
const { Upload } = require("@aws-sdk/lib-storage");
const { requireEnv } = require("./utils");

function getS3ConfigFromEnv() {
  const region = requireEnv("AWS_REGION");
  const bucket = requireEnv("S3_BUCKET");
  const prefix = (process.env.S3_PREFIX || "").trim().replace(/^\/+|\/+$/g, "");
  return { region, bucket, prefix };
}

function createS3Client(region) {
  return new S3Client({ region });
}

async function uploadStreamToS3({ s3, bucket, key, bodyStream, contentType }) {
  const uploader = new Upload({
    client: s3,
    params: {
      Bucket: bucket,
      Key: key,
      Body: bodyStream,
      ...(contentType ? { ContentType: contentType } : {})
    },
    queueSize: 4,
    partSize: 10 * 1024 * 1024,
    leavePartsOnError: false
  });

  await uploader.done();
}

module.exports = { getS3ConfigFromEnv, createS3Client, uploadStreamToS3 };
