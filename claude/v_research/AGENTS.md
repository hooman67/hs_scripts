# Durable Resume Rule

This is a long-running vehicle-deal research project. At the start of every new or resumed
session:

1. Read `/home/colligo/hs_scripts/claude/dotclaude/RESEARCH_RULES.md`, then `CLAUDE.md`,
   `PROJECT_STATE.md`, `DECISIONS.md`, and `LEARNINGS.md`.
2. Treat `PROJECT_STATE.md` as the exact live handoff. Continue from its next action; do not
   restart completed research.
3. Use bounded research batches and update `PROJECT_STATE.md` after every substantive batch with
   completed scope, findings, expired or sold listings, open gaps, and the next exact step.
4. Update `DECISIONS.md`, `LEARNINGS.md`, and `LONG_TERM_PLANS.md` when the work changes their
   contents. Never infer that Hooman accepted a recommendation.
5. Follow the evidence, confidence, and pricing rules in `research-plan.md`. Never treat an
   advertised price, history-report claim, dealer certification, or aggregator listing as fully
   verified without the required checks.
6. Keep files few, topic-organized, and understandable without chat history. Use one canonical
   summary per topic; store raw listing snapshots beneath the topic.
7. Parallelize only independent research when authorized. Keep scoring, synthesis, and edits to
   shared files centralized.
8. Do not contact a seller, submit personal information, apply for financing, place a deposit,
   reserve a vehicle, or make a purchase without Hooman's explicit approval.
9. Before recommending travel, re-confirm that the vehicle is available and obtain a written
   out-the-door quote and material-condition disclosures.
10. Whenever mentioning a file to Hooman, use its full absolute filesystem path.
