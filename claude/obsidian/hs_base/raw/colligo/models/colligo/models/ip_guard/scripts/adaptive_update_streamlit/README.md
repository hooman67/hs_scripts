# IP Guard Adaptive Update Tool

A Streamlit web application to streamline and automate the IP Guard adaptive update process.

## Overview

This tool provides a complete workflow for managing IP Guard's RAG database and moderation sets:
- Update moderation sets (CSV files with protected entity names)
- Manage RAG reference images and build FAISS indexes
- Test RAG retrieval with visual results

## Setup

### Prerequisites

- Access to a Pluto GPU instance with colligo setup
- AWS credentials configured (for S3 uploads)
- Python 3.10+

### Installation

Set up the colligo environment; this should be run inside the colligo env.

## Running the Tool

```bash
bash /mnt/localssd/colligo/models/colligo/models/ip_guard/scripts/adaptive_update_streamlit/run.sh
```

This script will:
- Automatically detect your Pluto instance hostname
- Start Streamlit with the correct configuration
- Display the URL to access the app

Copy the displayed URL (e.g., `https://pluto-prod-user-xyz-1-0-8501.or2.colligo.dev/`) and open it in your browser

**Note:** The hostname is detected automatically, so this works on any dynamic compute instance!

## Features

### Page 1: Update Moderation Set ✅

View, edit, and upload IP moderation sets (CSV files containing protected entity names).

#### Features:
- **View moderation sets**: Browse existing entries with metadata
- **Edit moderation sets**: Add/remove entries inline
- **Upload to S3**: Package and upload to production with automatic build.py updates
- **Multiple sets supported**: adaptive, famous_names, logos, characters

### Page 2: Update RAG Database ✅

Manage the reference image database and FAISS index.

#### 1. View Existing References
- Browse all references in `references.json`
- See image previews and metadata
- Delete references with a single click

#### 2. Add New References
- **Upload images**: Drag-and-drop or browse for image files
- **Provide URLs**: Use public URLs or S3 URIs
- **Automatic S3 upload**: Uploaded images stored with unique timestamps
- **Metadata entry**: Fill in source, category, source_query, etc.
- **Validation**: Automatic validation of required fields and enum values

#### 3. Create RAG Index
- **Build FAISS index**: Creates searchable vector database from `references.json`
- **Configure encoder**: Choose embedding model (e.g., facebook/dinov2-base)
- **Set output directory**: Where to save index files (default: `/mnt/localssd/rag_db/`)
- **Real-time logs**: Watch the index creation progress with streaming logs

#### 4. Upload RAG Index
- **Upload to S3**: Package and upload FAISS index as tarball
- **Auto-update build.py**: Automatically updates `worker/retrieval/build.py` with new S3 configuration
- **Seamless workflow**: No manual copy-paste needed

### Page 3: Test RAG Database ✅

Test your RAG database with uploaded images to verify retrieval is working correctly.

#### Features:
- **Two RAG database sources**:
  - **Colligo main branch S3**: Auto-download production index from build.py config
  - **Local Index**: Test against local FAISS index you've created
- **Smart encoder selection**: Auto-detects encoder from index ENCODER_NAME file
- **Create test sets**: Upload images and generate evaluation JSON files
  - Images automatically uploaded to S3 with unique filenames
  - JSON saved to S3 and available for download
  - Mark images as containing protected IP (True/False)
  - Uses IP name for consistent prefixes in filenames and entity IDs
- **Configure retrieval parameters**: Set k and similarity threshold (defaults from `IPGuardRAGRequest`)
- **Visual results**: See query image alongside retrieved references
- **Similarity scores**: Percentage display with metadata
- **Clickable links**: Reference locations are clickable (full URL preserved)

#### Testing Workflow:

**Create and Export Test Set:**
1. Enter IP Name (e.g., "Mickey Mouse") - cached in session
2. Upload test images (files or URLs)
3. Mark which images contain protected IP
4. Click "Export Test Set JSON"
   - Images uploaded to `s3://clio.corp.adobe.com/ip_guardrails/datasets/rag_testing_uploads/`
   - Filenames: `{ip_name_snake}_{timestamp}_{hash}.{ext}`
   - JSON saved locally to `data/test_sets/`: `{ip_name_snake}_{timestamp}.json`
   - Download button available for additional local copy

**Run RAG Retrieval:**
1. Select RAG database source (S3 or local)
2. Download/specify index location
3. Adjust retrieval parameters
4. Click "Run RAG Test"
5. View results with similarity scores and metadata

## Navigation

The app uses Streamlit's multipage structure:
- **Home**: Overview and quick reference
- **📝 Update Moderation Set**: Edit CSV files with protected names
- **📸 Update RAG Database**: Manage reference images and build indexes
- **🧪 Test RAG Database**: Test retrieval and create evaluation sets

## File Locations

### Data Files
- **references.json**: `/mnt/localssd/colligo/models/colligo/models/ip_guard/data/references.json`
- **Moderation sets**: `/mnt/localssd/colligo/models/colligo/models/ip_guard/data/*.csv`
- **Test sets**: `/mnt/localssd/colligo/models/colligo/models/ip_guard/data/test_sets/{ip_name}_{timestamp}.json`

### S3 Locations
- **Reference images**: `s3://clio.corp.adobe.com/ip_guardrails/datasets/references/adaptive/`
- **Test images**: `s3://clio.corp.adobe.com/ip_guardrails/datasets/rag_testing_uploads/`
- **RAG indexes**: `s3://clio.corp.adobe.com/ip_guardrails/faiss_indexes/`
- **Moderation sets**: `s3://clio.corp.adobe.com/ip_guardrails/datasets/moderation_sets/`

## Development

### Project Structure
```
scripts/adaptive_update_streamlit/
├── Home.py                              # Home page
├── run.sh                               # Startup script
├── requirements.txt                     # Dependencies
├── README.md                            # This file
├── .streamlit/
│   └── config.toml                     # Streamlit config
├── pages/
│   ├── 1_Update_Moderation_Set.py
│   ├── 2_Update_RAG_Database.py
│   └── 3_Test_RAG_Database.py
├── components/
│   ├── common/                         # Shared components
│   │   └── image_uploader.py          # Reusable image upload widget
│   ├── update_moderation_set/         # Page 1 components
│   │   ├── moderation_set.py          # Main orchestrator
│   │   ├── moderation_set_viewer.py
│   │   ├── moderation_set_editor.py
│   │   └── upload_moderation_set.py
│   ├── update_rag_database/           # Page 2 components
│   │   ├── rag_update.py             # Main orchestrator
│   │   ├── add_reference_form.py
│   │   ├── reference_grid.py
│   │   ├── create_index.py
│   │   └── upload_index.py
│   └── test_rag_database/             # Page 3 components
│       ├── rag_testing.py             # Main orchestrator
│       ├── create_test_set.py
│       ├── rag_source_selector.py
│       ├── retrieval_params.py
│       └── rag_retrieval.py
└── utils/
    ├── json_handler.py                # JSON operations
    ├── s3_handler.py                  # S3 operations (images and JSON)
    ├── url_utils.py                   # URL handling and unique filename generation
    ├── string_utils.py                # Snake case conversion
    ├── local_storage.py               # Session state caching (IP name)
    ├── index_retrieval.py             # Domain logic for RAG index retrieval
    ├── subprocess_utils.py            # Shell command execution with streaming logs
    ├── build_file_utils.py            # Parse and update build.py files
    └── constants.py                   # Shared constants
```

### Adding New Features

To add a new page:
1. Create a new file in `pages/` with numeric prefix (e.g., `4_📊_New_Page.py`)
2. The number prefix controls the order in the sidebar
3. Streamlit automatically detects and adds it to the navigation

To add features to existing pages:
1. Create components in the appropriate `components/` subdirectory
2. Import and use in the page's main orchestrator file
3. Put reusable logic in `utils/`

## Support

For issues or questions, reach out to the IP Guard ML team.
