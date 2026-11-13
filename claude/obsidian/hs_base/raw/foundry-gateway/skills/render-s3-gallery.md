Generate an HTML gallery to visualize assets on a Foundry S3 bucket, viewable via foundry-aws-corp.adobe.io.

Usage: /render-s3-gallery <s3_bucket> <s3_prefix> [--title "Gallery Title"] [--filter "pattern1,pattern2"]

Parse $ARGUMENTS to extract:
- **s3_bucket**: the S3 bucket name (e.g. `foundry-tccc-enterprise-adobe-assets`)
- **s3_prefix**: the S3 key prefix containing assets (e.g. `dam_assets_downloaded_by_hs/lifestyle_campaign`)
- Optional `--title "..."`: gallery title (defaults to bucket/prefix)
- Optional `--filter "..."`: comma-separated folder name substrings to include (if omitted, includes all)

## Credentials

Get temporary AWS credentials from `~/Downloads/creds.txt` (exported via foundry-aws-corp.adobe.io "Get Foundry Developer Credentials"). Source them before any `aws s3` commands:

```bash
source ~/Downloads/creds.txt
```

If the file is missing or expired, ask the user to refresh credentials at https://foundry-aws-corp.adobe.io/.

## How it works

Assets on Foundry S3 buckets are viewable at `https://foundry-aws-corp.adobe.io/asset/<bucket>/<key>` for anyone who is signed in and is a Foundry Initiative member. The gallery HTML and its supporting files are uploaded to a `gallery/` subfolder under the asset prefix. Images in the HTML use **relative paths** (e.g. `../tccc/marketing/.../image.png`) — no presigned URLs, no embedded credentials.

Ref: https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3647579510/Project+Setup+and+Access#ProjectSetupandAccess-ViewingHTMLassetsfromabucket

## Step-by-step

### 1. List assets

```bash
source ~/Downloads/creds.txt
aws s3 ls s3://<bucket>/<prefix>/ --recursive --region us-west-2
```

Filter to image/video extensions: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.tif`, `.tiff`, `.psd`, `.mp4`, `.mov`.

If `--filter` is provided, only include files whose path contains one of the filter substrings.

### 2. Build data.js

Create a JavaScript file with this structure:

```js
const GALLERY_DATA = {
  "Campaign Label 1": [
    {"n": "filename.png", "s": 12345, "p": "relative/path/from/prefix/filename.png"},
    {"n": "file.tif", "s": 99999, "p": "relative/path/file.tif", "t": "tif"}
  ],
  "Campaign Label 2": [...]
};
```

- `n` = filename, `s` = size in bytes, `p` = path relative to the prefix (NOT the gallery/ subfolder)
- `t` = file extension string for non-browser-viewable files (tif, tiff, psd). Omit for viewable files.
- Group files by folder/campaign. Use human-readable labels as keys.
- Paths in `p` are relative to the prefix folder. The HTML is inside `<prefix>/gallery/`, so it references assets as `../<p>`.

### 3. Create the gallery files

Create these 5 files locally, then upload to `s3://<bucket>/<prefix>/gallery/`:

#### index.html
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GALLERY_TITLE</title>
        <link rel="stylesheet" href="./style.css">
    </head>
    <body>
        <!-- IMS auth bar — REQUIRED for foundry-aws-corp.adobe.io -->
        <div id="ims"></div>
        <!-- Loading state -->
        <div id="loading" class="loading-screen">Loading...</div>
        <!-- Main content (hidden until auth completes) -->
        <div id="content" class="hidden">
            <div class="header-bar">
                <h1>GALLERY_TITLE</h1>
                <div class="subtitle">BUCKET_NAME</div>
                <div class="controls">
                    <input type="text" class="search-input" id="searchInput" placeholder="Search filenames or folders...">
                    <label style="font-size:11px;color:#888;">Size</label>
                    <input type="range" class="size-slider" id="sizeSlider" min="100" max="500" value="220">
                </div>
            </div>
            <div class="folder-nav" id="folderNav"></div>
            <div class="gallery" id="gallery"></div>
        </div>
        <!-- Lightbox modal -->
        <div id="assetModal" class="modal" onclick="if(event.target===this)closeModal()">
            <button class="close-btn" onclick="closeModal()">&times;</button>
            <button class="nav-btn nav-prev" onclick="navModal(-1)">&lsaquo;</button>
            <button class="nav-btn nav-next" onclick="navModal(1)">&rsaquo;</button>
            <img id="modalImage" src="" alt="Full size">
            <div class="modal-info" id="modalInfo"></div>
        </div>
        <!-- Scripts: IMS lib MUST come first -->
        <script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script>
        <script src="./imsauth.js"></script>
        <script src="./data.js"></script>
        <script src="./main.js"></script>
        <script>
            document.addEventListener("DOMContentLoaded", () => { initializeIMS(); });
        </script>
    </body>
</html>
```

#### imsauth.js

This is the IMS authentication script. It handles Adobe SSO sign-in and sets a `user_token` cookie at path `/asset` so the foundry gateway authorizes asset requests. **Copy this file exactly every time — do not modify it.**

Reference implementation is at: `~/hs_scripts/claude/temp_work/lifestyle_gallery/imsauth.js`

Key details:
- Uses `client_id: "colligo_testing"`, `environment: "stg1"`, scope `"AdobeID,firefly_api,openid"`
- IMS lib loaded from `https://auth-stg1.services.adobe.com/imslib/imslib.js`
- On successful auth, sets cookie: `document.cookie = "user_token=<token>; path=/asset; max-age=86400;"`
- Calls `onAuthReady()` (defined in main.js) after auth completes
- Provides sign-in/sign-out buttons and a token override fallback

#### style.css

Reference implementation: `~/hs_scripts/claude/temp_work/lifestyle_gallery/style.css`

Key sections: IMS bar styling (`.ims-span`, `.ims-button`), header, controls, folder chip nav, image grid with CSS variable `--thumb-size`, cards, lightbox modal, dark theme (#000 background).

#### main.js

Reference implementation: `~/hs_scripts/claude/temp_work/lifestyle_gallery/main.js`

Provides: `onAuthReady()` (called by imsauth.js after login), folder chip navigation, search filtering, grid rendering with `loading="lazy"`, lightbox with arrow key navigation. Non-viewable files (`.t` field present) render as labeled placeholders showing file type and size.

Image `src` attributes use `"../" + item.p` since the HTML is in the `gallery/` subfolder.

### 4. Upload to S3

Upload each file with the correct `--content-type`:

```bash
source ~/Downloads/creds.txt
aws s3 cp index.html  s3://<bucket>/<prefix>/gallery/index.html  --content-type "text/html"       --region us-west-2
aws s3 cp imsauth.js  s3://<bucket>/<prefix>/gallery/imsauth.js  --content-type "application/javascript" --region us-west-2
aws s3 cp data.js     s3://<bucket>/<prefix>/gallery/data.js     --content-type "application/javascript" --region us-west-2
aws s3 cp main.js     s3://<bucket>/<prefix>/gallery/main.js     --content-type "application/javascript" --region us-west-2
aws s3 cp style.css   s3://<bucket>/<prefix>/gallery/style.css   --content-type "text/css"         --region us-west-2
```

### 5. Return the URL

The gallery is accessible at:

```
https://foundry-aws-corp.adobe.io/asset/<bucket>/<prefix>/gallery/index.html
```

**IMPORTANT:** Always use `https://foundry-aws-corp.adobe.io` — never older URLs like `foundry-html-dev.corp.ethos851-stage-or2.ethos.adobe.net`.

## Critical rules

- **No presigned URLs.** All asset references are relative paths.
- **No embedded credentials.** Auth is handled by IMS cookie.
- **Always include imsauth.js** and the IMS library script tag. Without it, the gateway won't authorize image requests and nothing will load.
- **Content-Type headers matter.** If you upload `.js` as `binary/octet-stream`, browsers won't execute it.
- **Relative path from gallery/ subfolder.** Since `index.html` is at `<prefix>/gallery/index.html`, asset paths are `../<relative_to_prefix>`.
- **Browser-viewable formats:** png, jpg, jpeg, gif, webp, svg. Everything else (tif, tiff, psd, ai) should be marked with `"t"` field and shown as placeholders.
- **Reference implementations** of all files live at `~/hs_scripts/claude/temp_work/lifestyle_gallery/`. When creating a new gallery, read those files and adapt (change title, data, etc.) rather than writing from scratch.

## Working example

A known-working gallery that was validated:
```
https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/dam_assets_downloaded_by_hs/lifestyle_campaign/gallery/index.html
```

Local files: `~/hs_scripts/claude/temp_work/lifestyle_gallery/`
