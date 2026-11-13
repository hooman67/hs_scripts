# V23 calibration evidence map

- `CALIBRATION_REPORT.md`: canonical final run-3 report.
- `run_1/`: frozen first calibration against source SHA-256 `1fead3c08c441bf361a4878d2945265a6ce6398f24fbd379a77b9243a556402d`.
- `run_2/`: corrected calibration against frozen source SHA-256 `67cdf7608b6315792542ad95dadf15fafc5f41f879116a14463b5d6b11531ccb`.
- `run_3/`: final calibration against frozen source SHA-256 `8c1a8204d27eeb3ba922d6d9519113da7beeff9368301bcc9f8c9a7ec2fb2665`.
- Root result/checkpoint files mirror run 3 for convenient resume. Runs 1 and 2 remain immutable in their versioned folders.
- `compare_runs.py`: deterministic run-1/run-2/run-3 comparison; output is `run_3/run_comparison.json`.
- `replay_v23_calibration.py`: source-hash-keyed replay runner. Set `V23_CALIBRATION_OUT` to choose an isolated run directory.

Neither run made model calls, generated images, or edited Foundry source.
