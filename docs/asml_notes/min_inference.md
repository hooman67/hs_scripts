```markdown
## Min Inference Design Principles

1.  There are two types of MinInf pipelines:
    a.  Official minInf pipelines are the ones that have a production counterpart. These are made and maintained by ASML-Integration squad[cite: 2].
    b.  Prototype minInf pipelines are provided by researchers[cite: 3].
2.  MinInf is the gold standard for quality (so production pipelines will always have 100% parity with the official minInf for that pipeline)[cite: 3].
3.  MinInf will only contain what's needed by researchers. It will not include any complexity that is related to production needs[cite: 4].
4.  MinInf will remain as self-contained as possible. i.e. we will not add abstraction levels on top of it. No base class for min pipelines, etc[cite: 5, 6].
5.  Official MinInfs will always come with a lunch.json so that researchers can actually put breakpoints and get tensor shapes, etc.
    a.  No Colligo Tensor (only torch.Tensor)[cite: 6, 7].
6.  Regarding components:
    a.  Official MinInf pipelines will use the production components[cite: 7].
    b.  Researchers are not required to understand/modify components beyond what they need to know to use them. They can add their code directly[cite: 8, 9].

## Why asml-integration squad exists:

1.  To make sure production pipeline has quality that matches research prototypes (present ASML work in the best light)[cite: 9].
    Hand off: Minimal pipeline[cite: 10].
    ASML ensures parity between minimal and researchers., Lynn responsible for service scalability, reliability, etc. We are responsible for quality (parity with minimal)[cite: 10].
    Because right now, we do a lot of work, they get credit for it[cite: 11].
2.  To have access to rapid demos on firefly.com
    a.  Will build a quick mini colligo pipeline that connects to ff.com but uses the minimal pipeline under the hood[cite: 12]. Make minimal pipelines deployable[cite: 13].
3.  To have control over the code
    a.  We will always get pulled into debugging prod pipeline no matter what[cite: 14].
    b.  We should be code owners of minimal pipelines and everything they use (including diffusion loop, samplers, schedulers, etc)[cite: 15]. Also including anything that is used for training. And all the utilities that are used[cite: 16]. Basically, everything under old diffusion loop[cite: 17].

## Minimal Inference Immediate Tasks

* P0 --Hybrid loading: Multi source + GPU configuration (how to hit endpoint for some models and load others locally)
    * FFP-20010
* P0 -- Clean minimal inference pipelines
    * --Utility cleanup
        * FFP-20011 Sid
    * --ML logic cleanup Hooman
        * FFP-20013
    * --Breakdown into official and prototype folders
        * FFP-19547 Hooman
* P0 -- Wiki Documentation
    * FFP-19544 Aditya
* -- Common utilities P1
    * FFP-20193 Sid
* -- Batch processing - P2
    * FFP-19543 S
* -- Clio Demos cleanup
* -- Deployability (connected to ff.com for demos)
    * FFP-19542
* -- HTML generation re-design
    * FFP-20192
* -- AutoX
* -- Dependency management (how do researchers bring their deps?)
* -- SSEval
    * FFP-19546
* -- return all clineto params (entire config) with the response
* -- Make sure CI/CD has e2e test
* --compile examples of Soheil introducing last minute stuff in pipeline [cite: 18]
```