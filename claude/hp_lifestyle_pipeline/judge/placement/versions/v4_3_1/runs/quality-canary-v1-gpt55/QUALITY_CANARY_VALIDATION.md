# V4.3.1 GPT-5.5 quality canary validation

- Target: `elitebook__laptop_FrontLeftMedium__p1`
- Frozen protocol: `hp-natural-placement-v4.3.1-compact-quality-canary-v1`
- Requested model: `gpt-5.5`
- Returned model: `gpt-5.5-2026-04-23`
- Attempts: 1
- Finish reason: `stop`
- Refusal: none
- Total tokens: 31,325
- Structured response bytes: 19,441
- Envelope status: `ok`
- Score and verdict: `94`, `review`
- Required issue: `chair_displacement`, severity 1, review warning
- Local assessment/result validation: passed
- Deterministic derived-result equality: passed
- Stored and recomputed derived SHA-256: `9bbbdeae0af28d72f4eddf44bebe6a2c241be7382291aa2f522a7e48fe43b721`
- Result SHA-256: `182e3fd9f438f4b9df33616cd0f0936d994e5b01b9ff3735d1c89f882a4ddf30`
- Raw response SHA-256: `b720dd6c7d8234828756569d3dee6db82a0b214acc66659d091a6e41929ce0f6`
- Attempt metadata SHA-256: `d8274931bad98051cb5eaca88edde9fdb451db9a935e9178e416a76c319b9e48`

The model evaluated the partly cropped visible chair as the only plausible associated seated position. It retained `chair_displacement` because that chair is noticeably offset from the keyboard approach and an ordinary user would likely reposition it before typing. It did not invent an off-frame centered chair.

This satisfies the frozen V4.3.1 same-case quality and transport requirement. It is one calibrated development case and is not an accuracy estimate.
