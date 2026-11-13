# AEM Author - S3 Streaming Uploader

This project streams assets directly from **Adobe Experience Manager (AEM) Author URLs** and uploads them to **Amazon S3**.

* **ZIP files** are streamed, unzipped **in memory**, and uploaded file-by-file
* **Nested folder structures are preserved**
* **No files are written to disk**
* CSV files may contain any columns — only **`AUTHOR LINK`** is required

---

## Features

* Stream assets directly from AEM (no local downloads)
* Detect ZIP vs non-ZIP automatically
* Unzip ZIP files in memory
* Preserve nested ZIP folder structures
* Upload using S3 multipart streaming
* Continue on individual file failures
* CSV-driven execution
* Unit tests with **no AWS / no S3**
* Optional **real AEM integration test**

---

## Project Structure

```
aem-to-s3-stream/
├─ src/
│  ├─ index.js          # Main runner
│  ├─ csv.js            # CSV parsing utilities
│  ├─ aem.js            # AEM streaming (axios)
│  ├─ zipPipeline.js    # ZIP streaming pipeline (no AWS)
│  └─ s3Uploader.js     # S3 streaming uploader
├─ test/
│  ├─ zipPipeline.test.js        # Unit tests (no AWS)
│  ├─ aem.integration.test.js    # Real AEM streaming test
│  └─ fixtures/
│     └─ assets.csv
├─ package.json
├─ .env.example
└─ README.md
```

---

## CSV Format

Only **one column is required**:

```csv
AUTHOR LINK
https://author.aem.site/content/dam/foo/bar.zip
https://author.aem.site/content/dam/foo/image.psd
```

* Column name matching is **case-insensitive**
* Additional columns are ignored

---

## S3 Output Structure

### Non-ZIP file

```
s3://<bucket>/<prefix>/file.psd
```

### ZIP file

```
s3://<bucket>/<prefix>/<zip-name>/
├── folderA/file1.png
└── folderA/subfolder/file2.psd
```

---

## Installation

```bash
npm install
```

---

## Environment Variables

Create a `.env` file or pass env vars at runtime.

### Required (runtime)

```env
AEM_BEARER_TOKEN=your_aem_access_token
AWS_REGION=us-east-1
S3_BUCKET=my-s3-bucket
```

### Optional

```env
S3_PREFIX=uploads
```

---

## Running the Uploader

```bash
node src/index.js ./assets.csv
```

Example:

```bash
AEM_BEARER_TOKEN=xxx \
AWS_REGION=us-east-1 \
S3_BUCKET=my-bucket \
S3_PREFIX=coke-assets \
node src/index.js ./assets.csv
```


## Real AEM Integration Test (Optional)

This test:

* Uses a **real AEM Author URL**
* Confirms streaming connectivity and auth
* Reads only a small portion of the file
* Does **not** upload to S3

### Enable explicitly

```bash
RUN_AEM_INTEGRATION_TEST=1 \
AEM_BEARER_TOKEN=xxx \
ASSETS_CSV_PATH=/full/path/to/assets.csv \
npx jest test/aem.integration.test.js
```

> The test is skipped unless `RUN_AEM_INTEGRATION_TEST=1` is set.

---

## Security Notes

* ZIP paths are sanitized to prevent path traversal
* Streams are never written to disk
* ZIP extraction occurs fully in memory
* Multipart uploads prevent memory pressure for large files
