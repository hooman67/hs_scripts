<div align="center">
  <img src="./frontend/public/data/brewmaster.png" alt="Brewmaster Logo" width="400">
  <h1>🍺 Brewmaster - Model Evaluation Portal</h1>
</div>

A self-contained platform for evaluating models across different tasks, datasets.

---

## 📚 Documentation

- **[utils/AGENTS.md](utils/AGENTS.md)** — Agent handoff for `brewmaster/` scope and **`i2i_mask`** metrics
- **[utils/AGENTS.md](utils/AGENTS.md)** — Docs index + Evalhub inference exports → **`i2i_mask`** CSV helpers (`brewmaster_dataset_setup.py`, `send_data.py`)
- **[utils/I2I_MASK_REVIEW_MAP.md](utils/I2I_MASK_REVIEW_MAP.md)** — Suggested reviewer split for stacked mask-edit PRs

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup, configuration, and operations guide
  - Database sync with S3
  - Metric sync from brewmaster.eval_metrics
  - Configuration options
  - Troubleshooting
- **[eval_metrics/README.md](eval_metrics/README.md)** - Evaluation metrics system documentation
  - Available metrics and their usage
  - Task types and metric selection
  - Metric implementations and validation

---

## 🚀 Quick Start

### Prerequisites
- Node.js >= 18.0.0
- Python 3.8+
- npm or pnpm

### Local Development

#### Frontend Development (Hot Reload)
```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:3000
```

#### Backend Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install video metrics dependencies (required for JEDI, LPIPS, etc.)
pip install -r eval_metrics/requirements_video_metrics.txt

# Start backend server (default database)
python start_backend.py --reload

# Or with uvicorn directly
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

### Build & Serve

**Recommended: Use the build script**
```bash
# Build and start everything (recommended)
# Automatically installs both main and video metrics dependencies
./scripts/build_and_start_servers.sh

# Or recover from crash with latest backup
./scripts/build_and_start_servers.sh --use-backup
```

**Manual build and serve:**
```bash
# Build the frontend
cd frontend
npm run build

# Serve both frontend and backend
cd ..
uvicorn backend.main:app --host 0.0.0.0 --port 8000
# Frontend served at root, API at /api/v1
```

### Rhode Deployment

**Dual-Port Configuration:**
- Port 8000: Frontend (Vite dev server in development)
- Port 8001: Backend API (FastAPI server)
- In production, backend (port 8000) serves both API and built frontend

```bash
# SSH to your Rhode deployment
ssh <pluto-machine>

# Navigate to brewmaster
cd /path/to/brewmaster

# Option 1: Use build script (recommended)
./scripts/build_and_start_servers.sh

# Option 2: Manual build and start
# Build frontend
cd frontend
npm run build

# Start backend (serves both API and frontend)
cd ..
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Access at: pluto job usr --> e.g. https://<pluto-job-name>-8000.colligo.dev/
```

---

## 📊 Data Management

### Dataset Onboarding

Brewmaster provides a streamlined script to onboard new datasets for evaluation. Datasets are stored in S3 and referenced in the database.

#### Quick Onboarding

```bash
# Onboard a new dataset
python scripts/onboard_dataset.py \
    --file /path/to/your/dataset.csv \
    --name "my_dataset" \
    --version "v1.0" \
    --task-type t2v \
    --description "Description of your dataset"
```

The script will:
1. ✅ Upload the CSV file to S3 (`s3://colligo-comparison-results/brewmaster/data/datasets/`)
2. ✅ Call the Brewmaster API to onboard the dataset

#### Dataset CSV Format

Your CSV file should contain columns appropriate for your task type:

**Text-to-Video (t2v):**
```csv
prompt,negative_prompt,seeds,width,height,num_frames,save_fps
"A cat playing piano","blurry, low quality","[0, 1]",1280,720,120,24
```

**Image-to-Video (i2v):**
```csv
prompt,input_images,negative_prompt,seeds,width,height,num_frames,save_fps
"Zoom in on flower","['/path/to/image.jpg']","blurry","[0, 1]",1280,720,120,24
```

**Video-to-Video (v2v):**
```csv
prompt,video,negative_prompt,seeds,width,height,num_frames,save_fps
"Make it winter","path/to/video.mp4","blurry","[0, 1]",1280,720,120,24
```

#### Advanced Usage

```bash
# Update an existing dataset with new version
python scripts/onboard_dataset.py \
    --file /path/to/updated_dataset.csv \
    --name "my_dataset" \
    --version "v1.1" \
    --task-type t2v

# Skip upload if file is already on S3
python scripts/onboard_dataset.py \
    --file /path/to/dataset.csv \
    --name "my_dataset" \
    --version "v1.0" \
    --task-type t2v \
    --skip-upload

# Use custom S3 key
python scripts/onboard_dataset.py \
    --file /path/to/dataset.csv \
    --name "my_dataset" \
    --version "v1.0" \
    --task-type t2v \
    --s3-key "custom_key_v1.0.csv"
```

#### Dataset Storage Locations

- **S3**: `s3://colligo-comparison-results/brewmaster/data/datasets/`
- **Shared FS** (alternative): `/sensei-fs/users/meshghi/brewmaster/datasets/`

The generation script automatically handles both S3 URLs and local paths.

#### Viewing Datasets

After onboarding, datasets appear in the Brewmaster UI:
1. Open Brewmaster in your browser
2. Click "Settings" → "Datasets"
3. Your new dataset will be available for job submission

---

## 🎯 Model Configuration & Worker Selection

Brewmaster supports **dynamic worker selection** for GPU memory optimization. You can have multiple model variants that use different workers (e.g., different Filix versions) without loading all workers into memory.

### Adding Models with Specific Workers

#### Quick Add via API

```bash
curl -X POST "http://localhost:8001/api/v1/models" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "t2v_model_1p8",
    "model_type": "local_pipeline",
    "task_type": "t2v",
    "local_path": "clineto_pipeline",
    "created_by": "your_username",
    "description": "T2V model using Filix v1.8 worker",
    "meta_data": {
      "version": "v1.8",
      "debug_overrides": {
        "dit_model_name": "filix2_t2v_prod1_8_540p_1_opt"
      }
    }
  }'
```

#### Via UI

1. Click **"+ Add Model"** in Brewmaster
2. Fill in:
   - **Model Name**: `t2v_model_1p8`
   - **Model Type**: `Local Pipeline`
   - **Local Path**: `clineto_pipeline`
   - **Description**: Model description
3. After creation, update metadata via API (shown above)

### How Dynamic Worker Selection Works

**Problem:** GPUs can't fit multiple large DiT workers (e.g., v1.8 + v1.9) simultaneously.

**Solution:** 
- Config files contain **only the default worker** (v1.9)
- Models with `debug_overrides` **swap** the default worker for their specific one
- System ensures only **one DiT worker** is loaded at a time

#### Flow Example

**When selecting `t2v_model` (default v1.9 - no override):**
```
1. Config has: filix2_t2v_prod1_9_540p_1_student_opt (default)
2. No debug_overrides → uses config as-is
3. Deploys: filix2_t2v_prod1_9_540p_1_student_opt + other workers
4. Runs job with v1.9 worker ✅
```

**When selecting `t2v_model_1p8` (with override):**
```
1. Config has: filix2_t2v_prod1_9_540p_1_student_opt (default)
2. Reads debug_overrides.dit_model_name = "filix2_t2v_prod1_8_540p_1_opt"
3. Removes: filix2_t2v_prod1_9_540p_1_student_opt
4. Adds: filix2_t2v_prod1_8_540p_1_opt
5. Deploys: filix2_t2v_prod1_8_540p_1_opt + other workers
6. Runs job with v1.8 worker ✅
```

**Key Points:**
- ✅ Config lists **only default worker** (cleaner, easier to maintain)
- ✅ Override models **swap** the worker dynamically
- ✅ **All other workers** (VAE, prompt forge, NSFW, etc.) always included
- ✅ **No OOM** - only one DiT worker loaded per job

### Model Metadata Structure

```json
{
  "version": "v1.8",
  "dit_worker": "filix2_t2v_prod1_8_540p_1_opt",
  "debug_overrides": {
    "dit_model_name": "filix2_t2v_prod1_8_540p_1_opt"
  }
}
```

**Key Fields:**
- **`version`**: Human-readable version (e.g., "v1.8")
- **`dit_worker`**: Documentation - which worker this model uses
- **`debug_overrides`**: Dictionary of runtime parameters
  - **`dit_model_name`**: Specifies which DiT worker to load

### Available DiT Workers

From `colligo/models/firefly/diffusion/clineto/types/__init__.py`:

**T2V Workers:**
- `filix2_t2v_prod1_8_540p_1_opt` (v1.8)
- `filix2_t2v_prod1_9_540p_1_student_opt` (v1.9 - default)
- `filix2_t2v_prod1_9_540p_1_teacher` (v1.9 teacher)

**V2V Workers:**
- `filix2_v2v_prod1_8_540p_1_opt` (v1.8)

**RGBA Workers:**
- `filix2_t2rgba_prod1_8_540p_1_opt` (v1.8)

**Motion Brush:**
- `filix2_motion_brush_prod1_8_540p_1`

### Additional Debug Parameters

You can override any Clineto runtime config parameter via `debug_overrides`:

```json
{
  "debug_overrides": {
    "dit_model_name": "filix2_t2v_prod1_8_540p_1_opt",
    "decoder_model_name": "dual_vae_pytorch",
    "enable_dentro_post": true,
    "fp8_step_range": [0.15, 1.0],
    "video_length": 5.33,
    "bit_rate_factor": 18
  }
}
```

### Benefits

✅ **GPU Memory Efficient** - Only one DiT worker loaded per job  
✅ **Automatic Selection** - System picks the right worker based on model  
✅ **Flexible Testing** - Easy A/B testing between model versions  
✅ **No Code Changes** - Add new models via metadata only  
✅ **Backward Compatible** - Existing models work without changes

### Verification

After creating a job with a model that has debug overrides, check the logs:

```bash
# Check generation logs
tail -f /sensei-fs/users/meshghi/brewmaster/.../logs/generation_*.log

# Look for:
INFO - Loaded debug overrides from model metadata: {'dit_model_name': 'filix2_t2v_prod1_8_540p_1_opt'}
```

### Example: Multiple Model Variants

```bash
# Add v1.8 model
curl -X POST "http://localhost:8001/api/v1/models" -H "Content-Type: application/json" -d '{
  "model_name": "t2v_filix_1p8",
  "model_type": "local_pipeline",
  "task_type": "t2v",
  "local_path": "clineto_pipeline",
  "created_by": "meshghi",
  "meta_data": {"version": "v1.8", "debug_overrides": {"dit_model_name": "filix2_t2v_prod1_8_540p_1_opt"}}
}'

# Add v1.9 teacher model
curl -X POST "http://localhost:8001/api/v1/models" -H "Content-Type: application/json" -d '{
  "model_name": "t2v_filix_1p9_teacher",
  "model_type": "local_pipeline",
  "task_type": "t2v",
  "local_path": "clineto_pipeline",
  "created_by": "meshghi",
  "meta_data": {"version": "v1.9_teacher", "debug_overrides": {"dit_model_name": "filix2_t2v_prod1_9_540p_1_teacher"}}
}'
```

Now you can run comparison jobs between these variants, and each will use only its specified worker!

### Configuration Files

**Config files are task-based, not model-specific:**
- `backend/services/eval/configs/firefly_clineto_config_t2v.yaml` - Used by ALL t2v models
- `backend/services/eval/configs/firefly_clineto_config_i2v.yaml` - Used by ALL i2v models

**What's in the config:**
- Lists **only the default DiT worker** (e.g., `filix2_t2v_prod1_9_540p_1_student_opt`)
- Lists all other required workers (VAE, prompt forge, NSFW checker, etc.)

**Example from `firefly_clineto_config_t2v.yaml`:**
```yaml
workers:
  - clineto_pipeline
  - clineto_proxy_pipeline
  - dual_vae_pytorch
  - filix2_t2v_prod1_9_540p_1_student_opt  # Default DiT worker (v1.9)
  - internvl_4b_v1
  - nsfw_adobe_one
  - prompt_forge_filix_v2
  - t5_v2_512_torch
```

**How it works:**
- Models **without** `debug_overrides` use all workers as listed (default v1.9)
- Models **with** `debug_overrides.dit_model_name` swap the DiT worker:
  - Removes: `filix2_t2v_prod1_9_540p_1_student_opt`
  - Adds: Model's specified worker (e.g., `filix2_t2v_prod1_8_540p_1_opt`)
  - Keeps: All other workers unchanged

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Browser       │
│  (Rhode URL)    │
└────────┬────────┘
         │
         │ HTTPS
         ▼
┌─────────────────┐
│  FastAPI Server │  ← Serves both API and frontend
│  Port 8000      │     (frontend/dist/ + /api/v1)
└────────┬────────┘
         │
         ├──────────────┐
         ▼              ▼
┌─────────────────┐  ┌─────────────────┐
│  SQLite DB      │  │  Kaizen Jobs    │
│  Job Metadata   │  │  (Generation +  │
└─────────────────┘  │   Comparison)   │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Eval System    │
                     │     Metrics     │
                     └─────────────────┘
```

### Master JSON & Asset Tracking

Brewmaster uses a **Master JSON** system for efficient asset management and deduplication:

**File Structure:**
```
data/master_jsons/
├── t2v_t2v_demo_v1.0.json    # Pattern: {task_type}_{dataset_key}.json
├── i2v_t2v_demo_v1.0.json    # One file per task + dataset version
├── v2v_t2v_demo_v1.0.json
├── t2i_t2v_demo_v1.0.json
└── i2i_t2v_demo_v1.0.json
```

**Per-Dataset Structure:**
```json
{
  "models": {"uuid-1234": "firefly_video_v2.1"},
  "contents": [
    {
      "content_id": 0,
      "prompt": "A chef slicing vegetables",
      "ref_paths": {},
      "metadata": {
        "category": "Food",
        "detail_level": 1,
        "humans": 1
      }
    }
  ],
  "assets": [
    {
      "asset_id": 0,
      "content_id": 0,
      "model_id": "uuid-1234",
      "model_identifier": "firefly_video_v2.1",
      "path": "/path/to/video_0.mp4",
      "metric_scores": {
        "temporal_ssim": [0.95, 0.94, 0.96, ...],
        "fid": [25.3],
        "clip_score": [0.82, 0.83, ...]
      }
    }
  ]
}
```

**Benefits:**
- ✅ **Asset Deduplication** - Reuses assets from previous jobs (saves ~15-20 min per job)
- ✅ **Metric Persistence** - Stores calculated metrics for cross-job reuse (saves ~5-10 min per job)
- ✅ **Incremental Metrics** - Only calculate metrics that don't exist yet
- ✅ **Versioning** - Manual dataset versions for controlled regeneration
- ✅ **Scalability** - Split files by dataset for better concurrency
- ✅ **Fine-grained Locking** - Parallel writes to different datasets

**How Deduplication Works:**
When you submit a job, Brewmaster checks if matching assets already exist based on:
- Same model
- Same dataset version
- Same content (prompt + references)

If matches found → reuses assets (no regeneration needed)  
If no matches → generates new assets

### Complete Job Execution Workflow

#### **Job Submission → Completion Flow:**

```
1. User Submits Job
   ↓
2. Generation Phase
   ├─ Check Master JSON for existing assets
   │  ├─ Assets exist? → Skip generation ✅
   │  └─ Assets missing? → Generate new outputs
   ↓
   └─ Register new assets in Master JSON
      - Asset paths
      - Model/dataset association
      - Content metadata
   ↓
3. Comparison Phase (Incremental Metrics)
   ├─ Phase 2A: Check Master JSON for each requested metric
   │  ├─ For each model/dataset combination:
   │  │  ├─ Metric exists? → Load from Master JSON ✅
   │  │  └─ Metric missing? → Add to calculation list
   │  └─ Determine metrics to calculate (union of all missing)
   ↓
   ├─ Run eval_metrics ONLY on missing metrics
   │  - Skip metrics that already exist in Master JSON
   │  - Calculate only what's needed
   │  - Generate per-sample scores for new metrics
   ↓
   └─ Phase 2B: Write NEW metrics to Master JSON ✅
      - Append only newly calculated metrics
      - Preserve existing metrics (no overwrite)
      - Per-asset metric scores
      - Per-frame/sample values
      - Enables cross-job reuse and incremental calculation
   ↓
4. Report Generation
   ├─ Combine metrics from all models
   ├─ Generate comparison_report.json
   └─ Upload to S3
   ↓
5. Job Complete ✅
   - Report viewable in UI
   - Assets/metrics reusable for next job
```

#### **Cross-Job Optimization:**

**First Run (New Model/Dataset):**
- ⏱️ Generate assets: ~15-20 minutes
- ⏱️ Calculate metrics: ~5-10 minutes
- ✅ Total: ~20-30 minutes
- 💾 Assets + Metrics written to Master JSON

**Second Run (Same Model/Dataset):**
- ⚡ Skip generation: Assets exist in Master JSON
- ⚡ Skip metrics: Metrics exist in Master JSON
- ⏱️ Generate report only: ~30 seconds
- ✅ Total: **< 1 minute** (98% faster!)

**Incremental Run (New Metric):**
- ⚡ Skip generation: Assets exist in Master JSON
- ⚡ Reuse existing metrics: Load from Master JSON
- ⏱️ Calculate **only new metrics** not in Master JSON: ~1-2 minutes
- ✅ **Append new metrics** to Master JSON (keeps existing ones)
- ✅ Total: ~2 minutes

**How Incremental Metrics Work:**

1. **User requests metrics:** `[temporal_ssim, psnr, lpips]`
2. **Check Master JSON:**
   - `temporal_ssim`: ✅ Exists → Load from Master JSON
   - `psnr`: ✅ Exists → Load from Master JSON
   - `lpips`: ❌ Missing → Calculate via eval_metrics
3. **Calculation phase:** Run eval system ONLY for `[lpips]`
4. **Report generation:** Combine loaded + calculated metrics
5. **Write back:** Append `lpips` to Master JSON (keeps `temporal_ssim`, `psnr`)
6. **Next run:** All 3 metrics exist, skip calculation entirely

#### **Directory Structure (Consistent):**

All jobs follow this structure regardless of single or multi-model:
```
workdir/
  outputs/
    {model_id}/              # Always includes model_id
      logs/                  # Generation logs
      {dataset_id}/          # One per dataset
        outputs/             # Generated videos/images
          0.mp4
          1.mp4
          ...
        prompts.txt          # Dataset prompts
        results.json         # Generation metadata
  comparison_results/        # Comparison outputs
    comparison_report.json   # Final comparison
    logs/                    # Comparison logs
  eval_status.json           # Job status tracking
```

#### **Understanding the JSON Files:**

**`results.json`** (per dataset, per job):
- Purpose: Generation job metadata only
- Contains: model_id, dataset_id, status, timestamp, sample count
- Does NOT contain: metrics, comparison data, asset paths
- Used for: Validation that generation succeeded

**`comparison_report.json`** (per job):
- Purpose: Comparison results for UI display
- Contains: Metrics, model rankings, summary statistics
- Stored in: Job's workdir, then S3, then optionally in database
- Used for: UI report viewer

**Master JSON** (`data/master_jsons/{task}_{dataset}_{version}.json`):
- Purpose: Persistent asset and metric storage across ALL jobs
- Contains: All assets ever generated, all metrics ever calculated
- Stored in: Shared master_jsons directory
- Used for: Cross-job deduplication and metric reuse

**Why separate files?**
- `results.json`: Ephemeral, job-specific metadata
- `comparison_report.json`: Job-specific report for UI
- **Master JSON**: Persistent, cross-job asset and metric registry

---

## ✨ Features

### ✅ **Core Features**
- **React UI** with Material-UI and TypeScript
- **FastAPI Backend** with SQLite database
- **Automated Job Execution** via Kaizen compute infrastructure
- **Real-time Job Monitoring** with status updates and progress tracking
- **Job Cancellation** with process termination
- **Dataset & Model Management** with full CRUD operations
- **Master JSON System** for asset deduplication and versioning
- **Interactive Dashboard** with report viewing and data export (JSON/CSV)
- **MobX State Management** for reactive UI
- **Responsive Design** for all screen sizes
- **S3 Integration** for distributed storage and backup
- **Automatic Metric Sync** from eval_metrics module

### 🎯 **Evaluation Capabilities**
- **Generation and Model Evaluation** across T2V, I2V, V2V, T2I, I2I tasks
- **Quality Metrics** (temporal consistency, CLIP score, BRISQUE, JEDI, LPIPS, etc.)
- **Multi-Model Comparison** with automated ranking
- **Comprehensive Reports** (JSON + Markdown + HTML)
- **Asset Deduplication** - Skip regeneration when assets exist (saves 15-20 min)
- **Metric Persistence & Reuse** - Store metrics in Master JSON, reuse across jobs (saves 5-10 min)
- **Incremental Metrics** - Calculate only new metrics, load existing ones from Master JSON (saves ~8 min per reused metric)
  - Request metrics `[A, B, C]`, only `B` exists → Calculate `[A, C]` only, load `B` from Master JSON
  - New metrics appended to Master JSON, existing metrics preserved
  - Full automation: comparison script checks Master JSON before calculation
- **Download Results** as JSON or CSV for external analysis

---

## 📁 Project Structure

```
brewmaster/                                   # 🍺 Model Evaluation Portal
├── README.md                                 # 📝 This file
├── requirements.txt                          # 📦 Python dependencies
├── rhode.yaml                                # 🚀 Deployment configuration
│
├── eval_metrics/                             # 📊 Evaluation metrics system
│   ├── requirements_video_metrics.txt        # 📦 Video metrics dependencies
│   └── ...                                   # (See eval_metrics/README.md)
│
├── frontend/                                 # ⚛️ React frontend
│   ├── public/data/                          # 🖼️ Static assets
│   ├── src/
│   │   ├── components/                       # 🧩 UI components
│   │   │   ├── layout/                       # Header, Sidebar, MainContent
│   │   │   ├── job/                          # Job submission, history, results
│   │   │   │   ├── JobSubmissionForm.tsx     # Job creation form
│   │   │   │   ├── JobHistoryTable.tsx       # Job list/history
│   │   │   │   ├── JobDetails.tsx            # Job detail view
│   │   │   │   ├── JobResults.tsx            # Job results display
│   │   │   │   ├── JobResultsVisualization.tsx # Results charts
│   │   │   │   └── JobStatusBadge.tsx        # Status indicator
│   │   │   ├── dashboard/                    # Report viewer
│   │   │   │   └── ReportViewer.tsx          # HTML report display
│   │   │   ├── settings/                     # Resource management
│   │   │   │   ├── AddDatasetModal.tsx       # Dataset creation
│   │   │   │   └── AddModelModal.tsx         # Model creation
│   │   │   └── registry/                     # Registry viewer
│   │   │       └── RegistryViewer.tsx        # View registered resources
│   │   ├── store/                            # 🗃️ MobX stores
│   │   │   ├── jobStore.ts                   # Job state management
│   │   │   ├── datasetStore.ts               # Dataset state
│   │   │   ├── modelStore.ts                 # Model state
│   │   │   ├── metricStore.ts                # Metric state
│   │   │   └── uiStore.ts                    # UI state
│   │   ├── api/                              # 🔌 API client
│   │   │   ├── client.ts                     # Base API client
│   │   │   ├── jobs.ts                       # Job API
│   │   │   ├── datasets.ts                   # Dataset API
│   │   │   ├── models.ts                     # Model API
│   │   │   ├── metrics.ts                    # Metric API
│   │   │   └── system.ts                     # System API
│   │   └── types/                            # 📝 TypeScript types
│   ├── dist/                                 # 📦 Built static files
│   └── package.json
│
├── backend/                                  # 🐍 FastAPI backend
│   ├── api/v1/                               # 🌐 REST API endpoints
│   │   ├── datasets.py                       # Dataset endpoints
│   │   ├── jobs.py                           # Job endpoints
│   │   ├── metrics.py                        # Metric endpoints
│   │   ├── models.py                         # Model endpoints
│   │   └── system.py                         # System endpoints
│   ├── db/                                   # 🗄️ Database models
│   │   ├── models.py                         # SQLAlchemy models
│   │   ├── session.py                        # Database session
│   │   ├── base.py                           # Base classes
│   │   └── backup_triggers.py                # Backup automation
│   ├── schemas/                              # 📋 Pydantic schemas
│   ├── services/                             # 🔧 Core services
│   │   ├── brewmaster_job_executor.py        # Main job orchestrator
│   │   ├── result_processor.py               # Result processing
│   │   ├── report_generator.py               # HTML report generation
│   │   ├── master_json_manager.py            # Master JSON management
│   │   ├── asset_detail_generator.py         # Asset detail generation
│   │   ├── dataset_parser.py                 # Dataset parsing utilities
│   │   ├── metric_sync_service.py            # Metric synchronization
│   │   ├── eval/                             # Kaizen integration
│   │   │   ├── eval_config_manager.py        # Config & YAML generation
│   │   │   ├── eval_status_manager.py        # Status tracking
│   │   │   ├── eval_timeout_manager.py       # Timeout handling
│   │   │   ├── eval_service.py               # Eval service coordination
│   │   │   ├── eval_runner.py                # Eval job runner
│   │   │   ├── eval_job_monitor.py           # Job monitoring
│   │   │   ├── job_monitor.py                # Background job monitoring
│   │   │   ├── pluto_cli.py                  # Pluto CLI integration
│   │   │   ├── s3_utils.py                   # S3 utilities
│   │   │   ├── result_processor.py           # Result processing
│   │   │   ├── generation_kaizen_script.sh   # Generation job script
│   │   │   └── comparison_kaizen_script.sh   # Comparison job script
│   │   ├── generation/                       # Generation service
│   │   │   ├── main.py                       # Video/image generation
│   │   │   └── utils/                        # Generation utilities
│   │   └── comparison/                       # Comparison service
│   │       └── main.py                       # Metric computation & comparison
│   └── main.py                               # 🚀 FastAPI app
│
├── config/                                   # ⚙️ Configuration
│
├── scripts/                                  # 🛠️ Utility scripts
│   ├── setup_database.py                     # Database setup and initialization
│   ├── backup_database.py                    # Database backup utilities
│   ├── sync_to_s3.py                         # S3 synchronization
│   ├── sync_metrics.py                       # Metric synchronization
│   ├── onboard_dataset.py                    # Dataset onboarding script
│   ├── cleanup_stale_jobs.py                 # Clean up stale jobs
│   ├── check_metric_compatibility.py         # Verify metric compatibility
│   └── build_and_start_servers.sh            # Build and start all servers
│
├── utils/                                    # 📝 Agent docs + offline Evalhub CSV helpers (see AGENTS.md)
│   └── ...
│
└── tests/                                    # 🧪 Test files
    ├── test_master_json.py                   # Master JSON functionality tests
    ├── test_master_json_split.py             # Master JSON split tests
    ├── test_proactive_population.py          # Proactive population tests
    └── test_smart_workflows.py               # Smart workflow tests
```

---

## 🎬 How It Works

### 1. Job Submission
User submits an evaluation job via the UI, specifying:
- **Models** to evaluate (e.g., `t2v_model`)
- **Datasets** to test on (e.g., `t2v_1_example_set`)
- **Metrics** to compute (e.g., `Temporal SSIM`)

The system checks for existing assets in the master JSON and determines what needs to be generated.

### 2. Generation Phase
For each model/dataset combination:
- **Check master JSON** for existing assets (deduplication)
- **Launch Kaizen job** with appropriate compute resources (if new assets needed)
- **Generate videos/images** for all prompts in dataset
- **Save outputs** to structured directories (`outputs/{model_id}/{dataset_id}/`)
- **Save prompts** to `prompts.txt` for eval system
- **Update master JSON** with asset paths and metadata

### 3. Comparison Phase
After all generation jobs complete:
- **Launch comparison Kaizen job**
- **Run eval_metrics** on generated assets
- **Compute all selected metrics** (temporal, perceptual, alignment, etc.)
- **Aggregate results** across all models and datasets
- **Identify best model** based on metric scores
- **Update master JSON** with metric scores for future reference

### 4. Report Generation & Storage
- **JSON report** with all metrics and raw data
- **Markdown reports** with human-readable interpretations
- **HTML reports** for interactive viewing
- **Results stored** in database for frontend display
- **Upload to S3** for persistence and sharing
- **Clean up sensei-fs** after successful upload

### 5. Asset Deduplication
On subsequent jobs:
- System checks master JSON for matching assets
- Reuses existing assets if model, dataset, and content match
- Only generates new assets when needed
- Saves significant time and compute resources

---

## 📊 Output Directory Structure

Brewmaster jobs create a structured output hierarchy:

```
/sensei-fs/users/{username}/brewmaster/{user_id}_{timestamp}_{job_id}/
│
├── logs/                                          # 📋 All logs
│   ├── generation_{model}_{dataset}.log           # Per-model logs
│   └── comparison_{job_id}.log                    # Comparison logs
│
├── brewmaster_status.json                         # ⚡ Real-time status
│
├── outputs/                                       # 🎬 Generated content
│   └── {model_id}/
│       └── {dataset_id}/
│           ├── outputs/                           # Videos/images HERE
│           │   ├── 0.mp4
│           │   ├── 1.mp4
│           │   └── ...
│           ├── prompts.txt                        # Input prompts
│           └── results.json                       # Generation metrics
│
└── comparison_results/                            # 📈 Evaluation results
    ├── comparison_report.json                     # Combined report
    └── eval_reports/                              # Per-model reports
        └── {model_id}_{dataset_id}/
            ├── comparison_report.json             # Detailed metrics
            └── comparison_report.md               # Human-readable
```

**Key Locations:**
- **Videos**: `outputs/{model_id}/{dataset_id}/outputs/*.mp4`
- **Prompts**: `outputs/{model_id}/{dataset_id}/prompts.txt`
- **Eval Reports**: `comparison_results/eval_reports/{model}_{dataset}/`
- **Logs**: `logs/` (root level)
- **Status**: `brewmaster_status.json`

> **Note:** After evaluation completes, the directory will be uploaded to S3 and the generated assets will be removed from the sensei-fs directory to free up space.

---

## 🔬 Evaluation Metrics System Integration

Brewmaster uses the **eval_metrics** module for comprehensive video/image evaluation.

**Status**: Production Ready ✅  
**Latest Update**: Enhanced with 6 new temporal consistency metrics (Nov 2025)

**Key Features:**
- **50+ evaluation metrics** (temporal consistency, CLIP score, BRISQUE, JEDI, LPIPS, etc.)
- **Automatic metric computation** during comparison phase
- **Support for multiple tasks**: T2V, I2V, V2V, T2I, I2I
- **No manual configuration needed** - metrics auto-sync on startup
- **Deterministic temporal metrics** (9 metrics) - no external models required
- **Model-based metrics** (CLIP, LPIPS, JEDI) - high-quality evaluation

**Dependencies:**
- Main requirements in `requirements.txt`
- Video metrics requirements in `eval_metrics/requirements_video_metrics.txt`
  - Includes: `videojedi` (JEDI Score), `lpips` (Perceptual Similarity), `transformers` (CLIP)
  - Optional but recommended for full metric coverage
  - Automatically installed by `build_and_start_servers.sh`

**Evaluation Performance:**
- ~15-20 seconds per video (all metrics)
- 2-4GB RAM, GPU optional (speeds up CLIP/LPIPS)

**Available Metric Categories:**
- **Temporal Metrics**: Frame-to-frame consistency, motion smoothness
- **Perceptual Quality**: BRISQUE, NIQE, sharpness, contrast
- **Text-Visual Alignment**: CLIP score, semantic similarity
- **Reference-Based**: SSIM, PSNR, LPIPS, MSE
- **Video-Specific**: JEDI score, FVD (Frechet Video Distance)

**See [eval_metrics/README.md](eval_metrics/README.md) for:**
- Complete metrics list and implementations
- Task types and metric selection
- Metric validation and troubleshooting
- How to add new metrics

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:**
- Metric sync configuration
- Database integration
- Manual usage examples

---

## 🔧 Configuration

### Essential Settings

**Key Configuration (config/settings.py):**
- **Database**: `data/brewmaster.db` (configurable via `BREWMASTER_DB_FILE`)
- **Backend Port**: 8000 (production) or 8001 (development)
- **Master JSON Directory**: `data/master_jsons/`
- **Asset Storage**: `/sensei-fs/users/meshghi/brewmaster/assets`
- **S3 Sync**: Automatic every 5 minutes
- **Stale Job Threshold**: 24 hours (configurable via `STALE_JOB_THRESHOLD_HOURS`)
- **Generation Branch**: `main` (configurable via `GENERATION_BRANCH`)

**Environment Variables:**
- `BREWMASTER_DB_FILE` - Override default database file
- `BACKEND_HOST` - Backend host (default: 0.0.0.0)
- `BACKEND_PORT` - Backend port (default: 8001)
- `STALE_JOB_THRESHOLD_HOURS` - Hours before job is marked stale (default: 24)
- `GENERATION_BRANCH` - Git branch for generation jobs (default: main)

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:**
- Complete environment variables
- AWS credentials setup
- Database configuration options
- Custom S3 paths

---

## 📊 API Endpoints

### System
- `GET /api/v1/health` - Health check
- `GET /api/v1/tasks` - List available task types

### Jobs
- `POST /api/v1/jobs` - Submit new job
- `GET /api/v1/jobs` - List all jobs
- `GET /api/v1/jobs/{id}` - Get job details
- `DELETE /api/v1/jobs/{id}` - Cancel job (terminates executor process)
- `GET /api/v1/jobs/{id}/report` - Get job report (HTML)
- `GET /api/v1/jobs/{id}/comparison-data` - Get comparison report JSON
- `GET /api/v1/jobs/{id}/download/json` - Download results as JSON
- `GET /api/v1/jobs/{id}/download/csv` - Download results as CSV
- `GET /api/v1/jobs/{id}/asset-detail` - Get detailed asset information

### Datasets
- `GET /api/v1/datasets` - List datasets
- `GET /api/v1/datasets/{id}` - Get dataset details
- `POST /api/v1/datasets` - Create dataset
- `PUT /api/v1/datasets/{id}` - Update dataset
- `DELETE /api/v1/datasets/{id}` - Delete dataset

### Models
- `GET /api/v1/models` - List models
- `GET /api/v1/models/{id}` - Get model details
- `POST /api/v1/models` - Create model
- `PUT /api/v1/models/{id}` - Update model
- `DELETE /api/v1/models/{id}` - Delete model

### Metrics
- `GET /api/v1/metrics` - List metrics
- `GET /api/v1/metrics/{id}` - Get metric details
- `POST /api/v1/metrics` - Create metric
- `GET /api/v1/metrics/registry/available` - List all available metrics from eval_metrics registry

**Discovering Valid Metrics:**
```bash
# Get all available metrics
curl http://localhost:8000/api/v1/metrics/registry/available | jq '.metrics'

# Find motion-related metrics
curl http://localhost:8000/api/v1/metrics/registry/available | jq '.metrics[] | select(contains("motion"))'

# Get metric details
curl http://localhost:8000/api/v1/metrics/registry/available | jq '.details.motion_smoothness'
```

**API Documentation**: Available at `/docs` when backend is running

---

## 🛠️ Scripts & Utilities

### Main Scripts

```bash
# Build and start everything (recommended)
./scripts/build_and_start_servers.sh

# Recover from crash with latest backup
./scripts/build_and_start_servers.sh --use-backup

# Setup/reset database
python scripts/setup_database.py

# Onboard a new dataset
python scripts/onboard_dataset.py --file <path> --name <name> --version <version> --task-type <type>

# Sync metrics from eval_metrics module
python scripts/sync_metrics.py

# Backup database
python scripts/backup_database.py

# Sync database to S3
python scripts/sync_to_s3.py

# Clean up stale jobs
python scripts/cleanup_stale_jobs.py

# Sync master JSONs between local and sensei-fs
python scripts/sync_master_jsons.py
```

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:**
- Complete script options and flags
- Database management commands
- Job management utilities
- Manual sync commands

### S3 Backup and Storage

Brewmaster automatically backs up both database and job outputs to S3. See **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for detailed S3 configuration and sync instructions.

**Quick Summary:**
- Database synced to S3 every 5 minutes
- Job outputs uploaded after completion
- Automatic cleanup of sensei-fs after successful upload
- S3 location: `s3://colligo-comparison-results/brewmaster/`

### Master JSON Synchronization

**Master JSON files are automatically synced** between local storage and sensei-fs:

**Automatic Sync Points:**
1. **Dataset Creation** → Local to sensei-fs (automatic)
2. **Job Completion** → Sensei-fs to local (automatic)

**Manual Sync** (when needed):
```bash
# Sync all files from local to sensei-fs
python scripts/sync_master_jsons.py

# Sync specific file
python scripts/sync_master_jsons.py --file t2v_t2v_demo_v1.0.json

# Sync from sensei-fs to local (reverse direction)
python scripts/sync_master_jsons.py --direction from-sensei

# Dry run (preview changes)
python scripts/sync_master_jsons.py --dry-run
```

**When to Use Manual Sync:**
- After creating datasets manually (outside API)
- Troubleshooting sync issues
- Verifying consistency between environments
- Batch operations on multiple files

### Default Data

The setup script auto-creates default dataset, model, and metrics if no backup exists. See [SETUP_GUIDE.md](SETUP_GUIDE.md) for details.

---

## 📏 Metric Management

Brewmaster uses **automatic metric synchronization** from `brewmaster.eval_metrics`. Metrics are automatically synced on backend startup and database setup.

**Key Features:**
- Auto-discovers metrics from brewmaster.eval_metrics module
- Maps metrics to task types (t2v, i2v, t2i, etc.)
- Single source of truth for metrics

**See [eval_metrics/README.md](eval_metrics/README.md) for:**
- Complete list of available metrics
- Metric implementations and details
- How to add new metrics

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:**
- Metric sync configuration
- Manual sync commands
- Troubleshooting

---

## 🗄️ Database

**Location:** `{project_root}/data/brewmaster.db`  
**Backups:** `{project_root}/data/backups/`  
**S3 Sync:** Automatic every 5 minutes

**Key Tables:**
- `evaluation_jobs` - Job metadata and status
  - Includes: status, task_type, config, progress, eval_job_id, execution_type
  - Tracks generation and comparison phases
- `evaluation_datasets` - Dataset registry
  - Includes: name, task_type, storage_url, version, metadata
- `evaluation_models` - Model registry
  - Includes: name, version, config, docker_image
- `evaluation_metrics` - Metric registry
  - Includes: name, task_types, metric_type, implementation
- `job_results` - Per-model/dataset results
  - Links jobs, models, and datasets with evaluation results

**Database Features:**
- SQLite for simplicity and portability
- Automatic backup triggers
- S3 synchronization for cross-environment consistency
- Configurable via `BREWMASTER_DB_FILE` environment variable

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:**
- Database recovery and backup options
- Database selection at startup
- Troubleshooting database issues

---

## 🚀 Deployment

### Port Strategy

Brewmaster supports flexible deployment configurations:

**Development Mode:**
- Port 8000: Frontend (Vite dev server with hot reload)
- Port 8001: Backend API (FastAPI with auto-reload)
- Separate ports for independent development

**Production Mode (Single-Port):**
1. **Build React app** to static files (`frontend/dist/`)
2. **FastAPI serves both** API and static files on port 8000
3. **Rhode exposes port 8000** for external access

### Production Deployment

```bash
# Option 1: Use build script (recommended)
./scripts/build_and_start_servers.sh

# Option 2: Manual build and serve
# Build frontend
cd frontend && npm run build

# Start production server (serves both frontend and API)
cd .. && uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Rhode Configuration

See `rhode.yaml` for deployment settings:
- Exposes ports 8000 and 8001 for development flexibility
- In production, only port 8000 is needed (single-port strategy)

---

## 🔍 Troubleshooting

### Quick Fixes

**Port Already in Use:**
```bash
./scripts/build_and_start_servers.sh  # Auto-clears ports
```

**Database Issues:**
```bash
# Recover from backup
./scripts/build_and_start_servers.sh --use-backup
```

**Backend Not Running:**
- Check `/api/v1/health` is accessible
- Verify backend is on correct port (8000 or 8001)

**Missing Video Metrics Dependencies:**
```bash
# If you see "ModuleNotFoundError: No module named 'videojedi'" or similar
pip install -r eval_metrics/requirements_video_metrics.txt
```

**Failure to submit Pluto jobs**
```bash
python3 -m colligo.pluto.sdk.cli login
```

### Common Issues & Solutions

#### Master JSON Sync Issues

**Symptom:** Jobs complete without generating assets or calculating metrics

**Cause:** Master JSON files out of sync between local and sensei-fs storage

**Solution:**
```bash
# Sync all master JSONs
python scripts/sync_master_jsons.py

# Verify sync status
python scripts/sync_master_jsons.py --dry-run
```

**Prevention:** Automatic sync runs on dataset creation and job completion. For manual dataset operations, always run the sync script.

#### Invalid Metric Names

**Symptom:** Error message "Invalid metric IDs: ['metric_name']"

**Cause:** Requested metric name doesn't exist in the eval_metrics registry

**Solution:**
```bash
# Discover available metrics via API
curl http://localhost:8000/api/v1/metrics/registry/available | jq '.metrics'

# Or check the eval_metrics documentation
cat eval_metrics/README.md
```

**Common Mistakes:**
- ❌ `motion_metrics` → Use ✅ `motion_smoothness` or `motion_magnitude`
- ❌ `histogram_metrics` → Use ✅ `histogram_kl_divergence`, `histogram_chi_square`, etc.

**Note:** Metric validation now fails early with clear error messages listing available metrics.

#### Metric UUID to Name Conversion

**Symptom:** Metrics calculated but not showing in UI, or wrong metric names in job logs

**Cause:** System using module name instead of metric's actual name

**Solution:** This has been fixed. The system now uses `config.original_name` from the metric registry for accurate name conversion. Metrics from multi-metric modules (like `motion_metrics.py` containing both `motion_smoothness` and `motion_magnitude`) now work correctly.

**Verification:**
- Check executor logs for correct metric names (not module names)
- Verify UI displays all requested metrics
- Confirm Master JSON has metrics under correct keys

#### Master JSON Filename Issues

**Symptom:** Master JSON files named with UUIDs instead of human-readable names
- Wrong: `t2v_4de06df3-9769-4433-aa78-75dccd69f490_v1.0.json`
- Expected: `t2v_t2v_demo_v1.0.json`

**Cause:** System was using database field instead of dataset_names mapping

**Solution:** This has been fixed. The system now uses the `dataset_names` mapping for consistent, human-readable filenames.

**Cleanup Old Files:**
```bash
# List master JSONs to find UUID-named files
ls -la data/master_jsons/

# Remove UUID-named file (after verifying no unique data)
rm data/master_jsons/t2v_<UUID>_v1.0.json

# Or merge if it contains unique assets (see SETUP_GUIDE.md)
```

#### Job Completing Without Work

**Symptoms:**
- Job marked as complete immediately
- No assets generated
- No metrics calculated
- No errors in logs

**Common Causes:**
1. Master JSON sync issue (see above)
2. Empty `models_datasets` mapping
3. All assets already exist in Master JSON

**Debugging:**
```bash
# Check executor logs
tail -f /tmp/brewmaster_executors/executor_<job_id>.log

# Look for DEBUG messages showing:
# - models_datasets mapping
# - Asset detection logic
# - Master JSON paths and contents
```

**Solution:**
- Verify master JSONs are synced: `python scripts/sync_master_jsons.py`
- Check job configuration has valid model and dataset IDs
- Review debug logs for asset detection results

### Debug Logging

The system includes comprehensive debug logging to help diagnose issues:

**Executor Logs Location:** `/tmp/brewmaster_executors/executor_<job_id>.log`

**What's Logged:**
- `models_datasets` mapping contents
- Number of models to process
- Asset detection results for each model
- Master JSON paths being checked
- Contents and assets count in master JSONs
- Metric name conversions (UUID to name)

**Example Debug Output:**
```
DEBUG: models_datasets = {'58b51c52-...': ['4de06df3-...']}
DEBUG: Number of models to process: 1
DEBUG: Checking master JSON at: /sensei-fs/.../t2v_t2v_demo_v1.0.json
DEBUG: Master JSON for t2v_demo_v1.0 has 12 contents, 0 assets
DEBUG: assets_needed for model 58b51c52 = True
```

### Asset Accumulation Across Jobs

**How It Works:**
- Master JSON files accumulate assets from multiple jobs with different models
- Each job adds new assets without removing existing ones
- Assets are thread-safe with per-file locking
- Asset IDs auto-increment across all models

**Example:**
```
Job 1 (Model A): Creates assets 0-11 (12 contents)
Job 2 (Model B): Adds assets 12-23 (same 12 contents, different model)
Job 3 (Model C): Adds assets 24-35 (same 12 contents, different model)

Final Master JSON: 36 assets across 3 models ✅
```

**Verification:**
```bash
# Check asset count
cat data/master_jsons/t2v_t2v_demo_v1.0.json | jq '.assets | length'

# Check unique models
cat data/master_jsons/t2v_t2v_demo_v1.0.json | jq '.models'
```

**For detailed troubleshooting, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

---

## 📖 Quick Reference

### Common Scripts

```bash
# Start servers
./scripts/build_and_start_servers.sh

# Onboard a dataset
python scripts/onboard_dataset.py \
    --file /path/to/dataset.csv \
    --name "dataset_name" \
    --version "v1.0" \
    --task-type t2v

# Sync database to S3
cd scripts && source /sensei-fs/users/meshghi/colligo_eval_creds.sh && \
python sync_to_s3.py --no-delete

# Setup/update database schema
python scripts/setup_database.py

# Check dataset in database
python -c "
from sqlalchemy import create_engine, text
engine = create_engine('sqlite:///data/brewmaster.db')
with engine.connect() as conn:
    result = conn.execute(text('SELECT id, dataset_name, storage_url FROM evaluation_datasets'))
    for row in result:
        print(f'{row[1]}: {row[2]}')
"
```

### Useful Commands

```bash
# View backend logs
tail -f /path/to/logs/backend.log

# Check backend health
curl http://localhost:8001/api/v1/health

# List S3 datasets
source /sensei-fs/users/meshghi/colligo_eval_creds.sh && \
aws s3 ls s3://colligo-comparison-results/brewmaster/data/datasets/ --region us-west-2

# Download dataset from S3
source /sensei-fs/users/meshghi/colligo_eval_creds.sh && \
aws s3 cp s3://colligo-comparison-results/brewmaster/data/datasets/my_dataset.csv . --region us-west-2
```

---

## 🧪 Testing

### Run Brewmaster Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_master_json.py
python -m pytest tests/test_smart_workflows.py

# Run with verbose output
python -m pytest tests/ -v
```

### Run Eval Metrics Tests
```bash
# Run eval metrics tests
python -m pytest eval_metrics/tests/

# Run specific metric tests
python -m pytest eval_metrics/tests/test_technical_metrics.py
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

### Available Test Suites
- **tests/test_master_json.py** - Master JSON functionality
- **tests/test_master_json_split.py** - Dataset-specific JSON splitting
- **tests/test_proactive_population.py** - Proactive asset population
- **tests/test_smart_workflows.py** - End-to-end workflow validation
- **eval_metrics/tests/test_technical_metrics.py** - Technical metric validation
- **eval_metrics/tests/test_fid_integration.py** - FID metric integration

---

## 🤝 Contributing

This is a self-contained project. All code lives in the brewmaster directory.

### Development Workflow
1. Make changes to source files
2. Test locally with `npm run dev` and `uvicorn --reload`
3. Build and test production build
4. Deploy to Rhode for testing

### Code Style
- TypeScript for frontend (see `.prettierrc`)
- Python with type hints for backend

---

## 📚 Additional Resources

### Related Documentation
- **API Documentation**: `/docs` endpoint (Swagger UI)
- **Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Eval Metrics System**: [eval_metrics/README.md](eval_metrics/README.md)
- **Type Definitions**: `frontend/src/types/`
- **Database Schema**: `backend/db/models.py`
- **Metric Implementations**: `eval_metrics/metrics/`
- **Configuration**: `config/settings.py`

### Key Files
- **Job Executor**: `backend/services/eval/brewmaster_job_executor.py`
- **Comparison Service**: `backend/services/comparison/main.py`
- **Generation Service**: `backend/services/generation/main.py`
- **Eval Config Manager**: `backend/services/eval/eval_config_manager.py`
- **Master JSON Manager**: `backend/services/master_json_manager.py`
- **Status Manager**: `backend/services/eval/eval_status_manager.py`
- **Result Processor**: `backend/services/eval/result_processor.py`

---

## 📋 TODO / Future Improvements

### Job Assignment
- [ ] **Implement job assignment to user's LDAP**
  - Currently hardcoded to `meshghi` LDAP

### Authentication & Authorization
- [ ] **Implement user authentication in frontend**
  - Currently hardcoded to `meshghi` LDAP
  - Need to implement proper authentication mechanism to get user's LDAP/token
  - Files that need updates:
    - `frontend/src/components/job/JobSubmissionForm.tsx`
    - `frontend/src/components/settings/AddDatasetModal.tsx`
    - `frontend/src/components/settings/AddModelModal.tsx`
    - `frontend/src/store/uiStore.ts`

### Job Monitoring & Reliability
- [x] **Stale job threshold configured for long-running jobs**
  - Current threshold: 24 hours (configurable via `STALE_JOB_THRESHOLD_HOURS`)
  - Accommodates long-running generation jobs that may take several hours
  - Background monitoring runs every 5 minutes to clean up stale jobs
  - Jobs stuck in `running`/`pending` for >24 hours are automatically marked as failed
  - Related files:
    - `config/settings.py` - Configuration (default: 24 hours)
    - `backend/services/eval/job_monitor.py` - Background monitoring
    - `backend/main.py` - Startup cleanup

- [x] **Comparison job timeout configured for large-scale jobs**
  - Current timeout: 24 hours (in `brewmaster_job_executor.py`)
  - Accommodates large-scale comparisons with many metrics and models
  - Comparison jobs wait for Kaizen jobs to complete on Pluto before proceeding to S3 upload
  - Related files:
    - `backend/services/eval/brewmaster_job_executor.py` - `max_wait_time = 3600 * 24`

---

<div align="center">
  <p><strong>Happy Brewing! 🍺</strong></p>
</div>
