# Upload HTML artifacts to Foundry S3

Whenever producing an HTML report, gallery, visualization, or review artifact for Hooman, upload it to the
appropriate Foundry S3 bucket and return a directly clickable `https://foundry-aws-corp.adobe.io/asset/...`
URL. Do not hand off only a local HTML file.

Use the global `render-s3-gallery` skill for the authoritative upload, IMS authentication, content-type, and URL
conventions. Never use presigned URLs or embed credentials in HTML.

Local filesystem paths must still be shown as complete absolute paths in plain-text code blocks when referenced.
