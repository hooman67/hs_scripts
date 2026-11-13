# Examples

This folder contains a working example of video evaluation.

## Structure

```
examples/
├── README.md                   # This file
├── run_video_evaluation.py     # Main evaluation script
├── video_sets/                 # Model outputs
│   ├── 1.9/                    # Model 1
│   │   ├── 0.mp4
│   │   ├── 1.mp4
│   │   └── ...
│   └── wan22/                  # Model 2
│       ├── 0.mp4
│       ├── 1.mp4
│       └── ...
├── video_eval/
│   └── prompts.txt             # One prompt per line
└── example_report/             # Generated reports
    ├── comparison_report.json
    └── comparison_report.md
```

## Usage

```bash
cd /Users/jasondong/colligo
PYTHONPATH=/Users/jasondong/colligo python pylibs/colligo/eval/examples/run_video_evaluation.py
```

This will:
1. Load videos from both model folders
2. Load prompts from `prompts.txt`
3. Run 12 metrics (11 deterministic + CLIP Score)
4. Generate comparison reports in `example_report/`

## Requirements

- Videos in different model folders must have matching filenames
- Prompts must be in the same order as videos (line 1 = 0.mp4, etc.)
- For T2V tasks, only text prompts + generated videos are needed (no reference videos)

## Modifying for Your Data

1. Replace videos in `video_sets/` with your model outputs
2. Update `prompts.txt` with your prompts
3. Modify `model_dirs` and `model_names` in `run_video_evaluation.py` if needed
4. Run the script

That's it!
