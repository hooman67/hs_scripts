---
name: Squad Channel Reading History
description: Tracks how far back we have read the foundry_consumer_squad Slack channel and context summary
type: project
---

**Last read date:** 2026-03-20 (read all messages Mar 9–20)
**Last message timestamp:** 1742461200 (approx Mar 20 11:20 UTC — Abhinav's message about TCCC runs hanging)
**Messages processed:** 61 top-level messages, 670 total across 37 threads
**Full analysis saved to:** /tmp/squad_channel_analysis.md

**Access:** Channel is private, on Adobe Research workspace. Must use user_token (xoxp-...) not bot token. Bot token is on Creative Cloud E2E workspace and cannot see this channel.

**Key context (Mar 9–20, 2026):**

TCCC (Coca-Cola):
- Product likeness committed to April 13 (internal Apr 8). Mar 25 in-person readout.
- Hooman cracked DAM — ~114k images downloaded Mar 20
- Synthetic product data quality poor (731 clean records after filtering). Missing refs for 8/11 new products.
- Multi-node training hangs at distributed.barrier() on new conversational branch
- Abhinav ran fallback from old branch

THD (Home Depot):
- 3 training runs targeting Mar 19–20 weekend: GR6 multiref+T2I+IE (Joshua), GW multiref+T2I+IE (Pratyusha), GW T2I+IE for TCCC (Arpit/Abhinav)
- Caption V3 approved by Harish Mar 17. GPT used for production captioning.
- Vendor multi-ref data has domain gap — only 4k THD multiref samples
- Joshua hit httpx checkpoint save error Mar 20

HUMAIN:
- Arpit training Gen 4.5 T2I for Saudi tourism. 8-node hang same as others.
- Val loss fix confirmed (val_freq was >1M → set to ~100)

Cross-customer:
- Caption format standardized on SCAP, 100% open set for type
- Multi-node distributed.barrier() hang is #1 blocker across all teams
- Dongsheng building unified rewriter starting with THD then TCCC

**How to apply:** Update this file each time the channel is read. Include the last message timestamp processed and a brief summary of new context.
