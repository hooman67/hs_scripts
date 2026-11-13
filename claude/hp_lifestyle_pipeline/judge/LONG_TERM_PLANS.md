# Judge roadmap

1. Natural-placement prototype: freeze rubric, preserve a small held-out experiment, expose failure cases and uncertainty.
2. Placement calibration: obtain independent C-Tech labels for clear passes, minor awkwardness, material/major defects and unobservable close crops. Keep image families together; freeze weights/thresholds on development and evaluate on new cases. Current preference annotations cannot substitute for this.
3. Model/vision improvements: compare stronger visual models or structured geometric evidence on development only. Avoid repeatedly tuning on the current held-out cases; after inspection they become historical test data, not a new untouched test.
4. Integration only after adequate performance: versioned input/output contracts, explicit stage checks, no silent fallback, auditable model/version and artifacts. No automatic scene regeneration or changes to V6.1 in this detour.

Other judges (fidelity, text/faces, prop compliance, lighting, etc.) remain future scope. No date or production acceptance threshold has been agreed.
