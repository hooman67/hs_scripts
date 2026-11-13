# Client Pipeline Overview (V1.8)

This document provides an **overall pipeline** for the V1.8 text-to-video model. It is divided into separate condition pipelines for **text**, **images**, and **video**, each of which feeds into the **Core model (DiT)**. Finally, a **Decoding and SSR ** is used to generate the final output video.

---

# Models Description

## V1.8 Text to Video Model Pipeline

```mermaid
flowchart LR
    %% Current V1.8 client pipeline
    
    subgraph "Image Condition Pipeline"
        I["Image"] --> A["AdobeOneImage"]
        A --> B["Image NSFW (V7)"]
        B --> C["Dentro Pre"]
    end

    subgraph "Text Condition Pipeline"
        TP["Text Prompt"] --> PF2["Prompt Forge V2"]
        PF2 --> PP["Prompt Processor"]
        PP --> T5["T5Encoder"]
    end

    subgraph "Video Condition Pipeline"
        V["Video"] --> VNSFW1["Image NSFW"]
        VNSFW1 --> SM1["VideoDepthAnything"]
        VNSFW1 --> SM2["Edge"]
        SM1["VideoDepthAnything"] --> SM3["Spacial Encoder"]
        SM2["Edge"] --> SM3["Spacial Encoder"]
    end

    %% DiT core model subgraph with distinct input/output
    subgraph "V1.8 Core model(DiT)"
        DiT_in(("Condition Inputs")) --> DiT_core["DiT Processing"]
        DiT_core --> DiT_out(("DiT Output"))
    end

    %% Wire the pipelines into DiT input
    C --> DiT_in
    T5 --> DiT_in
    SM3 --> DiT_in

    subgraph "Video Decoding Pipeline"
        DiT_out --> DEC["VAEDecoder"]
        DEC --> VNSFW2["Image NSFW"]
        VNSFW2 --> DP["Dentro Post"]
        %% SSR is optional; dotted arrow paths
        VNSFW2 -.-> SSR["SSR (Optional)"]
        SSR -.-> DP
        DP --> FV["Final Video"]
    end
