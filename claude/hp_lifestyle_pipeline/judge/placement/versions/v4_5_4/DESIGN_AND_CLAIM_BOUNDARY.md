# V4.5.4 independent-observer design and claim boundary

V4.5.4 is an unvalidated development candidate. It uses the exact root-authored functional and geometry observer prompts in this directory. The two calls are independent, disjoint, receive no scene prompt or expected answer, and are synthesized by application code. This version must pass frozen Gate A and then a separately frozen held-out Gate B before any 160-image diagnostic run.

Normal execution makes two GPT-5.5 high-reasoning calls. One shared repair permits at most one additional call for transport, JSON, schema, or semantic validation failure. The SDK has zero retries. Any exhausted failure returns an explicit `review` sentinel with `score_valid:false`.

The six Gate A examples are reused labeled development cases. Three repeats measure whether the candidate meets a prespecified diagnostic gate; they do not estimate generalization accuracy. Prompts, schemas, code, input hashes, and deterministic algorithms are frozen before any V4.5.4 model call. No target-specific visual anchor is used.
