# v22.2 contradiction audit

- High-fill exact initial x-y is unconditional; conditional-move wording removed.
- Lower-fill alone receives free x-y translation permission.
- Support and room remain independently recomposed in both branches.
- Active branch and universal no-resize fallback are injected into Stage B and final executable prompt.
- Stage A and guide builder code remain behaviorally unchanged.

Potential contradictory phrases (expected none):
/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:100:3. The original user request, followed by defaults, wherever compatible with priorities 1 and 2.
/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:296:                "consistently in composition and the final prompt. Keep small props neutral by default. "
/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:375:                         "consistent; leave small props neutral by default. "
