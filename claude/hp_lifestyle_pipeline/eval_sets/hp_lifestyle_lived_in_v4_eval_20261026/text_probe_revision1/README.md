# Preserved first V4 text probe

Four GPT-5.5 banks (120 texts) tested compiled prompt SHA `0ce8988771298f6d7def687471fb585314626d64cec3ca2e64980692605fec60`. No images were generated. Root inspected all 120 prompt texts. This revision restored richer object state and material detail, but was not selected for the 540-text deliverable.

Findings: the wide texts sometimes introduced a fourth object through a paper towel, rag, napkin or separate note. Printer alternatives retained paperwork in too many scenes. Some surface descriptions were physically questionable (writing pressure impressions in quartz). Lexical validation also flagged `phone-room` and `desktop`; in these particular contexts they described a room and furniture surface, not visible computing devices. Revision 2 avoids those ambiguous words as well as addressing actual scene problems.

Two close banks passed automated validation; two wide banks were rejected. All four raw responses remain immutable under this archive. The archived manifest and sidecar paths record their original locations under the parent eval directory; when replaying this snapshot, map those historical eval-local paths into this archive. Original source inputs, schemas and render dependencies remain in their recorded durable locations. The archived `system_prompt.md` is the exact compiled prompt sent in these four requests.

Next bounded batch: the same four inputs against revision 2, then the remaining 14 only after review. No prompt text is repaired by hand.
