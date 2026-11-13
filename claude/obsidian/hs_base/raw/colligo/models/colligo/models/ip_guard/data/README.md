# IPGuard Data

This folder contains easily-accessible and modifiable versions of IPGuard moderation sets and RAG DBs.

NOTE: These files are NOT used directly by the IPGuard pipeline! The IPGuard source of truth for these files are the S3 artifacts linked in the build files. If you want to update IPGuard, you must follow the instructions in the [RAG Update Runbook](https://wiki.corp.adobe.com/spaces/GenAI/pages/3785502188/RAG+Update+Runbook). These files are included for convenience of making updates. This is not intended to be a long-term solution. 

Pleae update these files in sync with the S3 build objects.

## Contents

- `adaptive.csv`: Adaptive moderation set
- `characters.csv`: Characters moderation set
- `famous_names.csv`: Famous names moderation set
- `logos.csv`: Logos moderation set
- `references.json`: Input to `create_index.py` script specifying the data to include in the RAG DB.