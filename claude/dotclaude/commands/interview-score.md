**DEPRECATED — use `/hiring_generate_interview_feedback` instead.**

This skill's older behavior injected a hire/advance/reject recommendation and applied the model's
own culture biases (e.g. penalizing a company-impact-over-interest motivation, and docking for the
interviewer having to prompt). Per Hooman (2026-08-04), that is wrong: the job is to **parse the
candidate's answer to every question and score correctness/evidence only — never to judge whether
to promote**, and to score culture against Hooman's stated preferences (company-impact focus is a
positive), keeping the model's biases out.

→ Run `/hiring_generate_interview_feedback <transcript>` instead. See
`~/.claude/commands/hiring_generate_interview_feedback.md`.
