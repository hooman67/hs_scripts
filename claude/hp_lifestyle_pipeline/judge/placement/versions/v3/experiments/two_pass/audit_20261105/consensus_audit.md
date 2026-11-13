# Consensus-v2 independent audit

Status: **mechanically passed, with accuracy limitations**.

Both selected runs were independently recomputed from their two-pass sources and two verifier assessments. All 244 consensus records, 1,220 merged components, scores, confidence values, issue-code selections, provenance, and final decisions exactly match the saved envelopes. The same policy and merger hashes appear in every record. The policy and merger contain no case or device mapping; case IDs are used only to join inputs and requested components.

The trigger sets were independently derived from the saved predictions and exactly match their manifests: 6 development cases / 8 components and 4 NEW160 cases / 5 components. For all 20 verifier overlays, the raw response parses exactly to the saved assessment, requested component names are exact, and the generated image bytes, twin bytes, scene-prompt hash, product type, and image stage bind to the corresponding two-pass source. Proposal-aware results bind to the exact two-pass result hash; names-only results bind to the exact trigger manifest. No human comments, prior verdicts, proposal text, codes, or severities were passed where excluded by the respective protocol.

Development-84 consensus resolves 3 components as confirmed, 4 as confidently rejected/clear-or-minor, and 1 as unconfirmed. Its verdict counts are 38 pass, 44 fail, and 2 review. The independently recomputed development checks are:

- Diagnostic verdicts: **6/11**
- Extended explicit verdicts: **2/2**
- Extended agreement with V2: **55/56**
- Sole agreement mismatch: `cashmere__laptop_FrontCloseUp__p5`, consensus review versus V2 pass

NEW160 consensus resolves 1 component as confirmed and 4 as confidently rejected/clear-or-minor. Its counts are **118 pass, 38 fail, and 4 review**, exactly matching baseline V2, with **zero V2-to-consensus verdict changes**. It reverses the original two-pass fail back to pass for `elitebook__laptop_BackRightCloseUp__p9`.

The archived v1 runs remain present with the summary hashes pinned in the v2 protocol snapshot. The v2 source-binding rebuild preserves the selected semantic fields exactly for 84/84 and 160/160 records.

The optional local FE check also passes for the consensus-v2 build: exact 160 combined IDs, 80 laptop IDs, 80 printer IDs, manifest image/twin/prompt identity, score and verdict equality, and display of both verifier checks, consensus resolution, and final decision. Its status remains `local_build_validated_not_published`.

Core consensus tests passed: **9 passed**.

These results do not establish NEW160 accuracy. The policy was selected after partial root inspection of the four NEW160 trigger cases, and NEW160 is explicitly a posthoc development probe rather than held-out validation. The only concrete human image-level finding reported to this audit is root's suspected Elitebook error; no systematic NEW160 human labels exist. Files can prove that human labels did not enter runtime inputs, but cannot prove the full history of informal inspection.
