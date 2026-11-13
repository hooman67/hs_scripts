# Durable Resume Rule

This project contains a long-running independent audit that has repeatedly crossed context
compaction boundaries. Before continuing that audit in any new or resumed session:

1. Read `AUDIT_CHECKPOINT.md` completely. Treat its "Next exact batch" section as the current
   stopping point; do not restart the repository review or repeat completed batches.
2. Use small, bounded tool calls. Keep command output below roughly 14,000 tokens, avoid broad
   recursive dumps, and do not leave the user without a brief progress update during long work.
3. After every substantive reading or verification batch, update `AUDIT_CHECKPOINT.md` with
   the completed scope, material findings, and the next exact file/line or verification step.
4. Preserve existing research files unless the user explicitly requests corrections. The
   audit checkpoint itself may be updated as working memory.
5. Do not touch unrelated changes outside this project.

This project-local rule and checkpoint are the authoritative durable memory for the audit;
client-side generated memories are only a secondary convenience.
