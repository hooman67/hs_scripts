# Camera-aware V2 text sample review

Local text review only. No model or image-generation call was made by this builder. The HTML companion embeds exact supplied offline reference thumbnails as base64. Missing, unknown, and incompatible references remain unavailable.

Cases included: **22**.

Optional historical reference-integrity appendix: [/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity/SUMMARY.md](../../../../reference_integrity/SUMMARY.md)

<details><summary>Review source files and hashes</summary>

```json
{
  "manifest": {
    "version": "camera-aware-v2-bounded-text-eval-2026-10-22",
    "case_count": 22,
    "model": "gpt-5.5",
    "settings": {
      "reasoning_effort": "medium",
      "max_completion_tokens": 8000,
      "temperature": "omitted",
      "strict_json_schema": true
    },
    "image_generation": false,
    "input_schema_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/input.schema.json",
    "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
    "camera_profiles_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/camera_profiles.json",
    "camera_profiles_sha256": "db77622a56357097b56a15e755e89b1ce1139f24e71d371b713f667ea42833c7",
    "source_manifest_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_manifest.json",
    "edge_manifest_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_manifest.json",
    "laptop_source_selection": {
      "source_id": "22fdbf19f03d1a31",
      "rationale": "Actual source contains concrete mobile-work and meeting cues suitable for comparing tight, medium, wide, and top-oblique behavior."
    },
    "cases": [
      {
        "case_id": "01_rich_printer_magic_back_closeup",
        "source_id": "ee810cf51bb82bb4",
        "product_name": "Magic",
        "camera_tag": "Printer_Back_CloseUp",
        "purpose": "Rich actual printer messaging under a tight level view.",
        "input_path": "inputs/01_rich_printer_magic_back_closeup.json",
        "input_raw_sha256": "41991b0dfbaa9dc0304ef5ff58054e4096faf1e795961be7bc7c6c0b0ef41c6c",
        "input_semantic_sha256": "d15009e1a42d2fb0e3097249325295c35a503cb4a03369f0826223ca478a4a53",
        "source_kind": "actual",
        "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
            "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "member": null,
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Back_CloseUp",
          "resolved_tag": "Printer_Back_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "tight",
          "elevation": "level",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "02_rich_printer_messi_back_closeup",
        "source_id": "ee810cf51bb82bb4",
        "product_name": "Messi",
        "camera_tag": "Printer_Back_CloseUp",
        "purpose": "Same source and camera as case 01; exercise the Messi close-view override.",
        "input_path": "inputs/02_rich_printer_messi_back_closeup.json",
        "input_raw_sha256": "aa1e1c8dae5cf05f4a53b9b53ad887b31a0c2bc9294eb88360e7d80f666d1804",
        "input_semantic_sha256": "586df2b469dcf2339616c26352fd38556f8477fd512f71f041a26aa96ee258b8",
        "source_kind": "actual",
        "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
            "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "member": null,
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Back_CloseUp",
          "resolved_tag": "Printer_Back_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "level",
          "requested_product": "Messi",
          "resolved_product": "Messi_Ceramic-White.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "03_rich_printer_magic_front_right_medium",
        "source_id": "ee810cf51bb82bb4",
        "product_name": "Magic",
        "camera_tag": "Printer_Front_Right_Medium",
        "purpose": "Same rich source under a medium oblique view.",
        "input_path": "inputs/03_rich_printer_magic_front_right_medium.json",
        "input_raw_sha256": "8d284c843f7d2a5c300b1dd534bccbb28e688f078794fdef1118185857482352",
        "input_semantic_sha256": "f15cf3e89e5312fe84c08b5a19f2b2658079833bea33f6a837db1062fe93e035",
        "source_kind": "actual",
        "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
            "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "member": null,
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Front_Right_Medium",
          "resolved_tag": "Printer_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "04_rich_printer_magic_front_right_wide",
        "source_id": "ee810cf51bb82bb4",
        "product_name": "Magic",
        "camera_tag": "Printer_Front_Right_Wide",
        "purpose": "Same rich source under a wide oblique view.",
        "input_path": "inputs/04_rich_printer_magic_front_right_wide.json",
        "input_raw_sha256": "bbb48142b4717a969c28cf374a00d7019615cfd30ff70aaafc54efa343de35a1",
        "input_semantic_sha256": "7cb06625ddfad1e4a549df9d7a6b9edc921b9aceb691117c52760057c4fecd84",
        "source_kind": "actual",
        "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
            "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "member": null,
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Front_Right_Wide",
          "resolved_tag": "Printer_Front_Right_Wide",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "wide",
          "elevation": "oblique",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "05_rich_printer_magic_top_front_closeup",
        "source_id": "ee810cf51bb82bb4",
        "product_name": "Magic",
        "camera_tag": "Printer_Top_Front_CloseUp",
        "purpose": "Same rich source under a tight top-oblique view.",
        "input_path": "inputs/05_rich_printer_magic_top_front_closeup.json",
        "input_raw_sha256": "d03e69638683e22e9d781e13b5867acc470c4943c61cbbf9057d3d5f99ffe059",
        "input_semantic_sha256": "fa723bc327bfa0bd1c7b9691f6599cda28bd720bfa20d224cc9ac66931ebecac",
        "source_kind": "actual",
        "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
            "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "member": null,
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Top_Front_CloseUp",
          "resolved_tag": "Printer_Top_Front_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "tight",
          "elevation": "top_oblique",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "06_actual_laptop_koki_front_closeup",
        "source_id": "22fdbf19f03d1a31",
        "product_name": "Koki",
        "camera_tag": "Laptop_Front_CloseUp",
        "purpose": "Actual mobile-work and meeting cues under a tight level view.",
        "input_path": "inputs/06_actual_laptop_koki_front_closeup.json",
        "input_raw_sha256": "9f2d6ab604f7615a73347b7cb318eb222543f98d43a5d81502ecbc0b7e1f6404",
        "input_semantic_sha256": "12503723bd33ef07e76e6e4a84d0ffe951f158f5ebe568a5dacf0b1272f18f08",
        "source_kind": "actual",
        "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
            "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "member": null,
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Front_CloseUp",
          "resolved_tag": "Laptop_Front_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "tight",
          "elevation": "level",
          "requested_product": "Koki",
          "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "07_actual_laptop_koki_front_right_medium",
        "source_id": "22fdbf19f03d1a31",
        "product_name": "Koki",
        "camera_tag": "Laptop_Front_Right_Medium",
        "purpose": "Same actual laptop source under a medium oblique view.",
        "input_path": "inputs/07_actual_laptop_koki_front_right_medium.json",
        "input_raw_sha256": "dd5e7ff6c45e9261eece9891bd939e0064487cb2f4c6c563faf222e9b62f229e",
        "input_semantic_sha256": "b4f03ba2a7783333ffe64883a732435bda7580c39b5aac68103a0c803db30ecd",
        "source_kind": "actual",
        "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
            "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "member": null,
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Front_Right_Medium",
          "resolved_tag": "Laptop_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Koki",
          "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "08_actual_laptop_koki_front_right_wide",
        "source_id": "22fdbf19f03d1a31",
        "product_name": "Koki",
        "camera_tag": "Laptop_Front_Right_Wide",
        "purpose": "Same actual laptop source under a wide oblique view.",
        "input_path": "inputs/08_actual_laptop_koki_front_right_wide.json",
        "input_raw_sha256": "c644a5aeb3cc2a685ee5b8024da9d55db59279de4d4fb2e0d6fd6935b04a3e97",
        "input_semantic_sha256": "dfe89eff1607777a7d9fac133ebac13c5a57a2eed48c08c07f5dd05a07ee6ec6",
        "source_kind": "actual",
        "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
            "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "member": null,
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Front_Right_Wide",
          "resolved_tag": "Laptop_Front_Right_Wide",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "wide",
          "elevation": "oblique",
          "requested_product": "Koki",
          "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "09_actual_laptop_koki_top_front_medium",
        "source_id": "22fdbf19f03d1a31",
        "product_name": "Koki",
        "camera_tag": "Laptop_Top_Front_Medium",
        "purpose": "Same actual laptop source under a medium top-oblique view.",
        "input_path": "inputs/09_actual_laptop_koki_top_front_medium.json",
        "input_raw_sha256": "cd27b84cce7035814e9154bb8247e24ce73503074b9d87cb84752a4122386227",
        "input_semantic_sha256": "6ff9f668ebc418476ffdf46b748691a55470c06c0fdd04aa5de11387192f0b1f",
        "source_kind": "actual",
        "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
            "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "member": null,
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Top_Front_Medium",
          "resolved_tag": "Laptop_Top_Front_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "top_oblique",
          "requested_product": "Koki",
          "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "10_actual_laptop_viktor_front_right_closeup",
        "source_id": "22fdbf19f03d1a31",
        "product_name": "Viktor",
        "camera_tag": "Laptop_Front_Right_CloseUp",
        "purpose": "Actual laptop source under the especially tight Viktor override.",
        "input_path": "inputs/10_actual_laptop_viktor_front_right_closeup.json",
        "input_raw_sha256": "d1b3c0bdf827fa92859137c81d352897c101ce5370c00b2b0bc0a5ce19f93af8",
        "input_semantic_sha256": "8acf418210d534aaedf897dcdbf3eb81072be7b0f8ea5590fddcb7154dc1c047",
        "source_kind": "actual",
        "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
            "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
            "member": null,
            "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Front_Right_CloseUp",
          "resolved_tag": "Laptop_Front_Right_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "tight",
          "elevation": "oblique",
          "requested_product": "Viktor",
          "resolved_product": "Viktor_Sahara-Silver.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "11_actual_printer_tassel_front_closeup",
        "source_id": "160db92655412f4d",
        "product_name": "Tassel",
        "camera_tag": "Printer_Front_CloseUp",
        "purpose": "Second actual printer source with the PDF-only Tassel registry entry.",
        "input_path": "inputs/11_actual_printer_tassel_front_closeup.json",
        "input_raw_sha256": "5f1f88a4f02cfc3aea84b9ed0fbc9d2705d28a89a9c3e877b8bd503d71453345",
        "input_semantic_sha256": "438b3b96fc6802fd17b066829bad717faab4c388afb036b1f0ff9645c9a8242b",
        "source_kind": "actual",
        "source_semantic_sha256": "160db92655412f4d41d349bbf6f930adc248c6485b804ff4cade8824355b5710",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/160db92655412f4d.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2299778737384020264.zip",
            "member": "Source Messaging - 71bd2bda-ecc2-4841-bd21-30a6c05673a9.json",
            "sha256": "afdf3ed48a702c2d4bb475ddd54274754fda7bebf6d542c6abb3c41624428943"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Front_CloseUp",
          "resolved_tag": "Printer_Front_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "tight",
          "elevation": "level",
          "requested_product": "Tassel",
          "resolved_product": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "12_synthetic_gaming_cheddar_front_right_wide",
        "source_id": "048217039fd093b2",
        "product_name": "Cheddar",
        "camera_tag": "Laptop_Front_Right_Wide",
        "purpose": "Synthetic grounded Gaming cues under a known wide laptop view.",
        "input_path": "inputs/12_synthetic_gaming_cheddar_front_right_wide.json",
        "input_raw_sha256": "2b67741813b00812a8f4b99d68dfeb6a003993f39e2dadfe032db676f1fafccb",
        "input_semantic_sha256": "73daac251459c36be483f6ac27385166bf439e6ac08158bde40cc44897bed6fb",
        "source_kind": "synthetic",
        "source_semantic_sha256": "048217039fd093b2ad6819c601d3e2293a8616e943eeb6b605d56e3063d9a56f",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/gaming.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/gaming.json",
            "member": null,
            "synthetic": true
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Front_Right_Wide",
          "resolved_tag": "Laptop_Front_Right_Wide",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "wide",
          "elevation": "oblique",
          "requested_product": "Cheddar",
          "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "13_empty_source_unknown_camera",
        "source_id": "44136fa355b3678a",
        "product_name": "Magic",
        "camera_tag": "Printer_Unregistered_View",
        "purpose": "Empty source plus unknown camera must use the conservative minimal fallback.",
        "input_path": "inputs/13_empty_source_unknown_camera.json",
        "input_raw_sha256": "668d28944f2236be9d4298ddc5754dc8ad9abc09908d0288d7196fa0ee7292a1",
        "input_semantic_sha256": "d82300a54459013135a546936a12997f8c06dd25c611ed8766c1453d94af535e",
        "source_kind": "synthetic",
        "source_semantic_sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/empty.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/empty.json",
            "member": null,
            "synthetic": true
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Unregistered_View",
          "resolved_tag": null,
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "unknown",
          "framing": "unknown",
          "elevation": "unknown",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "14_technical_only_known_tight_camera",
        "source_id": "49aa979045b3b3d6",
        "product_name": "Koki",
        "camera_tag": "Laptop_Back_CloseUp",
        "purpose": "Technical-only source under a known tight camera must not invent a technical scene.",
        "input_path": "inputs/14_technical_only_known_tight_camera.json",
        "input_raw_sha256": "1c43221ec3e1e2336f1cd312ab004bdc80851dda02d7265ef3170cc03698fd0b",
        "input_semantic_sha256": "53af3123f37206ffbf4acb723351eefe551d3706208fd407a2f985c1211f5180",
        "source_kind": "synthetic",
        "source_semantic_sha256": "49aa979045b3b3d63ccf450a1267d24a849fe23da3777dcc2281b1f951911bdf",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/technical_only.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/technical_only.json",
            "member": null,
            "synthetic": true
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Back_CloseUp",
          "resolved_tag": "Laptop_Back_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "tight",
          "elevation": "level",
          "requested_product": "Koki",
          "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "15_known_type_conflict_magic_laptop_camera",
        "source_id": "ee810cf51bb82bb4",
        "product_name": "Magic",
        "camera_tag": "Laptop_Back_CloseUp",
        "purpose": "Known printer product with a known laptop camera must resolve as incompatible.",
        "input_path": "inputs/15_known_type_conflict_magic_laptop_camera.json",
        "input_raw_sha256": "a9da453e292578696b7bc658d3ff951014ed9ea664b2a7d39904f456da499b8a",
        "input_semantic_sha256": "8efbbb838b545dd836b801234af8a36f1ad805a10c993ffb313303a9e0b4cda2",
        "source_kind": "actual",
        "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
            "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "member": null,
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Back_CloseUp",
          "resolved_tag": "Laptop_Back_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "unknown",
          "elevation": "unknown",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "incompatible"
        }
      },
      {
        "case_id": "16_unknown_product_known_printer_camera",
        "source_id": "ee810cf51bb82bb4",
        "product_name": "Unregistered_Product",
        "camera_tag": "Printer_Back_CloseUp",
        "purpose": "Unknown product with a known camera must use the conservative camera base.",
        "input_path": "inputs/16_unknown_product_known_printer_camera.json",
        "input_raw_sha256": "3ab6114f20d62e1f85515e882cf1768919472470a56bdf8d3b8056857b4e1886",
        "input_semantic_sha256": "751484e7da07a89980b5ca5311e801e5818634e87b8b0568eb6fbf72e07f21f3",
        "source_kind": "actual",
        "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
            "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
            "member": null,
            "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Back_CloseUp",
          "resolved_tag": "Printer_Back_CloseUp",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "tight",
          "elevation": "level",
          "requested_product": "Unregistered_Product",
          "resolved_product": null,
          "product_resolution": "unknown"
        }
      },
      {
        "case_id": "17_actual_laptop_cashmere_front_right_medium",
        "source_id": "d60e13e4457fd44c",
        "product_name": "Cashmere",
        "camera_tag": "Laptop_Front_Right_Medium",
        "purpose": "Previously uncovered actual convertible-laptop source under a medium oblique view.",
        "input_path": "inputs/17_actual_laptop_cashmere_front_right_medium.json",
        "input_raw_sha256": "5c1d50f3fc1afe9d7fed7e1e1fe81595ee7a72db242895ec888dca9c393f8d5c",
        "input_semantic_sha256": "60454fb0f7273f3b23b84ce25bcd343242526055131e2164746857d013e90a13",
        "source_kind": "actual",
        "source_semantic_sha256": "d60e13e4457fd44cf5b7f89a6e754211bfe13d5dcd4c368f30d484ab85c65812",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/d60e13e4457fd44c.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2703900895627379394.zip",
            "member": "Source Messaging - 8e56189b-2c04-4066-bd8c-08fb6359588d.json",
            "sha256": "a61986ad16478088e9290cb1ebb44520e91e206c45b6b5e2cc11f12b3a354ca6"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 8e56189b-2c04-4066-bd8c-08fb6359588d.json",
            "member": null,
            "sha256": "a61986ad16478088e9290cb1ebb44520e91e206c45b6b5e2cc11f12b3a354ca6"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Front_Right_Medium",
          "resolved_tag": "Laptop_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Cashmere",
          "resolved_product": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "18_actual_laptop_cheddar_front_right_medium",
        "source_id": "fecec52a5c57c7bb",
        "product_name": "Cheddar",
        "camera_tag": "Laptop_Front_Right_Medium",
        "purpose": "Previously uncovered actual mobile-work laptop source under a medium oblique view.",
        "input_path": "inputs/18_actual_laptop_cheddar_front_right_medium.json",
        "input_raw_sha256": "86ba92602d75078017c8c872fca4b93d90301f6e5d5d46624c1e5f4e371093f3",
        "input_semantic_sha256": "894549da15db55e8bbfc829ed2a489a67d4c5f1cc4abb289136b3d29a42fe0fb",
        "source_kind": "actual",
        "source_semantic_sha256": "fecec52a5c57c7bb45dedfc39771fa53a1af96e1abdde37fa8a1bb3420af2fb4",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/fecec52a5c57c7bb.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2745132682490047977.zip",
            "member": "Source Messaging - 44b611c4-b58f-4614-a9e0-81a3d669f1d3.json",
            "sha256": "fd5ba38ec95e50344ac856198f7dccdb6ce43a6f946c5fcd8b3ae9bb2a32ccaa"
          }
        ],
        "expected_camera": {
          "requested_tag": "Laptop_Front_Right_Medium",
          "resolved_tag": "Laptop_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Cheddar",
          "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "19_actual_printer_magic_front_right_medium",
        "source_id": "8bbf8af1d8cbf4b2",
        "product_name": "Magic",
        "camera_tag": "Printer_Front_Right_Medium",
        "purpose": "Previously uncovered actual ink-tank printer source under a medium oblique view.",
        "input_path": "inputs/19_actual_printer_magic_front_right_medium.json",
        "input_raw_sha256": "749067a68237d200747fd6c07e49d859bcb4660a7cc3d7976a80cd4737226d76",
        "input_semantic_sha256": "f3ff9ef6779f3f196e0d339c1cbcc1690b9af628a986ed1b5ecb3d2b0fc69c04",
        "source_kind": "actual",
        "source_semantic_sha256": "8bbf8af1d8cbf4b2d70c755d9cec9030e658408f2076733d8407fbf710863935",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/8bbf8af1d8cbf4b2.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK4748855972432039582.zip",
            "member": "Source Messaging - 8a8e84ff-69e1-4581-a1ca-8eb411354a2a.json",
            "sha256": "fe8d1dc26056d55824e19fce50385c446f6a307feed7d72c0cc85916d07bb688"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Front_Right_Medium",
          "resolved_tag": "Printer_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "20_actual_printer_messi_front_right_medium",
        "source_id": "8189f3ad5af37a81",
        "product_name": "Messi",
        "camera_tag": "Printer_Front_Right_Medium",
        "purpose": "Previously uncovered actual shared-space printer source under a medium oblique view.",
        "input_path": "inputs/20_actual_printer_messi_front_right_medium.json",
        "input_raw_sha256": "6d96bb8b09532d60a12f30a1131c99797a68d6374043d9c6613d4e4ad40dc608",
        "input_semantic_sha256": "e674f69f73dee0826312d0d44ea0faaa0fe1feaddbdfc5d216c60207ecafb5ae",
        "source_kind": "actual",
        "source_semantic_sha256": "8189f3ad5af37a814b680c32ab1023a762aefbfc1c75d0f5d958ff4a6849dd2d",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/8189f3ad5af37a81.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK881963376314406021.zip",
            "member": "Source Messaging - cb0d856e-5f4e-4928-bb04-1dd770c491d1.json",
            "sha256": "3be81e2250494efef3678e51095f9356e52c32ce744c5659b6b05e3a3f5b8d06"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Front_Right_Medium",
          "resolved_tag": "Printer_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Messi",
          "resolved_product": "Messi_Ceramic-White.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "21_actual_printer_magic_enterprise_front_right_medium",
        "source_id": "324b14a617dfedba",
        "product_name": "Magic",
        "camera_tag": "Printer_Front_Right_Medium",
        "purpose": "Previously uncovered actual enterprise-printer source under a medium oblique view.",
        "input_path": "inputs/21_actual_printer_magic_enterprise_front_right_medium.json",
        "input_raw_sha256": "fa6a8903d7ef9eea25b37eb3305cadeb4cda27f2d92726f4e04db93bfd8096d4",
        "input_semantic_sha256": "9b63267e4b9ea06219a285c929135adaf8399c7100896e1d49b1e92102c0d853",
        "source_kind": "actual",
        "source_semantic_sha256": "324b14a617dfedbaa74ed0f14b93d038737a01c1fa6180a9af37de60905f53a9",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/324b14a617dfedba.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK901460674462796743.zip",
            "member": "Source Messaging - 27735f23-c479-4d5b-8951-cdf900133f0b.json",
            "sha256": "8ba3311a2196b3f0059c6f703fc260dc14f0fce1889420fe80a99c4e4c0087f4"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Front_Right_Medium",
          "resolved_tag": "Printer_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Magic",
          "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
          "product_resolution": "alias"
        }
      },
      {
        "case_id": "22_actual_printer_messi_ink_tank_front_right_medium",
        "source_id": "943faef0af11484f",
        "product_name": "Messi",
        "camera_tag": "Printer_Front_Right_Medium",
        "purpose": "Previously uncovered actual ink-tank all-in-one source under a medium oblique view.",
        "input_path": "inputs/22_actual_printer_messi_ink_tank_front_right_medium.json",
        "input_raw_sha256": "e48ba726b349e11728def96930422dc0399d8ff8ebfe7fe984e6058cf423e246",
        "input_semantic_sha256": "58447acc50e22d9e333ccfafc018b6c134b0a9c1bf7db79fc448ed6d224be89b",
        "source_kind": "actual",
        "source_semantic_sha256": "943faef0af11484f5bee2a60f6bb25ac7d70ee4ab00c220b2ff1e599e2eb58cf",
        "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/943faef0af11484f.json",
        "source_origins": [
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK9166360275256369928.zip",
            "member": "Source Messaging - 784a9ea4-d2b6-4465-a642-ea40c1f18408.json",
            "sha256": "f2736e7d3a5802d1e78591be6f3c003446d458c22981b6ee3b990962920a91ac"
          },
          {
            "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 784a9ea4-d2b6-4465-a642-ea40c1f18408 (1).json",
            "member": null,
            "sha256": "f2736e7d3a5802d1e78591be6f3c003446d458c22981b6ee3b990962920a91ac"
          }
        ],
        "expected_camera": {
          "requested_tag": "Printer_Front_Right_Medium",
          "resolved_tag": "Printer_Front_Right_Medium",
          "profile_version": "camera-v2-draft-2026-10-22",
          "resolution": "exact",
          "framing": "medium",
          "elevation": "oblique",
          "requested_product": "Messi",
          "resolved_product": "Messi_Ceramic-White.printer.usdz",
          "product_resolution": "alias"
        }
      }
    ]
  },
  "manifest_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/manifest.json",
  "manifest_sha256": "a6750b3f3034a80926c0519f4651865f3c48c5544bb63e1a742aeb17f08ca9e1",
  "registry_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/camera_profiles.json",
  "registry_sha256": "db77622a56357097b56a15e755e89b1ce1139f24e71d371b713f667ea42833c7",
  "catalog_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware/data/camera_catalog.json",
  "catalog_sha256": "9cd0b23dd19161c0c085df60eee0a7b32f94b3d7422036b6ccdb327c3a710ff5",
  "validation_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/validation.json",
  "validation_sha256": "261e40c6377a65625350ab94b7798edfaacc06e62a925d219c8755e48ab6b2b1",
  "missing_cases": []
}
```

</details>

## 01_rich_printer_magic_back_closeup

Rich actual printer messaging under a tight level view.

- Requested product: `Magic`
- Requested camera: `Printer_Back_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A practical office work surface in pale wood, kept clear under soft daylight with a plain neutral backdrop.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Back_CloseUp",
  "resolved_tag": "Printer_Back_CloseUp",
  "resolution": "exact",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Back_CloseUp",
  "effective_profile": {
    "framing": "tight",
    "elevation": "level",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Back_CloseUp.png`

SHA-256: `d76ed540e3c7c386ad412414996c62c1d26d35db140034b0d8f18e6766b2f2e0`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "source_camera_name": "Back_CloseUp",
  "catalog": {
    "device_id": "camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "camera_name_exact": "Back_CloseUp",
    "zip_filename": "Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Back_CloseUp.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Back_CloseUp.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 145310,
    "sha256": "d76ed540e3c7c386ad412414996c62c1d26d35db140034b0d8f18e6766b2f2e0",
    "zip_crc32": "bbb6b070"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Back_CloseUp.png",
    "bytes": 145310,
    "sha256": "d76ed540e3c7c386ad412414996c62c1d26d35db140034b0d8f18e6766b2f2e0",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Included ink value\n\nOR\n\nPrint longer between refills",
      "long_message_best_sku": "Print longer with fewer refill interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "long_message_safe_to_inherit": "Print longer with fewer refill interruptions. This HP Smart Tank all-in-one includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "mid_length": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "mid_length_safe_to_inherit": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "short_message": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "ultra_short": "Fewer refill interruptions",
      "ultra_short_safe_to_inherit": "Fewer refill interruptions"
    },
    "KSP2": {
      "headline": "Ready for recurring print work\n\nOR\n\nEveryday output that keeps moving",
      "long_message_best_sku": "Keep recurring print work moving through busy stretches. HP Smart Tank 7602 All-in-One is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "long_message_safe_to_inherit": "Keep recurring print work moving through busy stretches. This HP Smart Tank all-in-one is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "mid_length": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "mid_length_safe_to_inherit": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "short_message": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "short_message_safe_to_inherit": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "ultra_short": "Everyday productivity",
      "ultra_short_safe_to_inherit": "Everyday productivity"
    },
    "KSP3": {
      "headline": "Less handling for longer tasks\n\nOR\n\nMulti-page work made easier",
      "long_message_best_sku": "Move through multi-page tasks with fewer manual steps. HP Smart Tank 7602 All-in-One pairs a 35-page auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "long_message_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. This HP Smart Tank all-in-one pairs an auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "mid_length": "Move through multi-page tasks with fewer manual steps. A 35-page auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "mid_length_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. An auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "short_message": "A 35-page auto document feeder and automatic two-sided printing reduce manual handling.",
      "short_message_safe_to_inherit": "An auto document feeder and automatic two-sided printing reduce manual handling.",
      "ultra_short": "Fewer manual steps",
      "ultra_short_safe_to_inherit": "Fewer manual steps"
    },
    "KSP4": {
      "headline": "Connections that fit your setup\n\nOR\n\nFlexible ways to get printing",
      "long_message_best_sku": "Connect the way your devices work. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "long_message_safe_to_inherit": "Connect the way your devices work. This HP Smart Tank all-in-one supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "mid_length": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "mid_length_safe_to_inherit": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "short_message": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "short_message_safe_to_inherit": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "ultra_short": "Flexible connections",
      "ultra_short_safe_to_inherit": "Flexible connections"
    },
    "ValueProposition": {
      "headline": "Print more with fewer interruptions",
      "long_message_best_sku": "Keep recurring print, scan, copy, and fax work moving with a high-capacity all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. HP Smart Tank 7602 All-in-One pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, a 35-page auto document feeder, fax, and a 3-inch touchscreen, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "long_message_safe_to_inherit": "Keep recurring print, scan, copy, and fax work moving with a high-capacity HP Smart Tank all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. It pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, an auto document feeder, fax, and touchscreen control, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "mid_length": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "mid_length_safe_to_inherit": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "short_message": "Included ink, workflow tools, and flexible connections keep recurring printing moving.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0d2b454316ccbd87006aa461cfe69c81978dbfd3b1d9a87744",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Magic",
  "camera_tag": "Printer_Back_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging contains four numbered KSPs and a ValueProposition. The strongest concrete cues are recurring paperwork, forms, records, handouts, everyday admin work, desks, and business paperwork; technical ink, feeder, duplex, and connectivity claims were not translated into visible hardware details.",
  "count_explanation": "Several KSPs point to overlapping recurring document and admin workflows, so they were combined into one Office prompt. The selected tight, level back close-up permits no props or background details, so paperwork cues were reduced to a clear local work surface and light.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring document and color jobs"
        },
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "finishing the pages you need"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The recurring page-work cue supports an office work setting, but visible pages or supplies were omitted because the effective tight view allows no props."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, records, handouts, and color materials"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "regular document production"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Concrete document-production cues informed the practical office surface. Specific forms, records, and handouts were not requested as visible props due to the tight level profile."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "forms, records, and everyday admin work easier to complete at the desk"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The desk-based admin cue directly supports the Office environment, simplified to a clear work surface because no local props are permitted."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "nearby devices or a shared network"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "phones, laptops, and desks"
        }
      ],
      "prompt_ids": [],
      "explanation": "Connectivity and nearby-device language is mainly technical. It was not used because the prompt cannot mention or add computing hardware, and the tight view allows no props."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "regular document queues, household administration, and everyday business paperwork"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The broader proposition reinforces a regular paperwork context, expressed as a modest office work surface rather than visible document stacks or extra equipment."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wood surface, soft daylight, and a plain neutral backdrop are plausible ordinary setting details added to ground the scene without exceeding the tight-view limits."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "visible forms, records, handouts, and page stacks",
          "nearby phones, shared-network cues, and other devices",
          "people, room fixtures, and background office details"
        ],
        "explanation": "The resolved Printer_Back_CloseUp profile for the Magic product is a tight, level view with zero local props and zero background details. The prompt retains only the source-supported office paperwork context through a clear local surface and simple daylight."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "ff37be59325baaf7f13a2fcd692dd34ba642b20b45c8cc766341843fa57783bd",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "input_raw_sha256": "41991b0dfbaa9dc0304ef5ff58054e4096faf1e795961be7bc7c6c0b0ef41c6c",
  "recorded_input_semantic_sha256": "d15009e1a42d2fb0e3097249325295c35a503cb4a03369f0826223ca478a4a53",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvsEwvUyPTVnajHzNsgVdIFPI0Je",
  "usage": {
    "completion_tokens": 1916,
    "prompt_tokens": 13014,
    "total_tokens": 14930,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 0,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 330,
      "engine_ttlt_ms": 18594,
      "pre_inference_ms": 373,
      "service_tbt_ms": 9,
      "service_ttft_ms": 1175,
      "service_ttlt_ms": 19370,
      "user_visible_ttft_ms": 801
    }
  },
  "attempt": 1,
  "latency_seconds": 20.65,
  "started_at": "2026-10-22T22:48:29.231947+00:00",
  "completed_at": "2026-10-22T22:48:49.882729+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "01_rich_printer_magic_back_closeup",
  "source_id": "ee810cf51bb82bb4",
  "product_name": "Magic",
  "camera_tag": "Printer_Back_CloseUp",
  "purpose": "Rich actual printer messaging under a tight level view.",
  "input_path": "inputs/01_rich_printer_magic_back_closeup.json",
  "input_raw_sha256": "41991b0dfbaa9dc0304ef5ff58054e4096faf1e795961be7bc7c6c0b0ef41c6c",
  "input_semantic_sha256": "d15009e1a42d2fb0e3097249325295c35a503cb4a03369f0826223ca478a4a53",
  "source_kind": "actual",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
      "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "member": null,
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "01_rich_printer_magic_back_closeup",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/01_rich_printer_magic_back_closeup.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 18,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 3,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 02_rich_printer_messi_back_closeup

Same source and camera as case 01; exercise the Messi close-view override.

- Requested product: `Messi`
- Requested camera: `Printer_Back_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A tidy office work surface in pale wood, with a compact stack of forms and color handouts beside a single pen. A low file tray sits softly behind in daylight.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Back_CloseUp",
  "resolved_tag": "Printer_Back_CloseUp",
  "resolution": "exact",
  "requested_product": "Messi",
  "resolved_product": "Messi_Ceramic-White.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Back_CloseUp",
  "effective_profile": {
    "framing": "medium",
    "elevation": "level",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "omit"
  },
  "applied_overrides": [
    {
      "product_name": "Messi_Ceramic-White.printer.usdz",
      "camera_tag": "Printer_Back_CloseUp",
      "replacements": {
        "framing": "medium",
        "max_local_props": 2,
        "max_background_details": 1,
        "people_policy": "omit"
      },
      "reason": "Unlike Magic/Tassel, supplied regular Messi close views show a small product with broad surrounding margins. Allow one extra modest cue, but do not fill all blank space, enlarge the product, or add prominent people. These are offline qualitative limits, not occupancy-derived capacity."
    }
  ],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Back_CloseUp.png`

SHA-256: `5b5d3b0ec8c38cccbfac113238ebe767b219734615d2d4600ffa68a7cde93a9d`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Messi_Ceramic-White.printer.usdz",
  "source_camera_name": "Back_CloseUp",
  "catalog": {
    "device_id": "camera_printer.locator_Messi_Ceramic-White.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Messi_Ceramic-White.printer.usdz",
    "camera_name_exact": "Back_CloseUp",
    "zip_filename": "Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Back_CloseUp.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Back_CloseUp.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 32465,
    "sha256": "5b5d3b0ec8c38cccbfac113238ebe767b219734615d2d4600ffa68a7cde93a9d",
    "zip_crc32": "ebddac10"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Back_CloseUp.png",
    "bytes": 32465,
    "sha256": "5b5d3b0ec8c38cccbfac113238ebe767b219734615d2d4600ffa68a7cde93a9d",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Included ink value\n\nOR\n\nPrint longer between refills",
      "long_message_best_sku": "Print longer with fewer refill interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "long_message_safe_to_inherit": "Print longer with fewer refill interruptions. This HP Smart Tank all-in-one includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "mid_length": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "mid_length_safe_to_inherit": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "short_message": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "ultra_short": "Fewer refill interruptions",
      "ultra_short_safe_to_inherit": "Fewer refill interruptions"
    },
    "KSP2": {
      "headline": "Ready for recurring print work\n\nOR\n\nEveryday output that keeps moving",
      "long_message_best_sku": "Keep recurring print work moving through busy stretches. HP Smart Tank 7602 All-in-One is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "long_message_safe_to_inherit": "Keep recurring print work moving through busy stretches. This HP Smart Tank all-in-one is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "mid_length": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "mid_length_safe_to_inherit": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "short_message": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "short_message_safe_to_inherit": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "ultra_short": "Everyday productivity",
      "ultra_short_safe_to_inherit": "Everyday productivity"
    },
    "KSP3": {
      "headline": "Less handling for longer tasks\n\nOR\n\nMulti-page work made easier",
      "long_message_best_sku": "Move through multi-page tasks with fewer manual steps. HP Smart Tank 7602 All-in-One pairs a 35-page auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "long_message_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. This HP Smart Tank all-in-one pairs an auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "mid_length": "Move through multi-page tasks with fewer manual steps. A 35-page auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "mid_length_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. An auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "short_message": "A 35-page auto document feeder and automatic two-sided printing reduce manual handling.",
      "short_message_safe_to_inherit": "An auto document feeder and automatic two-sided printing reduce manual handling.",
      "ultra_short": "Fewer manual steps",
      "ultra_short_safe_to_inherit": "Fewer manual steps"
    },
    "KSP4": {
      "headline": "Connections that fit your setup\n\nOR\n\nFlexible ways to get printing",
      "long_message_best_sku": "Connect the way your devices work. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "long_message_safe_to_inherit": "Connect the way your devices work. This HP Smart Tank all-in-one supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "mid_length": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "mid_length_safe_to_inherit": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "short_message": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "short_message_safe_to_inherit": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "ultra_short": "Flexible connections",
      "ultra_short_safe_to_inherit": "Flexible connections"
    },
    "ValueProposition": {
      "headline": "Print more with fewer interruptions",
      "long_message_best_sku": "Keep recurring print, scan, copy, and fax work moving with a high-capacity all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. HP Smart Tank 7602 All-in-One pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, a 35-page auto document feeder, fax, and a 3-inch touchscreen, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "long_message_safe_to_inherit": "Keep recurring print, scan, copy, and fax work moving with a high-capacity HP Smart Tank all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. It pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, an auto document feeder, fax, and touchscreen control, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "mid_length": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "mid_length_safe_to_inherit": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "short_message": "Included ink, workflow tools, and flexible connections keep recurring printing moving.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0d2b454316ccbd87006aa461cfe69c81978dbfd3b1d9a87744",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Messi",
  "camera_tag": "Printer_Back_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging provides concrete recurring paperwork, forms, records, handouts, and desk admin cues. Connectivity and refill-value claims are mostly nonvisual, so the scene stays local and paperwork-focused.",
  "count_explanation": "Three KSPs supplied useful explicit scene or activity cues, but they overlap around recurring document work and desk administration. One prompt covers the strongest compatible setting without crowding the medium level view.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring document and color jobs"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Represented through recurring paperwork and color handouts. Ink supply and refill interruption claims were omitted as nonvisual product benefits."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, records, handouts, and color materials"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Forms and color handouts directly informed the compact paper stack on the local office surface."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "forms, records, and everyday admin work easier to complete at the desk"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Everyday desk administration is simplified into a tidy office work surface with paperwork and a pen, avoiding product-handling specifics."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "nearby devices or a shared network"
        }
      ],
      "prompt_ids": [],
      "explanation": "Connectivity, phones, laptops, and shared networks are not useful visible cues here and would require extra computing hardware or abstract network imagery, so they were omitted."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "regular document queues, household administration, and everyday business paperwork"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The broader value proposition supports an office paperwork context, narrowed to a local surface compatible with the selected view."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wood surface, single pen, low file tray, and daylight are ordinary invented details used to make the source-supported paperwork setting believable while staying within prop and background limits."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "level",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "refillable tank and included ink claims",
          "hardware workflow details such as feeder and two-sided output",
          "phones, laptops, shared-network connectivity",
          "broader household and business administration queues"
        ],
        "explanation": "The Messi alias resolves to the registered printer product, and its Back CloseUp override allows a medium local scene with at most two nearby props and one background detail while omitting people. The prompt keeps two nearby props, a paper stack and pen, plus one subdued file-tray background detail."
      }
    ],
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "2f452ed3271d1cf9f491d74f560543a31fa339db6338a234401f2a3dc07309b0",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "input_raw_sha256": "aa1e1c8dae5cf05f4a53b9b53ad887b31a0c2bc9294eb88360e7d80f666d1804",
  "recorded_input_semantic_sha256": "586df2b469dcf2339616c26352fd38556f8477fd512f71f041a26aa96ee258b8",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvsYyWur3XrTQNp90WBdhPbFu82v",
  "usage": {
    "completion_tokens": 2351,
    "prompt_tokens": 13015,
    "total_tokens": 15366,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1537,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 12544,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 330,
      "engine_ttlt_ms": 24095,
      "pre_inference_ms": 144,
      "service_tbt_ms": 10,
      "service_ttft_ms": 1084,
      "service_ttlt_ms": 24845,
      "user_visible_ttft_ms": 940
    }
  },
  "attempt": 1,
  "latency_seconds": 25.576,
  "started_at": "2026-10-22T22:48:49.907646+00:00",
  "completed_at": "2026-10-22T22:49:15.483537+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "02_rich_printer_messi_back_closeup",
  "source_id": "ee810cf51bb82bb4",
  "product_name": "Messi",
  "camera_tag": "Printer_Back_CloseUp",
  "purpose": "Same source and camera as case 01; exercise the Messi close-view override.",
  "input_path": "inputs/02_rich_printer_messi_back_closeup.json",
  "input_raw_sha256": "aa1e1c8dae5cf05f4a53b9b53ad887b31a0c2bc9294eb88360e7d80f666d1804",
  "input_semantic_sha256": "586df2b469dcf2339616c26352fd38556f8477fd512f71f041a26aa96ee258b8",
  "source_kind": "actual",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
      "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "member": null,
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "level",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "02_rich_printer_messi_back_closeup",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/02_rich_printer_messi_back_closeup.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 30,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 3,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "level",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "level",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 03_rich_printer_magic_front_right_medium

Same rich source under a medium oblique view.

- Requested product: `Magic`
- Requested camera: `Printer_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A practical office work surface in light wood, with a compact stack of forms and a single pen. A softly blurred filing tray adds recurring-paperwork context in diffuse daylight.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Front_Right_Medium",
  "resolved_tag": "Printer_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png`

SHA-256: `66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 79199,
    "sha256": "66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda",
    "zip_crc32": "6993477e"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "bytes": 79199,
    "sha256": "66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Included ink value\n\nOR\n\nPrint longer between refills",
      "long_message_best_sku": "Print longer with fewer refill interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "long_message_safe_to_inherit": "Print longer with fewer refill interruptions. This HP Smart Tank all-in-one includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "mid_length": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "mid_length_safe_to_inherit": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "short_message": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "ultra_short": "Fewer refill interruptions",
      "ultra_short_safe_to_inherit": "Fewer refill interruptions"
    },
    "KSP2": {
      "headline": "Ready for recurring print work\n\nOR\n\nEveryday output that keeps moving",
      "long_message_best_sku": "Keep recurring print work moving through busy stretches. HP Smart Tank 7602 All-in-One is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "long_message_safe_to_inherit": "Keep recurring print work moving through busy stretches. This HP Smart Tank all-in-one is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "mid_length": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "mid_length_safe_to_inherit": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "short_message": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "short_message_safe_to_inherit": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "ultra_short": "Everyday productivity",
      "ultra_short_safe_to_inherit": "Everyday productivity"
    },
    "KSP3": {
      "headline": "Less handling for longer tasks\n\nOR\n\nMulti-page work made easier",
      "long_message_best_sku": "Move through multi-page tasks with fewer manual steps. HP Smart Tank 7602 All-in-One pairs a 35-page auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "long_message_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. This HP Smart Tank all-in-one pairs an auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "mid_length": "Move through multi-page tasks with fewer manual steps. A 35-page auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "mid_length_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. An auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "short_message": "A 35-page auto document feeder and automatic two-sided printing reduce manual handling.",
      "short_message_safe_to_inherit": "An auto document feeder and automatic two-sided printing reduce manual handling.",
      "ultra_short": "Fewer manual steps",
      "ultra_short_safe_to_inherit": "Fewer manual steps"
    },
    "KSP4": {
      "headline": "Connections that fit your setup\n\nOR\n\nFlexible ways to get printing",
      "long_message_best_sku": "Connect the way your devices work. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "long_message_safe_to_inherit": "Connect the way your devices work. This HP Smart Tank all-in-one supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "mid_length": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "mid_length_safe_to_inherit": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "short_message": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "short_message_safe_to_inherit": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "ultra_short": "Flexible connections",
      "ultra_short_safe_to_inherit": "Flexible connections"
    },
    "ValueProposition": {
      "headline": "Print more with fewer interruptions",
      "long_message_best_sku": "Keep recurring print, scan, copy, and fax work moving with a high-capacity all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. HP Smart Tank 7602 All-in-One pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, a 35-page auto document feeder, fax, and a 3-inch touchscreen, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "long_message_safe_to_inherit": "Keep recurring print, scan, copy, and fax work moving with a high-capacity HP Smart Tank all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. It pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, an auto document feeder, fax, and touchscreen control, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "mid_length": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "mid_length_safe_to_inherit": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "short_message": "Included ink, workflow tools, and flexible connections keep recurring printing moving.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0d2b454316ccbd87006aa461cfe69c81978dbfd3b1d9a87744",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging provides concrete recurring paperwork, forms, records, handouts, admin work, and desk/setup cues. Product resolved by explicit alias to a printer product, and the requested printer camera is supported.",
  "count_explanation": "Four numbered KSPs are present, but their useful visual cues overlap around recurring paperwork and desk-based administration. One prompt preserves the strongest compatible setting without crowding the medium oblique view.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring document and color jobs"
        },
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "finishing the pages you need"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Recurring document output is represented by a compact paperwork stack. Ink supply and refill messaging was omitted because it is a product feature, not a visible setting cue."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, records, handouts, and color materials"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "regular document production"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Forms and recurring document production directly inform the office paperwork surface and background filing tray."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "forms, records, and everyday admin work easier to complete at the desk"
        },
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "multi-page tasks"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Desk-based admin work is simplified into nearby forms and a pen. Hardware handling features were not translated into visible product interactions."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "everyday setups"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "desks"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The everyday desk setup supports the office surface choice, but connectivity, devices, and shared networks are mostly abstract or would require extra hardware props, so they do not justify a separate prompt."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "paperwork, forms, records, and color documents"
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "regular document queues, household administration, and everyday business paperwork"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The value proposition reinforces a recurring paperwork context, carried into one concise office prompt."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Light wood work surface chosen as a plausible neutral office material.",
        "Single pen added as a modest admin prop within the two-prop limit.",
        "Softly blurred filing tray added as one subordinate background detail.",
        "Diffuse daylight added for believable illumination."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "ink tanks and refill interruptions",
          "monthly duty cycle and print speeds",
          "ADF, duplexing, fax, touchscreen, and other product controls",
          "phones, laptops, shared networks, and connectivity details",
          "people or multi-user activity"
        ],
        "explanation": "The medium oblique printer view permits a local setting with at most two nearby props and one simple background detail. The prompt keeps forms, a pen, and one filing-tray cue while avoiding extra devices, people, or a wider office layout."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "318edfd0d0a88cbfc5a139189dc24b1234b55854abb38e291390f5554cf1f7fc",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "input_raw_sha256": "8d284c843f7d2a5c300b1dd534bccbb28e688f078794fdef1118185857482352",
  "recorded_input_semantic_sha256": "f15cf3e89e5312fe84c08b5a19f2b2658079833bea33f6a837db1062fe93e035",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvsxxT14YtXvLAWA7CN1t4POrK6G",
  "usage": {
    "completion_tokens": 2387,
    "prompt_tokens": 13016,
    "total_tokens": 15403,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1448,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 12544,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 336,
      "engine_ttlt_ms": 23346,
      "pre_inference_ms": 257,
      "service_tbt_ms": 10,
      "service_ttft_ms": 1088,
      "service_ttlt_ms": 24055,
      "user_visible_ttft_ms": 830
    }
  },
  "attempt": 1,
  "latency_seconds": 25.615,
  "started_at": "2026-10-22T22:49:15.508147+00:00",
  "completed_at": "2026-10-22T22:49:41.123709+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "03_rich_printer_magic_front_right_medium",
  "source_id": "ee810cf51bb82bb4",
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Medium",
  "purpose": "Same rich source under a medium oblique view.",
  "input_path": "inputs/03_rich_printer_magic_front_right_medium.json",
  "input_raw_sha256": "8d284c843f7d2a5c300b1dd534bccbb28e688f078794fdef1118185857482352",
  "input_semantic_sha256": "f15cf3e89e5312fe84c08b5a19f2b2658079833bea33f6a837db1062fe93e035",
  "source_kind": "actual",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
      "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "member": null,
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "03_rich_printer_magic_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/03_rich_printer_magic_front_right_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 29,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 3,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 04_rich_printer_magic_front_right_wide

Same rich source under a wide oblique view.

- Requested product: `Magic`
- Requested camera: `Printer_Front_Right_Wide`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A shared office worktable with a matte laminate surface, a compact stack of completed forms, a labeled folder, and a single pen. A neutral partition and soft seating edge sit quietly in the background under diffuse daylight.

**p2 · Education**

A school preparation table with light wood grain, a small stack of handouts, a marked worksheet, and one pen. A softly blurred bulletin board and chair back add classroom context in daylight.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Front_Right_Wide",
  "resolved_tag": "Printer_Front_Right_Wide",
  "resolution": "exact",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Front_Right_Wide",
  "effective_profile": {
    "framing": "wide",
    "elevation": "oblique",
    "max_local_props": 3,
    "max_background_details": 2,
    "people_policy": "optional_if_supported_and_unobtrusive"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Wide.png`

SHA-256: `917ad50f81d97c676d22ea0724d536a1d59f71edd7d87afe27c25eb8fb227743`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "source_camera_name": "Front_Right_Wide",
  "catalog": {
    "device_id": "camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "camera_name_exact": "Front_Right_Wide",
    "zip_filename": "Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Wide.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Wide.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 50431,
    "sha256": "917ad50f81d97c676d22ea0724d536a1d59f71edd7d87afe27c25eb8fb227743",
    "zip_crc32": "e04f4567"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Wide.png",
    "bytes": 50431,
    "sha256": "917ad50f81d97c676d22ea0724d536a1d59f71edd7d87afe27c25eb8fb227743",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Included ink value\n\nOR\n\nPrint longer between refills",
      "long_message_best_sku": "Print longer with fewer refill interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "long_message_safe_to_inherit": "Print longer with fewer refill interruptions. This HP Smart Tank all-in-one includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "mid_length": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "mid_length_safe_to_inherit": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "short_message": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "ultra_short": "Fewer refill interruptions",
      "ultra_short_safe_to_inherit": "Fewer refill interruptions"
    },
    "KSP2": {
      "headline": "Ready for recurring print work\n\nOR\n\nEveryday output that keeps moving",
      "long_message_best_sku": "Keep recurring print work moving through busy stretches. HP Smart Tank 7602 All-in-One is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "long_message_safe_to_inherit": "Keep recurring print work moving through busy stretches. This HP Smart Tank all-in-one is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "mid_length": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "mid_length_safe_to_inherit": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "short_message": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "short_message_safe_to_inherit": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "ultra_short": "Everyday productivity",
      "ultra_short_safe_to_inherit": "Everyday productivity"
    },
    "KSP3": {
      "headline": "Less handling for longer tasks\n\nOR\n\nMulti-page work made easier",
      "long_message_best_sku": "Move through multi-page tasks with fewer manual steps. HP Smart Tank 7602 All-in-One pairs a 35-page auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "long_message_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. This HP Smart Tank all-in-one pairs an auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "mid_length": "Move through multi-page tasks with fewer manual steps. A 35-page auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "mid_length_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. An auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "short_message": "A 35-page auto document feeder and automatic two-sided printing reduce manual handling.",
      "short_message_safe_to_inherit": "An auto document feeder and automatic two-sided printing reduce manual handling.",
      "ultra_short": "Fewer manual steps",
      "ultra_short_safe_to_inherit": "Fewer manual steps"
    },
    "KSP4": {
      "headline": "Connections that fit your setup\n\nOR\n\nFlexible ways to get printing",
      "long_message_best_sku": "Connect the way your devices work. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "long_message_safe_to_inherit": "Connect the way your devices work. This HP Smart Tank all-in-one supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "mid_length": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "mid_length_safe_to_inherit": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "short_message": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "short_message_safe_to_inherit": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "ultra_short": "Flexible connections",
      "ultra_short_safe_to_inherit": "Flexible connections"
    },
    "ValueProposition": {
      "headline": "Print more with fewer interruptions",
      "long_message_best_sku": "Keep recurring print, scan, copy, and fax work moving with a high-capacity all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. HP Smart Tank 7602 All-in-One pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, a 35-page auto document feeder, fax, and a 3-inch touchscreen, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "long_message_safe_to_inherit": "Keep recurring print, scan, copy, and fax work moving with a high-capacity HP Smart Tank all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. It pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, an auto document feeder, fax, and touchscreen control, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "mid_length": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "mid_length_safe_to_inherit": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "short_message": "Included ink, workflow tools, and flexible connections keep recurring printing moving.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0d2b454316ccbd87006aa461cfe69c81978dbfd3b1d9a87744",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Wide"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging is printer workflow focused. KSP1 through KSP3 provide concrete paperwork, forms, records, handouts, and desk-task cues. KSP4 is mainly connectivity oriented, with device references unsuitable for scene prose.",
  "count_explanation": "Three KSPs contain useful explicit scene or activity cues, so the response may include up to three prompts. Two prompts were returned because the strongest distinct settings are office paperwork and education preparation; adding a third would mostly repeat document-handling cues.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring document and color jobs"
        },
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "finishing the pages you need."
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Recurring document and page-output cues are simplified into local paper-based work surfaces without depicting the product or supplies."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, records, handouts, and color materials"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "regular document production"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Forms and records support the office prompt, while handouts support the education preparation prompt. Color-material specifics were not visualized to avoid imposing a color treatment."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "multi-page tasks with fewer manual steps"
        },
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "forms, records, and everyday admin work easier to complete at the desk."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Multi-page forms and desk admin work are represented as a compact stack of completed forms and a folder. Hardware workflow features were omitted from the environment prompt."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "nearby devices or a shared network"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "phones, laptops, and desks."
        }
      ],
      "prompt_ids": [],
      "explanation": "Connectivity and nearby-device language does not create a distinct non-hardware scene cue. Phones and laptops were omitted because scene prose must not introduce computing hardware."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "paperwork, forms, records, and color documents"
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "regular document queues, household administration, and everyday business paperwork"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The value proposition reinforces the office paperwork context and regular document queues. Household administration was not used as a separate prompt because the KSPs already support stronger paperwork and handout settings."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Matte laminate worktable surface",
        "Labeled folder and single pen as modest local props",
        "Neutral partition and soft seating edge as simple office background details",
        "Diffuse daylight"
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Light wood grain preparation table",
        "Marked worksheet and pen paired with the source-supported handouts cue",
        "Softly blurred bulletin board and chair back for limited classroom context",
        "Daylight"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Front_Right_Wide",
    "resolved_tag": "Printer_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "Ink refill value",
          "Published speeds and duty cycle",
          "Auto document feeder and two-sided printing features",
          "Phones, laptops, shared-network details",
          "People"
        ],
        "explanation": "The wide oblique printer profile allows a local setting with up to three nearby props and two simple background details. The prompt retains paperwork/admin cues as forms, a folder, and a pen while keeping background detail subordinate."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "Ink refill value",
          "Detailed recurring-output specifications",
          "Document-handling hardware features",
          "Connectivity devices",
          "Full classroom activity or people"
        ],
        "explanation": "The view supports a local education surface without requiring a whole room. The prompt keeps the handout cue with flat, nearby paper details and uses only two simple background details."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "6dc39f55ed7b69add50fa3214b9b91d9b01f4978189c6487d6bed0b943dca820",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "input_raw_sha256": "bbb48142b4717a969c28cf374a00d7019615cfd30ff70aaafc54efa343de35a1",
  "recorded_input_semantic_sha256": "7cb06625ddfad1e4a549df9d7a6b9edc921b9aceb691117c52760057c4fecd84",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvtNFWbF1HCBxkki708rEDGMPLFs",
  "usage": {
    "completion_tokens": 2678,
    "prompt_tokens": 13016,
    "total_tokens": 15694,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1536,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 12544,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 341,
      "engine_ttlt_ms": 25269,
      "pre_inference_ms": 180,
      "service_tbt_ms": 9,
      "service_ttft_ms": 960,
      "service_ttlt_ms": 25875,
      "user_visible_ttft_ms": 780
    }
  },
  "attempt": 1,
  "latency_seconds": 26.562,
  "started_at": "2026-10-22T22:49:41.148375+00:00",
  "completed_at": "2026-10-22T22:50:07.710537+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "04_rich_printer_magic_front_right_wide",
  "source_id": "ee810cf51bb82bb4",
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Wide",
  "purpose": "Same rich source under a wide oblique view.",
  "input_path": "inputs/04_rich_printer_magic_front_right_wide.json",
  "input_raw_sha256": "bbb48142b4717a969c28cf374a00d7019615cfd30ff70aaafc54efa343de35a1",
  "input_semantic_sha256": "7cb06625ddfad1e4a549df9d7a6b9edc921b9aceb691117c52760057c4fecd84",
  "source_kind": "actual",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
      "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "member": null,
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Wide",
    "resolved_tag": "Printer_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "04_rich_printer_magic_front_right_wide",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/04_rich_printer_magic_front_right_wide.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 37,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 32,
      "environment": "Education"
    }
  ],
  "prompt_count": 2,
  "declared_eligible_ksps": 3,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Wide",
    "resolved_tag": "Printer_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Front_Right_Wide",
    "resolved_tag": "Printer_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 05_rich_printer_magic_top_front_closeup

Same rich source under a tight top-oblique view.

- Requested product: `Magic`
- Requested camera: `Printer_Top_Front_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A clean office work surface with a compact stack of forms, lit by diffuse daylight for a recurring paperwork session.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Top_Front_CloseUp",
  "resolved_tag": "Printer_Top_Front_CloseUp",
  "resolution": "exact",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Top_Front_CloseUp",
  "effective_profile": {
    "framing": "tight",
    "elevation": "top_oblique",
    "max_local_props": 1,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Top_Front_CloseUp.png`

SHA-256: `321300b1edd7d20039c2845f10436495503f9e50fa5d572d514866704c6321d5`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "source_camera_name": "Top_Front_CloseUp",
  "catalog": {
    "device_id": "camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "camera_name_exact": "Top_Front_CloseUp",
    "zip_filename": "Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Top_Front_CloseUp.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Top_Front_CloseUp.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 124548,
    "sha256": "321300b1edd7d20039c2845f10436495503f9e50fa5d572d514866704c6321d5",
    "zip_crc32": "f55b2654"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Top_Front_CloseUp.png",
    "bytes": 124548,
    "sha256": "321300b1edd7d20039c2845f10436495503f9e50fa5d572d514866704c6321d5",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Included ink value\n\nOR\n\nPrint longer between refills",
      "long_message_best_sku": "Print longer with fewer refill interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "long_message_safe_to_inherit": "Print longer with fewer refill interruptions. This HP Smart Tank all-in-one includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "mid_length": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "mid_length_safe_to_inherit": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "short_message": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "ultra_short": "Fewer refill interruptions",
      "ultra_short_safe_to_inherit": "Fewer refill interruptions"
    },
    "KSP2": {
      "headline": "Ready for recurring print work\n\nOR\n\nEveryday output that keeps moving",
      "long_message_best_sku": "Keep recurring print work moving through busy stretches. HP Smart Tank 7602 All-in-One is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "long_message_safe_to_inherit": "Keep recurring print work moving through busy stretches. This HP Smart Tank all-in-one is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "mid_length": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "mid_length_safe_to_inherit": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "short_message": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "short_message_safe_to_inherit": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "ultra_short": "Everyday productivity",
      "ultra_short_safe_to_inherit": "Everyday productivity"
    },
    "KSP3": {
      "headline": "Less handling for longer tasks\n\nOR\n\nMulti-page work made easier",
      "long_message_best_sku": "Move through multi-page tasks with fewer manual steps. HP Smart Tank 7602 All-in-One pairs a 35-page auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "long_message_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. This HP Smart Tank all-in-one pairs an auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "mid_length": "Move through multi-page tasks with fewer manual steps. A 35-page auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "mid_length_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. An auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "short_message": "A 35-page auto document feeder and automatic two-sided printing reduce manual handling.",
      "short_message_safe_to_inherit": "An auto document feeder and automatic two-sided printing reduce manual handling.",
      "ultra_short": "Fewer manual steps",
      "ultra_short_safe_to_inherit": "Fewer manual steps"
    },
    "KSP4": {
      "headline": "Connections that fit your setup\n\nOR\n\nFlexible ways to get printing",
      "long_message_best_sku": "Connect the way your devices work. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "long_message_safe_to_inherit": "Connect the way your devices work. This HP Smart Tank all-in-one supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "mid_length": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "mid_length_safe_to_inherit": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "short_message": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "short_message_safe_to_inherit": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "ultra_short": "Flexible connections",
      "ultra_short_safe_to_inherit": "Flexible connections"
    },
    "ValueProposition": {
      "headline": "Print more with fewer interruptions",
      "long_message_best_sku": "Keep recurring print, scan, copy, and fax work moving with a high-capacity all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. HP Smart Tank 7602 All-in-One pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, a 35-page auto document feeder, fax, and a 3-inch touchscreen, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "long_message_safe_to_inherit": "Keep recurring print, scan, copy, and fax work moving with a high-capacity HP Smart Tank all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. It pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, an auto document feeder, fax, and touchscreen control, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "mid_length": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "mid_length_safe_to_inherit": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "short_message": "Included ink, workflow tools, and flexible connections keep recurring printing moving.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0d2b454316ccbd87006aa461cfe69c81978dbfd3b1d9a87744",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Magic",
  "camera_tag": "Printer_Top_Front_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging is mainly product-feature copy, with usable scene cues around recurring paperwork, forms, records, handouts, and desk-based administration. The selected product resolves to a registered printer alias, and the requested camera is a supported tight top-oblique preset.",
  "count_explanation": "KSP1, KSP2, and KSP3 provide overlapping paperwork cues, so they are combined into one compatible local office prompt. KSP4 is primarily about connectivity and nearby devices, which does not justify adding extra hardware or a separate setting. The tight top-oblique view permits only a local surface and one flat prop, with no background details.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring document and color jobs"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The recurring document cue supports the paperwork context, simplified to one compact stack of forms because the view is tight and top-oblique."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, records, handouts, and color materials"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Forms and records are concrete office materials. The prompt keeps the strongest flat cue as one compact stack rather than listing multiple paper types."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "forms, records, and everyday admin work easier to complete at the desk"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The desk-based admin work cue supports an office work surface. Manual handling and product functions are omitted because they would describe hardware behavior rather than the surrounding environment."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "nearby devices or a shared network"
        }
      ],
      "prompt_ids": [],
      "explanation": "The connectivity cue is mostly technical and would require adding extra devices or network context, which is not appropriate for this tight top-oblique view."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "paperwork, forms, records, and color documents are easier to manage"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The value proposition reinforces the recurring paperwork context used in the single office prompt."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Clean office work surface",
        "Diffuse daylight",
        "Recurring paperwork session phrasing to connect the visible stack of forms to the source activity"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Top_Front_CloseUp",
    "resolved_tag": "Printer_Top_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "top_oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "Ink and refill claims",
          "Print speed and duty cycle details",
          "ADF, two-sided printing, fax, touchscreen, and other hardware features",
          "Connectivity devices and shared-network details",
          "People, room fixtures, and background depth"
        ],
        "explanation": "The prompt retains a single flat paperwork prop on a local work surface. The tight top-oblique preset allows at most one local prop and no background details, so the broader office workflow is represented only by a compact stack of forms and daylight."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "f01bca32be39d8b28d8423ea8411a111a946b345330cec717ee4f08d4918c4bd",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "input_raw_sha256": "d03e69638683e22e9d781e13b5867acc470c4943c61cbbf9057d3d5f99ffe059",
  "recorded_input_semantic_sha256": "fa723bc327bfa0bd1c7b9691f6599cda28bd720bfa20d224cc9ac66931ebecac",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvtoJyCQVJtByL5c3GmMA5lU5QG9",
  "usage": {
    "completion_tokens": 1882,
    "prompt_tokens": 13017,
    "total_tokens": 14899,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 12544,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 188,
      "engine_ttlt_ms": 18184,
      "pre_inference_ms": 137,
      "service_tbt_ms": 10,
      "service_ttft_ms": 864,
      "service_ttlt_ms": 18851,
      "user_visible_ttft_ms": 727
    }
  },
  "attempt": 1,
  "latency_seconds": 19.414,
  "started_at": "2026-10-22T22:50:07.735259+00:00",
  "completed_at": "2026-10-22T22:50:27.149572+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "05_rich_printer_magic_top_front_closeup",
  "source_id": "ee810cf51bb82bb4",
  "product_name": "Magic",
  "camera_tag": "Printer_Top_Front_CloseUp",
  "purpose": "Same rich source under a tight top-oblique view.",
  "input_path": "inputs/05_rich_printer_magic_top_front_closeup.json",
  "input_raw_sha256": "d03e69638683e22e9d781e13b5867acc470c4943c61cbbf9057d3d5f99ffe059",
  "input_semantic_sha256": "fa723bc327bfa0bd1c7b9691f6599cda28bd720bfa20d224cc9ac66931ebecac",
  "source_kind": "actual",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
      "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "member": null,
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Top_Front_CloseUp",
    "resolved_tag": "Printer_Top_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "top_oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "05_rich_printer_magic_top_front_closeup",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/05_rich_printer_magic_top_front_closeup.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 20,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 3,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Top_Front_CloseUp",
    "resolved_tag": "Printer_Top_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "top_oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Top_Front_CloseUp",
    "resolved_tag": "Printer_Top_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "top_oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 06_actual_laptop_koki_front_closeup

Actual mobile-work and meeting cues under a tight level view.

- Requested product: `Koki`
- Requested camera: `Laptop_Front_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A clean shared-workspace table surface in pale wood, softly lit by diffuse daylight, with a calm neutral backdrop kept unobtrusive.

**p2 · Office**

A compact customer-site meeting surface in matte laminate, lit by even indoor light against a plain professional background.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Front_CloseUp",
  "resolved_tag": "Laptop_Front_CloseUp",
  "resolution": "exact",
  "requested_product": "Koki",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Front_CloseUp",
  "effective_profile": {
    "framing": "tight",
    "elevation": "level",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_CloseUp.png`

SHA-256: `1814d227cd19499266b091656d3e5402f28db58ae67ee64339a0dfc0df000b12`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "source_camera_name": "Front_CloseUp",
  "catalog": {
    "device_id": "camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "camera_name_exact": "Front_CloseUp",
    "zip_filename": "Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_CloseUp.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_CloseUp.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 82541,
    "sha256": "1814d227cd19499266b091656d3e5402f28db58ae67ee64339a0dfc0df000b12",
    "zip_crc32": "f96fb71a"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_CloseUp.png",
    "bytes": 82541,
    "sha256": "1814d227cd19499266b091656d3e5402f28db58ae67ee64339a0dfc0df000b12",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Work Smarter in More Places\n\nOR\n\nProtected Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places while sensitive work stays protected. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition pairs ultralight portability with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "long_message_safe_to_inherit": "Work smarter from more places while sensitive work stays protected. This HP EliteBook X G2i family pairs portable design with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "mid_length": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "mid_length_safe_to_inherit": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "short_message": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "short_message_safe_to_inherit": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "ultra_short": "Secure AI productivity",
      "ultra_short_safe_to_inherit": "Secure AI productivity"
    },
    "KSP2": {
      "headline": "Ready for AI-Enhanced Work\n\nOR\n\nBuilt for Emerging Workflows",
      "long_message_best_sku": "Stay ready for AI-assisted tasks, calls, and content work. The latest Intel Core Ultra processor is purpose-built for the next era of AI software, with three compute engines that manage AI workloads, help improve video conferencing, and allow advanced content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "long_message_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work. Intel Core Ultra processing is purpose-built for the next era of AI software, with compute engines that manage AI workloads, help improve video conferencing, and allow content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "mid_length": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and three compute engines for AI workloads.",
      "mid_length_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and compute engines for AI workloads.",
      "short_message": "Stay ready for AI-assisted work with Intel Core Ultra and three compute engines.",
      "short_message_safe_to_inherit": "Stay ready for AI-assisted work with Intel Core Ultra processing and compute engines.",
      "ultra_short": "AI-ready platform",
      "ultra_short_safe_to_inherit": "AI-ready platform"
    },
    "KSP3": {
      "headline": "Protection Beyond the Office\n\nOR\n\nDefense from BIOS to Browser",
      "long_message_best_sku": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "long_message_safe_to_inherit": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "mid_length": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "mid_length_safe_to_inherit": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "short_message": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "short_message_safe_to_inherit": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "ultra_short": "Resilient protection",
      "ultra_short_safe_to_inherit": "Resilient protection"
    },
    "KSP4": {
      "headline": "Polished Presence for Every Meeting\n\nOR\n\nStay Framed and Focused",
      "long_message_best_sku": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "long_message_safe_to_inherit": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "mid_length": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "mid_length_safe_to_inherit": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "short_message": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "short_message_safe_to_inherit": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "ultra_short": "Polished meeting presence",
      "ultra_short_safe_to_inherit": "Polished meeting presence"
    },
    "ValueProposition": {
      "headline": "Secure AI Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places with a secure business notebook built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition combines an ultralight 14-inch design, Windows 11 Pro for business, and the latest Intel Core Ultra processor, using three compute engines to manage AI workloads, help improve video conferencing, and allow advanced content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "long_message_safe_to_inherit": "Work smarter from more places with a secure business notebook family built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i family combines portable design, Windows 11 Pro for business, and Intel Core Ultra processing, using compute engines to manage AI workloads, help improve video conferencing, and allow content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "mid_length": "Work smarter from more places with an ultralight HP EliteBook built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "mid_length_safe_to_inherit": "Work smarter from more places with an HP EliteBook family built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "short_message": "A secure, ultralight AI PC for productive work and polished collaboration anywhere.",
      "ultra_short": "Secure AI mobility"
    },
    "_chatSession": {
      "responseId": "resp_0836a6860971d1c4006aabef7902b88197a3d08e1215d8cdf7",
      "model": "gpt-5.5"
    }
  },
  "product_name": "Koki",
  "camera_tag": "Laptop_Front_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The messaging contains four numbered KSPs. Useful scene cues center on mobile professional work, documents, calls, meetings, shared workspaces, customer sites, and work beyond a controlled office; technical AI, security, processor, Wi-Fi, and software claims were not translated into visible props or effects.",
  "count_explanation": "Four KSPs contain some explicit setting or activity cues, so up to four prompts were allowed. Two prompts were returned because the selected tight level view supports only local surface, light, and plain background tone, making broader activity differences impractical.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "Work smarter from more places"
        },
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "mobile professionals move through documents, meetings, and decisions"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "The mobile professional and meeting/document cues informed professional local work surfaces. Documents and visible meeting activity were omitted because the view permits no props or people."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "AI-assisted tasks, calls, and content work"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "emerging business workflows"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Business workflow and calls/content work supported an office workspace context. Processor and AI-platform specifications were omitted as non-environmental details, and calls/content activity was simplified to a quiet work surface."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "Protect sensitive work wherever business takes you"
        },
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "work beyond controlled office environments"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "The beyond-office business cue supported a customer-site professional surface. Security architecture claims were not visualized, and no guards, locks, or cybersecurity metaphors were added."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Bring a polished presence to every meeting"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "office, shared workspace, or customer site"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Meeting, shared-workspace, and customer-site cues directly informed the two office-context prompts. People and visible collaboration details were omitted due to the tight no-people view."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "productive work and polished collaboration anywhere"
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "so sensitive work, meetings, and decisions can keep moving wherever the day takes you"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2"
    ],
    "explanation": "The value proposition reinforced mobile professional collaboration across places, but did not increase the prompt count. Hardware, connectivity, software, and security claims were excluded from scene prose."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wood surface",
        "Diffuse daylight",
        "Calm neutral backdrop"
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Matte laminate surface",
        "Even indoor light",
        "Plain professional background"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Laptop_Front_CloseUp",
    "resolved_tag": "Laptop_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "documents",
          "calls",
          "visible meeting participants",
          "workspace background details"
        ],
        "explanation": "The selected preset is a tight level front view with no local props, no background details, and no people. The prompt retains only a shared-workspace surface, simple light, and neutral backdrop."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "customer-site room context",
          "meeting participants",
          "forms or notebooks",
          "security-related visual metaphors"
        ],
        "explanation": "The selected preset cannot support props, people, or room fixtures. The customer-site meeting cue was reduced to a local professional surface and plain lighting."
      }
    ],
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "ca5b13c25a4d19793c0157bb712be1aa28afffe3513ca32ec8de17cb4b66d0e1",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "input_raw_sha256": "9f2d6ab604f7615a73347b7cb318eb222543f98d43a5d81502ecbc0b7e1f6404",
  "recorded_input_semantic_sha256": "12503723bd33ef07e76e6e4a84d0ffe951f158f5ebe568a5dacf0b1272f18f08",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-Ebvu7QXGXi4y9gd88lGOS0I1ODoPU",
  "usage": {
    "completion_tokens": 2081,
    "prompt_tokens": 8369,
    "total_tokens": 10450,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 3840,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 309,
      "engine_ttlt_ms": 20730,
      "pre_inference_ms": 126,
      "service_tbt_ms": 10,
      "service_ttft_ms": 853,
      "service_ttlt_ms": 21269,
      "user_visible_ttft_ms": 727
    }
  },
  "attempt": 1,
  "latency_seconds": 22.15,
  "started_at": "2026-10-22T22:50:27.174502+00:00",
  "completed_at": "2026-10-22T22:50:49.324997+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "06_actual_laptop_koki_front_closeup",
  "source_id": "22fdbf19f03d1a31",
  "product_name": "Koki",
  "camera_tag": "Laptop_Front_CloseUp",
  "purpose": "Actual mobile-work and meeting cues under a tight level view.",
  "input_path": "inputs/06_actual_laptop_koki_front_closeup.json",
  "input_raw_sha256": "9f2d6ab604f7615a73347b7cb318eb222543f98d43a5d81502ecbc0b7e1f6404",
  "input_semantic_sha256": "12503723bd33ef07e76e6e4a84d0ffe951f158f5ebe568a5dacf0b1272f18f08",
  "source_kind": "actual",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
      "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "member": null,
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Front_CloseUp",
    "resolved_tag": "Laptop_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "06_actual_laptop_koki_front_closeup",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/06_actual_laptop_koki_front_closeup.json",
  "failures": [
    "Evidence is not a verbatim source substring: ValueProposition.long_message_best_sku"
  ],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 20,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 18,
      "environment": "Office"
    }
  ],
  "prompt_count": 2,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Front_CloseUp",
    "resolved_tag": "Laptop_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Front_CloseUp",
    "resolved_tag": "Laptop_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 07_actual_laptop_koki_front_right_medium

Same actual laptop source under a medium oblique view.

- Requested product: `Koki`
- Requested camera: `Laptop_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A shared workspace table in pale wood with a closed notebook and a takeaway cup. A softened meeting-room partition suggests business collaboration in gentle daylight.

**p2 · Office**

A compact creative studio worktable with a paper storyboard sheet and a single pen, lit by diffuse daylight. A muted pinboard section sits softly behind.

**p3 · Office**

A customer-site worktable with a slim folder of documents and a single pen, lit by diffuse daylight. A neutral wall panel keeps the setting focused and professional.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Front_Right_Medium",
  "resolved_tag": "Laptop_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Koki",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Medium.png`

SHA-256: `fd7398fb0e895e12745270e69526386d5a3cb6de2e4e67aaeb8609224f3a67b0`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 60525,
    "sha256": "fd7398fb0e895e12745270e69526386d5a3cb6de2e4e67aaeb8609224f3a67b0",
    "zip_crc32": "bb682d63"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Medium.png",
    "bytes": 60525,
    "sha256": "fd7398fb0e895e12745270e69526386d5a3cb6de2e4e67aaeb8609224f3a67b0",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Work Smarter in More Places\n\nOR\n\nProtected Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places while sensitive work stays protected. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition pairs ultralight portability with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "long_message_safe_to_inherit": "Work smarter from more places while sensitive work stays protected. This HP EliteBook X G2i family pairs portable design with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "mid_length": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "mid_length_safe_to_inherit": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "short_message": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "short_message_safe_to_inherit": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "ultra_short": "Secure AI productivity",
      "ultra_short_safe_to_inherit": "Secure AI productivity"
    },
    "KSP2": {
      "headline": "Ready for AI-Enhanced Work\n\nOR\n\nBuilt for Emerging Workflows",
      "long_message_best_sku": "Stay ready for AI-assisted tasks, calls, and content work. The latest Intel Core Ultra processor is purpose-built for the next era of AI software, with three compute engines that manage AI workloads, help improve video conferencing, and allow advanced content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "long_message_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work. Intel Core Ultra processing is purpose-built for the next era of AI software, with compute engines that manage AI workloads, help improve video conferencing, and allow content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "mid_length": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and three compute engines for AI workloads.",
      "mid_length_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and compute engines for AI workloads.",
      "short_message": "Stay ready for AI-assisted work with Intel Core Ultra and three compute engines.",
      "short_message_safe_to_inherit": "Stay ready for AI-assisted work with Intel Core Ultra processing and compute engines.",
      "ultra_short": "AI-ready platform",
      "ultra_short_safe_to_inherit": "AI-ready platform"
    },
    "KSP3": {
      "headline": "Protection Beyond the Office\n\nOR\n\nDefense from BIOS to Browser",
      "long_message_best_sku": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "long_message_safe_to_inherit": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "mid_length": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "mid_length_safe_to_inherit": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "short_message": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "short_message_safe_to_inherit": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "ultra_short": "Resilient protection",
      "ultra_short_safe_to_inherit": "Resilient protection"
    },
    "KSP4": {
      "headline": "Polished Presence for Every Meeting\n\nOR\n\nStay Framed and Focused",
      "long_message_best_sku": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "long_message_safe_to_inherit": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "mid_length": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "mid_length_safe_to_inherit": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "short_message": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "short_message_safe_to_inherit": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "ultra_short": "Polished meeting presence",
      "ultra_short_safe_to_inherit": "Polished meeting presence"
    },
    "ValueProposition": {
      "headline": "Secure AI Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places with a secure business notebook built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition combines an ultralight 14-inch design, Windows 11 Pro for business, and the latest Intel Core Ultra processor, using three compute engines to manage AI workloads, help improve video conferencing, and allow advanced content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "long_message_safe_to_inherit": "Work smarter from more places with a secure business notebook family built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i family combines portable design, Windows 11 Pro for business, and Intel Core Ultra processing, using compute engines to manage AI workloads, help improve video conferencing, and allow content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "mid_length": "Work smarter from more places with an ultralight HP EliteBook built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "mid_length_safe_to_inherit": "Work smarter from more places with an HP EliteBook family built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "short_message": "A secure, ultralight AI PC for productive work and polished collaboration anywhere.",
      "ultra_short": "Secure AI mobility"
    },
    "_chatSession": {
      "responseId": "resp_0836a6860971d1c4006aabef7902b88197a3d08e1215d8cdf7",
      "model": "gpt-5.5"
    }
  },
  "product_name": "Koki",
  "camera_tag": "Laptop_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging is business-productivity oriented, with usable cues around mobile work, documents, meetings, content work, shared workspaces, and customer-site work. Technical security, AI, processor, wireless, and camera-feature claims were translated only into ordinary work-context details where they supported a believable local setting.",
  "count_explanation": "Four numbered KSPs contain explicit scene or activity cues, so up to four prompts were allowed. Three prompts were returned because KSP1 and KSP3 overlap around mobile sensitive work beyond the office, while KSP2 and KSP4 support distinct content-work and meeting-work settings. Each prompt stays within the medium oblique view limits.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "It helps mobile professionals move through documents, meetings, and decisions with greater confidence."
        }
      ],
      "prompt_ids": [
        "p1",
        "p3"
      ],
      "explanation": "Documents and meetings were expressed through a shared workspace table and a customer-site document folder. Security and AI claims were omitted from the visible environment because they are abstract benefits, not physical scene elements."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "Stay ready for AI-assisted tasks, calls, and content work."
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "The content-work cue was simplified into a compact creative studio surface with a storyboard sheet and pen. Processor and AI workload details were omitted as non-environmental specifications."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step."
        }
      ],
      "prompt_ids": [
        "p3"
      ],
      "explanation": "The beyond-office cue was represented as a customer-site worktable. The security architecture claim was not visualized as guards, locks, or special effects."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "whether joining from an office, shared workspace, or customer site."
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Bring a polished presence to every meeting."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The meeting and shared-workspace cues were retained as a local shared table with a subtle meeting-room partition. No full participants were added because the medium view only supports modest partial activity and the scene works without people."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "sensitive work, meetings, and decisions can keep moving wherever the day takes you."
      }
    ],
    "prompt_ids": [
      "p1",
      "p2",
      "p3"
    ],
    "explanation": "The value proposition reinforced a mobile business-work context across meeting, content, and document-focused scenes. Product specifications and branded feature claims were omitted from scene prose."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wood surface, closed notebook, takeaway cup, meeting-room partition, and gentle daylight are ordinary invented details used to make the shared-workspace cue feel concrete."
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Storyboard sheet, pen, muted pinboard section, and diffuse daylight are plausible invented details for the content-work cue."
      ]
    },
    {
      "prompt_id": "p3",
      "details": [
        "Slim folder, pen, neutral wall panel, and diffuse daylight are plausible invented details for a customer-site document-work setting."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession.responseId",
    "_chatSession.model"
  ],
  "camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "No full meeting participants",
          "No broad room layout",
          "No device-dependent video-call details"
        ],
        "explanation": "The medium oblique preset allows at most two nearby props and one subordinate background detail, so the meeting cue was kept to a notebook, cup, and a softened partition."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "No full creative studio inventory",
          "No extra tools or displays",
          "No technical AI or processor visuals"
        ],
        "explanation": "The content-work cue was localized to a storyboard sheet and pen with one simple background pinboard section, preserving the selected view without demanding more space."
      },
      {
        "prompt_id": "p3",
        "omitted_or_simplified": [
          "No whole customer-site room",
          "No people",
          "No security imagery"
        ],
        "explanation": "The beyond-office and sensitive-document cue was reduced to a folder and pen on a professional worktable, with one neutral wall detail to avoid exceeding the medium framing limits."
      }
    ],
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "95b95d225e9ebf4aebc5451e8fd721053fdab69ebb26bdd8a5399cbd367c759a",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "input_raw_sha256": "dd5e7ff6c45e9261eece9891bd939e0064487cb2f4c6c563faf222e9b62f229e",
  "recorded_input_semantic_sha256": "b4f03ba2a7783333ffe64883a732435bda7580c39b5aac68103a0c803db30ecd",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvuT56fuJC4mcbFZUm841eRnrGZQ",
  "usage": {
    "completion_tokens": 2258,
    "prompt_tokens": 8370,
    "total_tokens": 10628,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 7936,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 316,
      "engine_ttlt_ms": 20442,
      "pre_inference_ms": 117,
      "service_tbt_ms": 9,
      "service_ttft_ms": 726,
      "service_ttlt_ms": 20855,
      "user_visible_ttft_ms": 609
    }
  },
  "attempt": 1,
  "latency_seconds": 21.577,
  "started_at": "2026-10-22T22:50:49.349195+00:00",
  "completed_at": "2026-10-22T22:51:10.926848+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "07_actual_laptop_koki_front_right_medium",
  "source_id": "22fdbf19f03d1a31",
  "product_name": "Koki",
  "camera_tag": "Laptop_Front_Right_Medium",
  "purpose": "Same actual laptop source under a medium oblique view.",
  "input_path": "inputs/07_actual_laptop_koki_front_right_medium.json",
  "input_raw_sha256": "dd5e7ff6c45e9261eece9891bd939e0064487cb2f4c6c563faf222e9b62f229e",
  "input_semantic_sha256": "b4f03ba2a7783333ffe64883a732435bda7580c39b5aac68103a0c803db30ecd",
  "source_kind": "actual",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
      "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "member": null,
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "07_actual_laptop_koki_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/07_actual_laptop_koki_front_right_medium.json",
  "failures": [
    "Upstream metadata is not listed as ignored"
  ],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 25,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 25,
      "environment": "Office"
    },
    {
      "prompt_id": "p3",
      "words": 27,
      "environment": "Office"
    }
  ],
  "prompt_count": 3,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 08_actual_laptop_koki_front_right_wide

Same actual laptop source under a wide oblique view.

- Requested product: `Koki`
- Requested camera: `Laptop_Front_Right_Wide`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A quiet meeting table in pale wood with a paper agenda, a closed notebook, and a capped pen. Softly blurred seating and an acoustic wall panel add a focused collaboration setting in daylight.

**p2 · Office**

A customer-site touchdown counter with a compact stack of forms, a visitor badge, and a ceramic cup. Neutral reception seating and soft daylight suggest work continuing away from the main office.

**p3 · Office**

A shared workspace surface with storyboard printouts, a pencil, and a small notebook. A muted pinboard and simple lounge chair sit softly out of focus, supporting content work in natural light.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Front_Right_Wide",
  "resolved_tag": "Laptop_Front_Right_Wide",
  "resolution": "exact",
  "requested_product": "Koki",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Front_Right_Wide",
  "effective_profile": {
    "framing": "wide",
    "elevation": "oblique",
    "max_local_props": 3,
    "max_background_details": 2,
    "people_policy": "optional_if_supported_and_unobtrusive"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Wide.png`

SHA-256: `c6e0cf71f75a55562146a49a0d55c5b61ab8c236ec154b404645a7fab9d7834d`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "source_camera_name": "Front_Right_Wide",
  "catalog": {
    "device_id": "camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "camera_name_exact": "Front_Right_Wide",
    "zip_filename": "Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Wide.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Wide.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 21140,
    "sha256": "c6e0cf71f75a55562146a49a0d55c5b61ab8c236ec154b404645a7fab9d7834d",
    "zip_crc32": "486abfb5"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Front_Right_Wide.png",
    "bytes": 21140,
    "sha256": "c6e0cf71f75a55562146a49a0d55c5b61ab8c236ec154b404645a7fab9d7834d",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Work Smarter in More Places\n\nOR\n\nProtected Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places while sensitive work stays protected. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition pairs ultralight portability with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "long_message_safe_to_inherit": "Work smarter from more places while sensitive work stays protected. This HP EliteBook X G2i family pairs portable design with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "mid_length": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "mid_length_safe_to_inherit": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "short_message": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "short_message_safe_to_inherit": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "ultra_short": "Secure AI productivity",
      "ultra_short_safe_to_inherit": "Secure AI productivity"
    },
    "KSP2": {
      "headline": "Ready for AI-Enhanced Work\n\nOR\n\nBuilt for Emerging Workflows",
      "long_message_best_sku": "Stay ready for AI-assisted tasks, calls, and content work. The latest Intel Core Ultra processor is purpose-built for the next era of AI software, with three compute engines that manage AI workloads, help improve video conferencing, and allow advanced content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "long_message_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work. Intel Core Ultra processing is purpose-built for the next era of AI software, with compute engines that manage AI workloads, help improve video conferencing, and allow content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "mid_length": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and three compute engines for AI workloads.",
      "mid_length_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and compute engines for AI workloads.",
      "short_message": "Stay ready for AI-assisted work with Intel Core Ultra and three compute engines.",
      "short_message_safe_to_inherit": "Stay ready for AI-assisted work with Intel Core Ultra processing and compute engines.",
      "ultra_short": "AI-ready platform",
      "ultra_short_safe_to_inherit": "AI-ready platform"
    },
    "KSP3": {
      "headline": "Protection Beyond the Office\n\nOR\n\nDefense from BIOS to Browser",
      "long_message_best_sku": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "long_message_safe_to_inherit": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "mid_length": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "mid_length_safe_to_inherit": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "short_message": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "short_message_safe_to_inherit": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "ultra_short": "Resilient protection",
      "ultra_short_safe_to_inherit": "Resilient protection"
    },
    "KSP4": {
      "headline": "Polished Presence for Every Meeting\n\nOR\n\nStay Framed and Focused",
      "long_message_best_sku": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "long_message_safe_to_inherit": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "mid_length": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "mid_length_safe_to_inherit": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "short_message": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "short_message_safe_to_inherit": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "ultra_short": "Polished meeting presence",
      "ultra_short_safe_to_inherit": "Polished meeting presence"
    },
    "ValueProposition": {
      "headline": "Secure AI Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places with a secure business notebook built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition combines an ultralight 14-inch design, Windows 11 Pro for business, and the latest Intel Core Ultra processor, using three compute engines to manage AI workloads, help improve video conferencing, and allow advanced content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "long_message_safe_to_inherit": "Work smarter from more places with a secure business notebook family built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i family combines portable design, Windows 11 Pro for business, and Intel Core Ultra processing, using compute engines to manage AI workloads, help improve video conferencing, and allow content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "mid_length": "Work smarter from more places with an ultralight HP EliteBook built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "mid_length_safe_to_inherit": "Work smarter from more places with an HP EliteBook family built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "short_message": "A secure, ultralight AI PC for productive work and polished collaboration anywhere.",
      "ultra_short": "Secure AI mobility"
    },
    "_chatSession": {
      "responseId": "resp_0836a6860971d1c4006aabef7902b88197a3d08e1215d8cdf7",
      "model": "gpt-5.5"
    }
  },
  "product_name": "Koki",
  "camera_tag": "Laptop_Front_Right_Wide"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging is mostly business productivity copy, but it contains usable cues around documents, meetings, calls, content work, shared workspaces, customer sites, and working beyond controlled office environments.",
  "count_explanation": "Four numbered KSPs contain useful scene or activity cues. Three prompts were returned because the cues overlap heavily around mobile business work, meetings, and shared or customer-site office contexts; combining them avoids repetitive variants while staying within the wide oblique view limits.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "mobile professionals move through documents, meetings, and decisions"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Mapped to local meeting and document-handling cues. Security and AI language were omitted as abstract benefits rather than visible setting requirements."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "AI-assisted tasks, calls, and content work"
        }
      ],
      "prompt_ids": [
        "p1",
        "p3"
      ],
      "explanation": "Mapped to work-session and content-preparation surfaces. Calls and AI processing were simplified because adding extra hardware or a visible conferencing setup would conflict with the prompt restrictions."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "work beyond controlled office environments"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "Mapped to a customer-site touchdown counter. The protection claim itself was not visualized through guards, locks, or security props."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "whether joining from an office, shared workspace, or customer site"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2",
        "p3"
      ],
      "explanation": "Mapped to office, shared workspace, and customer-site contexts. Full meeting participants were omitted to keep the scene unobtrusive for the selected wide product view."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "sensitive work, meetings, and decisions can keep moving wherever the day takes you"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2",
      "p3"
    ],
    "explanation": "Used to unify the prompts around mobile business productivity, collaboration, and work continuing across different professional locations."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wooden meeting table",
        "Paper agenda, closed notebook, and capped pen",
        "Softly blurred seating and acoustic wall panel",
        "Natural daylight"
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Customer-site touchdown counter",
        "Compact stack of forms, visitor badge, and ceramic cup",
        "Neutral reception seating",
        "Soft daylight"
      ]
    },
    {
      "prompt_id": "p3",
      "details": [
        "Shared workspace surface",
        "Storyboard printouts, pencil, and small notebook",
        "Muted pinboard and simple lounge chair",
        "Natural light"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession.responseId",
    "_chatSession.model"
  ],
  "camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "No full people or group meeting",
          "No conferencing hardware",
          "Limited to three nearby props and two background details"
        ],
        "explanation": "The wide oblique preset can support a local meeting-table context, so meeting cues were retained through an agenda, notebook, pen, seating, and an acoustic panel without requiring a larger room or added devices."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "Customer site reduced to a local counter and reception cue",
          "No visible security metaphor",
          "No full office layout"
        ],
        "explanation": "The beyond-office cue was retained through a touchdown counter, forms, visitor badge, cup, and reception seating while keeping background detail subordinate to the selected view."
      },
      {
        "prompt_id": "p3",
        "omitted_or_simplified": [
          "Content work shown through paper materials only",
          "No extra computing hardware",
          "No large studio inventory"
        ],
        "explanation": "The content-work cue was simplified into storyboard printouts, a pencil, and a notebook, with only a pinboard and lounge chair as soft background details within the wide oblique limits."
      }
    ],
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "24bb3461e0f87d115486381ae4f1b00ce8611cdae72b9f3b9660a9b313ae71da",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "input_raw_sha256": "c644a5aeb3cc2a685ee5b8024da9d55db59279de4d4fb2e0d6fd6935b04a3e97",
  "recorded_input_semantic_sha256": "dfe89eff1607777a7d9fac133ebac13c5a57a2eed48c08c07f5dd05a07ee6ec6",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-Ebvupsdw70QFrndxhcSAoF4VFcwuA",
  "usage": {
    "completion_tokens": 2176,
    "prompt_tokens": 8370,
    "total_tokens": 10546,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 7936,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 191,
      "engine_ttlt_ms": 20757,
      "pre_inference_ms": 172,
      "service_tbt_ms": 9,
      "service_ttft_ms": 922,
      "service_ttlt_ms": 21476,
      "user_visible_ttft_ms": 750
    }
  },
  "attempt": 1,
  "latency_seconds": 22.118,
  "started_at": "2026-10-22T22:51:10.950996+00:00",
  "completed_at": "2026-10-22T22:51:33.069479+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "08_actual_laptop_koki_front_right_wide",
  "source_id": "22fdbf19f03d1a31",
  "product_name": "Koki",
  "camera_tag": "Laptop_Front_Right_Wide",
  "purpose": "Same actual laptop source under a wide oblique view.",
  "input_path": "inputs/08_actual_laptop_koki_front_right_wide.json",
  "input_raw_sha256": "c644a5aeb3cc2a685ee5b8024da9d55db59279de4d4fb2e0d6fd6935b04a3e97",
  "input_semantic_sha256": "dfe89eff1607777a7d9fac133ebac13c5a57a2eed48c08c07f5dd05a07ee6ec6",
  "source_kind": "actual",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
      "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "member": null,
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "08_actual_laptop_koki_front_right_wide",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/08_actual_laptop_koki_front_right_wide.json",
  "failures": [
    "Upstream metadata is not listed as ignored"
  ],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 33,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 31,
      "environment": "Office"
    },
    {
      "prompt_id": "p3",
      "words": 31,
      "environment": "Office"
    }
  ],
  "prompt_count": 3,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 09_actual_laptop_koki_top_front_medium

Same actual laptop source under a medium top-oblique view.

- Requested product: `Koki`
- Requested camera: `Laptop_Top_Front_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A natural-wood shared-workspace table with a paper meeting agenda and a closed notebook, kept uncluttered in diffuse daylight.

**p2 · Office**

A compact customer-site work counter with a small stack of marked-up forms and a single pen, under even overhead office light.

**p3 · Office**

A matte laminate office surface with a storyboard worksheet and one pencil, kept uncluttered under soft daylight for focused content work.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Top_Front_Medium",
  "resolved_tag": "Laptop_Top_Front_Medium",
  "resolution": "exact",
  "requested_product": "Koki",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Top_Front_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "top_oblique",
    "max_local_props": 2,
    "max_background_details": 0,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Top_Front_Medium.png`

SHA-256: `a2d493dd6d8d1160fe302bef2903ea264292e2030ac6cc840482c6ace8b6650b`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "source_camera_name": "Top_Front_Medium",
  "catalog": {
    "device_id": "camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "camera_name_exact": "Top_Front_Medium",
    "zip_filename": "Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Top_Front_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Top_Front_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 99617,
    "sha256": "a2d493dd6d8d1160fe302bef2903ea264292e2030ac6cc840482c6ace8b6650b",
    "zip_crc32": "8b77170c"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Top_Front_Medium.png",
    "bytes": 99617,
    "sha256": "a2d493dd6d8d1160fe302bef2903ea264292e2030ac6cc840482c6ace8b6650b",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Work Smarter in More Places\n\nOR\n\nProtected Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places while sensitive work stays protected. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition pairs ultralight portability with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "long_message_safe_to_inherit": "Work smarter from more places while sensitive work stays protected. This HP EliteBook X G2i family pairs portable design with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "mid_length": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "mid_length_safe_to_inherit": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "short_message": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "short_message_safe_to_inherit": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "ultra_short": "Secure AI productivity",
      "ultra_short_safe_to_inherit": "Secure AI productivity"
    },
    "KSP2": {
      "headline": "Ready for AI-Enhanced Work\n\nOR\n\nBuilt for Emerging Workflows",
      "long_message_best_sku": "Stay ready for AI-assisted tasks, calls, and content work. The latest Intel Core Ultra processor is purpose-built for the next era of AI software, with three compute engines that manage AI workloads, help improve video conferencing, and allow advanced content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "long_message_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work. Intel Core Ultra processing is purpose-built for the next era of AI software, with compute engines that manage AI workloads, help improve video conferencing, and allow content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "mid_length": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and three compute engines for AI workloads.",
      "mid_length_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and compute engines for AI workloads.",
      "short_message": "Stay ready for AI-assisted work with Intel Core Ultra and three compute engines.",
      "short_message_safe_to_inherit": "Stay ready for AI-assisted work with Intel Core Ultra processing and compute engines.",
      "ultra_short": "AI-ready platform",
      "ultra_short_safe_to_inherit": "AI-ready platform"
    },
    "KSP3": {
      "headline": "Protection Beyond the Office\n\nOR\n\nDefense from BIOS to Browser",
      "long_message_best_sku": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "long_message_safe_to_inherit": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "mid_length": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "mid_length_safe_to_inherit": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "short_message": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "short_message_safe_to_inherit": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "ultra_short": "Resilient protection",
      "ultra_short_safe_to_inherit": "Resilient protection"
    },
    "KSP4": {
      "headline": "Polished Presence for Every Meeting\n\nOR\n\nStay Framed and Focused",
      "long_message_best_sku": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "long_message_safe_to_inherit": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "mid_length": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "mid_length_safe_to_inherit": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "short_message": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "short_message_safe_to_inherit": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "ultra_short": "Polished meeting presence",
      "ultra_short_safe_to_inherit": "Polished meeting presence"
    },
    "ValueProposition": {
      "headline": "Secure AI Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places with a secure business notebook built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition combines an ultralight 14-inch design, Windows 11 Pro for business, and the latest Intel Core Ultra processor, using three compute engines to manage AI workloads, help improve video conferencing, and allow advanced content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "long_message_safe_to_inherit": "Work smarter from more places with a secure business notebook family built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i family combines portable design, Windows 11 Pro for business, and Intel Core Ultra processing, using compute engines to manage AI workloads, help improve video conferencing, and allow content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "mid_length": "Work smarter from more places with an ultralight HP EliteBook built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "mid_length_safe_to_inherit": "Work smarter from more places with an HP EliteBook family built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "short_message": "A secure, ultralight AI PC for productive work and polished collaboration anywhere.",
      "ultra_short": "Secure AI mobility"
    },
    "_chatSession": {
      "responseId": "resp_0836a6860971d1c4006aabef7902b88197a3d08e1215d8cdf7",
      "model": "gpt-5.5"
    }
  },
  "product_name": "Koki",
  "camera_tag": "Laptop_Top_Front_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The messaging provides concrete business mobility, meetings, protected work, customer-site/shared-workspace, and content-work cues. Technical claims and security wording were translated only into ordinary local work-surface details that fit the selected top-oblique medium view.",
  "count_explanation": "Four numbered KSPs contain usable scene or activity cues, so up to four prompts were allowed. Three prompts were returned because KSP1 and KSP4 overlap around mobile meetings, while KSP3 and KSP2 support distinct protected-work and content-work surfaces.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "It helps mobile professionals move through documents, meetings, and decisions with greater confidence."
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Documents, meetings, and mobile professional work informed the meeting agenda and customer-site forms. Broader portability and security claims were not shown literally."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "Stay ready for AI-assisted tasks, calls, and content work."
        }
      ],
      "prompt_ids": [
        "p3"
      ],
      "explanation": "The content-work cue was represented as a storyboard worksheet and pencil. Calls, processors, AI engines, and conferencing improvements were omitted because they would imply the target hardware or off-view activity."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "Protect sensitive work wherever business takes you."
        },
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "work beyond controlled office environments with greater confidence"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "Sensitive mobile business work was simplified to marked-up forms on a customer-site counter. Security mechanisms were omitted as abstract or non-environmental."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Bring a polished presence to every meeting."
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "whether joining from an office, shared workspace, or customer site."
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Meeting and shared-workspace/customer-site cues informed the local table and counter settings. People and active video presence were omitted to avoid implying the target device or exceeding the view."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "secure business notebook built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2",
      "p3"
    ],
    "explanation": "Used for overall business mobility and collaboration context, without adding extra prompts or hardware-specific details."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Natural wood surface",
        "Closed notebook",
        "Diffuse daylight"
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Compact counter",
        "Marked-up forms",
        "Even overhead office light"
      ]
    },
    {
      "prompt_id": "p3",
      "details": [
        "Matte laminate surface",
        "Storyboard worksheet",
        "Soft daylight"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Laptop_Top_Front_Medium",
    "resolved_tag": "Laptop_Top_Front_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "top_oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "Whole meeting room omitted",
          "People omitted",
          "Background details omitted"
        ],
        "explanation": "The selected top-oblique medium profile supports a local horizontal surface with up to two low-profile props and no background details, so the meeting cue became an agenda and notebook."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "Customer-site environment reduced to a counter",
          "Security claims reduced to work papers",
          "Background details omitted"
        ],
        "explanation": "The view allows only nearby surface context, so protected mobile work was represented with forms and a pen rather than a larger site or visible workers."
      },
      {
        "prompt_id": "p3",
        "omitted_or_simplified": [
          "Calls and conferencing omitted",
          "Technical AI platform details omitted",
          "No room-depth context"
        ],
        "explanation": "Top-oblique constraints favor flat surface details; content work was kept to a storyboard worksheet and pencil with simple light."
      }
    ],
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "e5a379d9bd4675b6bed54545934696c533c32ea8b9a441104402e78eca09d74d",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "input_raw_sha256": "cd27b84cce7035814e9154bb8247e24ce73503074b9d87cb84752a4122386227",
  "recorded_input_semantic_sha256": "6ff9f668ebc418476ffdf46b748691a55470c06c0fdd04aa5de11387192f0b1f",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvvBfOtM4H6YR9KKXcd1dEhSzBSm",
  "usage": {
    "completion_tokens": 2653,
    "prompt_tokens": 8371,
    "total_tokens": 11024,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1536,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 7936,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 349,
      "engine_ttlt_ms": 25567,
      "pre_inference_ms": 208,
      "service_tbt_ms": 10,
      "service_ttft_ms": 990,
      "service_ttlt_ms": 26203,
      "user_visible_ttft_ms": 783
    }
  },
  "attempt": 1,
  "latency_seconds": 26.829,
  "started_at": "2026-10-22T22:51:33.093918+00:00",
  "completed_at": "2026-10-22T22:51:59.923600+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "09_actual_laptop_koki_top_front_medium",
  "source_id": "22fdbf19f03d1a31",
  "product_name": "Koki",
  "camera_tag": "Laptop_Top_Front_Medium",
  "purpose": "Same actual laptop source under a medium top-oblique view.",
  "input_path": "inputs/09_actual_laptop_koki_top_front_medium.json",
  "input_raw_sha256": "cd27b84cce7035814e9154bb8247e24ce73503074b9d87cb84752a4122386227",
  "input_semantic_sha256": "6ff9f668ebc418476ffdf46b748691a55470c06c0fdd04aa5de11387192f0b1f",
  "source_kind": "actual",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
      "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "member": null,
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Top_Front_Medium",
    "resolved_tag": "Laptop_Top_Front_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "top_oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "09_actual_laptop_koki_top_front_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/09_actual_laptop_koki_top_front_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 18,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 21,
      "environment": "Office"
    },
    {
      "prompt_id": "p3",
      "words": 21,
      "environment": "Office"
    }
  ],
  "prompt_count": 3,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Top_Front_Medium",
    "resolved_tag": "Laptop_Top_Front_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "top_oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Top_Front_Medium",
    "resolved_tag": "Laptop_Top_Front_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "top_oblique",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 10_actual_laptop_viktor_front_right_closeup

Actual laptop source under the especially tight Viktor override.

- Requested product: `Viktor`
- Requested camera: `Laptop_Front_Right_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A shared-work setting on a clean matte tabletop, softened by gentle daylight against an unobtrusive neutral background.

**p2 · Office**

A customer-site meeting surface in smooth wood, kept clear under soft ambient light with a simple neutral backdrop.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Front_Right_CloseUp",
  "resolved_tag": "Laptop_Front_Right_CloseUp",
  "resolution": "exact",
  "requested_product": "Viktor",
  "resolved_product": "Viktor_Sahara-Silver.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Front_Right_CloseUp",
  "effective_profile": {
    "framing": "tight",
    "elevation": "oblique",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [
    {
      "product_name": "Viktor_Sahara-Silver.laptop.usdz",
      "camera_tag": "Laptop_Front_Right_CloseUp",
      "replacements": {
        "max_local_props": 0,
        "max_background_details": 0,
        "people_policy": "omit"
      },
      "reason": "Very tight tall framing in the reviewed Viktor view; favor only the support surface and light."
    }
  ],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Viktor_Sahara-Silver.laptop/camera_laptop.locator_Viktor_Sahara-Silver.laptop_Front_Right_CloseUp.png`

SHA-256: `2c3af15f2c30d952c3208b256258ada4c6be040f3b07c57ba96b3a27de5c3c1a`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Viktor_Sahara-Silver.laptop.usdz",
  "source_camera_name": "Front_Right_CloseUp",
  "catalog": {
    "device_id": "camera_laptop.locator_Viktor_Sahara-Silver.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Viktor_Sahara-Silver.laptop.usdz",
    "camera_name_exact": "Front_Right_CloseUp",
    "zip_filename": "Shared/camera_laptop.locator_Viktor_Sahara-Silver.laptop/camera_laptop.locator_Viktor_Sahara-Silver.laptop_Front_Right_CloseUp.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Viktor_Sahara-Silver.laptop/camera_laptop.locator_Viktor_Sahara-Silver.laptop_Front_Right_CloseUp.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 99096,
    "sha256": "2c3af15f2c30d952c3208b256258ada4c6be040f3b07c57ba96b3a27de5c3c1a",
    "zip_crc32": "8aca2995"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Viktor_Sahara-Silver.laptop/camera_laptop.locator_Viktor_Sahara-Silver.laptop_Front_Right_CloseUp.png",
    "bytes": 99096,
    "sha256": "2c3af15f2c30d952c3208b256258ada4c6be040f3b07c57ba96b3a27de5c3c1a",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Work Smarter in More Places\n\nOR\n\nProtected Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places while sensitive work stays protected. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition pairs ultralight portability with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "long_message_safe_to_inherit": "Work smarter from more places while sensitive work stays protected. This HP EliteBook X G2i family pairs portable design with AI-enhanced workflow support and HP Wolf Security for Business, creating hardware-enforced, always-on, resilient defense from BIOS to browser. It helps mobile professionals move through documents, meetings, and decisions with greater confidence.",
      "mid_length": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "mid_length_safe_to_inherit": "Work smarter from more places while sensitive work stays protected, with AI-enhanced workflow support and HP Wolf Security for Business.",
      "short_message": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "short_message_safe_to_inherit": "Work smarter from more places with AI-enhanced support and HP Wolf Security.",
      "ultra_short": "Secure AI productivity",
      "ultra_short_safe_to_inherit": "Secure AI productivity"
    },
    "KSP2": {
      "headline": "Ready for AI-Enhanced Work\n\nOR\n\nBuilt for Emerging Workflows",
      "long_message_best_sku": "Stay ready for AI-assisted tasks, calls, and content work. The latest Intel Core Ultra processor is purpose-built for the next era of AI software, with three compute engines that manage AI workloads, help improve video conferencing, and allow advanced content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "long_message_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work. Intel Core Ultra processing is purpose-built for the next era of AI software, with compute engines that manage AI workloads, help improve video conferencing, and allow content creation. It gives mobile professionals a practical foundation for emerging business workflows.",
      "mid_length": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and three compute engines for AI workloads.",
      "mid_length_safe_to_inherit": "Stay ready for AI-assisted tasks, calls, and content work with Intel Core Ultra processing and compute engines for AI workloads.",
      "short_message": "Stay ready for AI-assisted work with Intel Core Ultra and three compute engines.",
      "short_message_safe_to_inherit": "Stay ready for AI-assisted work with Intel Core Ultra processing and compute engines.",
      "ultra_short": "AI-ready platform",
      "ultra_short_safe_to_inherit": "AI-ready platform"
    },
    "KSP3": {
      "headline": "Protection Beyond the Office\n\nOR\n\nDefense from BIOS to Browser",
      "long_message_best_sku": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "long_message_safe_to_inherit": "Protect sensitive work wherever business takes you. HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS. It helps mobile professionals work beyond controlled office environments with greater confidence, without treating protection as a separate step.",
      "mid_length": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "mid_length_safe_to_inherit": "Protect sensitive work beyond the office with HP Wolf Security for Business, built for resilient defense from BIOS to browser.",
      "short_message": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "short_message_safe_to_inherit": "Protect sensitive work with HP Wolf Security and resilient defense from BIOS to browser.",
      "ultra_short": "Resilient protection",
      "ultra_short_safe_to_inherit": "Resilient protection"
    },
    "KSP4": {
      "headline": "Polished Presence for Every Meeting\n\nOR\n\nStay Framed and Focused",
      "long_message_best_sku": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "long_message_safe_to_inherit": "Bring a polished presence to every meeting. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight. It helps mobile professionals stay focused on the conversation, whether joining from an office, shared workspace, or customer site.",
      "mid_length": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "mid_length_safe_to_inherit": "Bring a polished presence to every meeting with Poly Camera Pro framing, smart background adjustments, and spotlight that helps reduce visual distractions.",
      "short_message": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "short_message_safe_to_inherit": "Bring a polished meeting presence with Poly Camera Pro and smart background adjustments.",
      "ultra_short": "Polished meeting presence",
      "ultra_short_safe_to_inherit": "Polished meeting presence"
    },
    "ValueProposition": {
      "headline": "Secure AI Productivity on the Move",
      "long_message_best_sku": "Work smarter from more places with a secure business notebook built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition combines an ultralight 14-inch design, Windows 11 Pro for business, and the latest Intel Core Ultra processor, using three compute engines to manage AI workloads, help improve video conferencing, and allow advanced content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "long_message_safe_to_inherit": "Work smarter from more places with a secure business notebook family built for AI-enhanced work, polished collaboration, connected mobility, and protected productivity. The HP EliteBook X G2i family combines portable design, Windows 11 Pro for business, and Intel Core Ultra processing, using compute engines to manage AI workloads, help improve video conferencing, and allow content creation. Poly Camera Pro keeps you framed and distraction-free with smart background adjustments and spotlight, Wi-Fi 7 supports a reliable connection in dense wireless environments with gigabit data-rate wireless LAN, and HP Wolf Security for Business creates hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so sensitive work, meetings, and decisions can keep moving wherever the day takes you.",
      "mid_length": "Work smarter from more places with an ultralight HP EliteBook built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "mid_length_safe_to_inherit": "Work smarter from more places with an HP EliteBook family built for AI-enhanced productivity, polished video presence, reliable Wi-Fi 7 connectivity, and HP Wolf Security.",
      "short_message": "A secure, ultralight AI PC for productive work and polished collaboration anywhere.",
      "ultra_short": "Secure AI mobility"
    },
    "_chatSession": {
      "responseId": "resp_0836a6860971d1c4006aabef7902b88197a3d08e1215d8cdf7",
      "model": "gpt-5.5"
    }
  },
  "product_name": "Viktor",
  "camera_tag": "Laptop_Front_Right_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging gives mobile business work, meetings, shared workspaces, and customer-site contexts. The selected product-camera pair is recognized, but the Viktor close-up override allows only a clear local surface, light, and neutral background tone with no visible props or people.",
  "count_explanation": "Four numbered KSPs contain usable scene or activity cues. Returned two concise prompts because the tight prop-free view can support distinct shared-work and customer-site meeting contexts, but not documents, call activity, people, or a broader room.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "mobile professionals move through documents, meetings, and decisions"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Used the mobile professional work and meeting cue as a clear shared-work/customer-site surface. Document details were omitted because this view allows no props."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "AI-assisted tasks, calls, and content work"
        }
      ],
      "prompt_ids": [],
      "explanation": "Calls and content work are useful activity cues, but visible call materials, creative tools, or extra hardware would exceed the tight prop-free view."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "work beyond controlled office environments"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "Represented the beyond-office idea as a customer-site meeting surface without adding people, security imagery, or a broader room."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "whether joining from an office, shared workspace, or customer site"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Directly informed the shared-work and customer-site meeting contexts. Meeting participants and visible video-call elements were omitted for view compatibility."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.short_message",
        "quote": "productive work and polished collaboration anywhere"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2"
    ],
    "explanation": "Used as overall context for mobile professional collaboration while keeping the setting local and uncluttered."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Clean matte tabletop",
        "Gentle daylight",
        "Unobtrusive neutral background tone"
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Smooth wood meeting surface",
        "Soft ambient light",
        "Simple neutral backdrop"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Laptop_Front_Right_CloseUp",
    "resolved_tag": "Laptop_Front_Right_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "documents",
          "meeting participants",
          "video-call cues",
          "shared-workspace background details"
        ],
        "explanation": "Retained only a shared-work local surface and soft light because the recognized Viktor close-up view has an override limiting visible props and background details to zero."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "customer-site room context",
          "people",
          "notebooks or forms",
          "security and AI feature visuals"
        ],
        "explanation": "Kept the customer-site cue as a clear meeting surface with neutral background tone; the fixed tight oblique view does not support added props, people, or room fixtures."
      }
    ],
    "requested_product": "Viktor",
    "resolved_product": "Viktor_Sahara-Silver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "f84301924483056329671513cf85cbe3c534b436fb28f8248fb977c7fd5b9176",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "input_raw_sha256": "d1b3c0bdf827fa92859137c81d352897c101ce5370c00b2b0bc0a5ce19f93af8",
  "recorded_input_semantic_sha256": "8acf418210d534aaedf897dcdbf3eb81072be7b0f8ea5590fddcb7154dc1c047",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvvcFe1ro3aseTaPFoNReYPM77Ax",
  "usage": {
    "completion_tokens": 2292,
    "prompt_tokens": 8371,
    "total_tokens": 10663,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1398,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 7936,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 624,
      "engine_ttlt_ms": 22856,
      "pre_inference_ms": 313,
      "service_tbt_ms": 10,
      "service_ttft_ms": 1276,
      "service_ttlt_ms": 23505,
      "user_visible_ttft_ms": 963
    }
  },
  "attempt": 1,
  "latency_seconds": 24.47,
  "started_at": "2026-10-22T22:51:59.948248+00:00",
  "completed_at": "2026-10-22T22:52:24.418166+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "10_actual_laptop_viktor_front_right_closeup",
  "source_id": "22fdbf19f03d1a31",
  "product_name": "Viktor",
  "camera_tag": "Laptop_Front_Right_CloseUp",
  "purpose": "Actual laptop source under the especially tight Viktor override.",
  "input_path": "inputs/10_actual_laptop_viktor_front_right_closeup.json",
  "input_raw_sha256": "d1b3c0bdf827fa92859137c81d352897c101ce5370c00b2b0bc0a5ce19f93af8",
  "input_semantic_sha256": "8acf418210d534aaedf897dcdbf3eb81072be7b0f8ea5590fddcb7154dc1c047",
  "source_kind": "actual",
  "source_semantic_sha256": "22fdbf19f03d1a31516a6638b1ba12df246cbe7ac63637d8e2e77e293f14eed4",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/22fdbf19f03d1a31.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2613589805017517007.zip",
      "member": "Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 2f9616d5-0c90-479d-89dd-4c8b3e0f02fe.json",
      "member": null,
      "sha256": "87351342e53250fae2bacf8a57be3be70f3d03e594bf6140bb910c830ced3ca9"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_CloseUp",
    "resolved_tag": "Laptop_Front_Right_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "oblique",
    "requested_product": "Viktor",
    "resolved_product": "Viktor_Sahara-Silver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "10_actual_laptop_viktor_front_right_closeup",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/10_actual_laptop_viktor_front_right_closeup.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 17,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 18,
      "environment": "Office"
    }
  ],
  "prompt_count": 2,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_CloseUp",
    "resolved_tag": "Laptop_Front_Right_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "oblique",
    "requested_product": "Viktor",
    "resolved_product": "Viktor_Sahara-Silver.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Front_Right_CloseUp",
    "resolved_tag": "Laptop_Front_Right_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "oblique",
    "requested_product": "Viktor",
    "resolved_product": "Viktor_Sahara-Silver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 11_actual_printer_tassel_front_closeup

Second actual printer source with the PDF-only Tassel registry entry.

- Requested product: `Tassel`
- Requested camera: `Printer_Front_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A shared office work area with a clean laminate counter, soft overhead light, and a plain neutral backdrop.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Front_CloseUp",
  "resolved_tag": "Printer_Front_CloseUp",
  "resolution": "exact",
  "requested_product": "Tassel",
  "resolved_product": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Front_CloseUp",
  "effective_profile": {
    "framing": "tight",
    "elevation": "level",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/review/tassel_example_13.png`

SHA-256: `75978b07bc94564bae051725a4424d9c5e49584018c450e3cf2ccb542ad934bc`

```json
{
  "available": true,
  "kind": "exact_pdf_extraction",
  "match_rule": "resolved full product name + source camera name, exact; standalone printer PDF",
  "resolved_product": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
  "source_camera_name": "Front_CloseUp",
  "catalog": {
    "source_id": "standalone_printer_development",
    "pdf_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/originals/asset_comparison_report (1).pdf",
    "pdf_sha256": "b07b4982d407168507e92c515a0cc1869c6866452b5d702e55c2fb3f7f5ddc50",
    "page_number": 2,
    "image_index": 14,
    "pdf_object_name": "Im55.png",
    "camera_name_exact": "Front_CloseUp",
    "width_px": 1024,
    "height_px": 576,
    "encoded_bytes": 57524,
    "sha256": "75978b07bc94564bae051725a4424d9c5e49584018c450e3cf2ccb542ad934bc",
    "pixel_exact_with_matched_zip_asset": null,
    "matched_zip_filename": null
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/review/tassel_example_13.png",
    "bytes": 57524,
    "sha256": "75978b07bc94564bae051725a4424d9c5e49584018c450e3cf2ccb542ad934bc",
    "mime_type": "image/png"
  },
  "index_note": "Local filename suffix 13 is the zero-based extraction position; the catalog's one-based PDF image_index is 14."
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Keep shared work moving\n\nOR\n\nFewer steps at the printer",
      "long_message_best_sku": "Daily document work can move with fewer manual steps. The HP LaserJet Enterprise 6501dn Printer series supports automatic two-sided printing and a 4.3-inch color touchscreen, giving walk-up users a simpler way to start jobs and keep recurring reports, forms, and packets flowing through busy workdays.",
      "long_message_safe_to_inherit": "Daily document work can move with fewer manual steps. The HP LaserJet Enterprise 6501dn Printer series supports automatic two-sided printing and a color touchscreen, giving walk-up users a simpler way to start jobs and keep recurring reports, forms, and packets flowing through busy workdays.",
      "mid_length": "Daily document work can move with fewer manual steps. Automatic two-sided printing and a 4.3-inch color touchscreen simplify shared walk-up use for teams.",
      "mid_length_safe_to_inherit": "Daily document work can move with fewer manual steps. Automatic two-sided printing and a color touchscreen simplify shared walk-up use for teams.",
      "short_message": "Fewer manual steps help shared teams keep daily document work moving all day.",
      "short_message_safe_to_inherit": "Fewer manual steps help shared teams keep daily document work moving all day.",
      "ultra_short": "Fewer print steps",
      "ultra_short_safe_to_inherit": "Fewer print steps"
    },
    "KSP2": {
      "headline": "Protection for shared print\n\nOR\n\nSecure the print endpoint",
      "long_message_best_sku": "Shared print environments can reduce endpoint risk while keeping work accessible to authorized users. The HP LaserJet Enterprise 6501dn Printer series includes HP Sure Start and Memory Shield, helping IT add embedded protection to a networked device that supports everyday black-and-white printing and policy-driven operations across large teams.",
      "long_message_safe_to_inherit": "Shared print environments can reduce endpoint risk while keeping work accessible to authorized users. The HP LaserJet Enterprise 6501dn Printer series includes embedded HP protection technologies, helping IT add protection to a networked device that supports everyday black-and-white printing and policy-driven operations across large teams.",
      "mid_length": "Shared print environments can reduce endpoint risk. HP Sure Start and Memory Shield help IT add embedded protection to everyday black-and-white printing.",
      "mid_length_safe_to_inherit": "Shared print environments can reduce endpoint risk. Embedded HP protection technologies help IT add protection to everyday black-and-white printing.",
      "short_message": "Reduce endpoint risk while keeping shared black-and-white printing accessible to authorized users and teams.",
      "short_message_safe_to_inherit": "Reduce endpoint risk while keeping shared black-and-white printing accessible to authorized users and teams.",
      "ultra_short": "Protected shared printing",
      "ultra_short_safe_to_inherit": "Protected shared printing"
    },
    "KSP3": {
      "headline": "Fit the fleet\n\nOR\n\nBuilt for IT standards",
      "long_message_best_sku": "Fleet updates and workflow needs are easier to handle when printers fit existing IT models. The HP LaserJet Enterprise 6501dn Printer series supports HP FutureSmart firmware and HP Web Jetadmin, helping administrators align shared print deployments with fleet visibility, firmware planning, and standardized management practices without forcing a separate device approach.",
      "long_message_safe_to_inherit": "Fleet updates and workflow needs are easier to handle when printers fit existing IT models. The HP LaserJet Enterprise 6501dn Printer series supports enterprise firmware and fleet management tools, helping administrators align shared print deployments with fleet visibility, firmware planning, and standardized management practices without forcing a separate device approach.",
      "mid_length": "Fleet updates and workflow needs are easier to handle. HP FutureSmart firmware and HP Web Jetadmin support standardized management across shared print deployments.",
      "mid_length_safe_to_inherit": "Fleet updates and workflow needs are easier to handle. Enterprise firmware and fleet management tools support standardized management across shared print deployments.",
      "short_message": "Manage shared print deployments with firmware and fleet tools that fit IT standards.",
      "short_message_safe_to_inherit": "Manage shared print deployments with firmware and fleet tools that fit IT standards.",
      "ultra_short": "Fleet-ready fit",
      "ultra_short_safe_to_inherit": "Fleet-ready fit"
    },
    "KSP4": {
      "headline": "Capacity for busy teams\n\nOR\n\nPaper handling that scales",
      "long_message_best_sku": "Large teams can handle changing document volumes with fewer paper interruptions. The HP LaserJet Enterprise 6501dn Printer series starts with 650-sheet standard input capacity and expands to 2,850 sheets, so departments can support recurring print work and varied workloads from a shared device.",
      "long_message_safe_to_inherit": "Large teams can handle changing document volumes with fewer paper interruptions. The HP LaserJet Enterprise 6501dn Printer series starts with substantial standard input capacity and expands with additional paper handling, so departments can support recurring print work and varied workloads from a shared device.",
      "mid_length": "Large teams can handle changing document volumes. 650-sheet standard input capacity expands to 2,850 sheets to support recurring shared print work.",
      "mid_length_safe_to_inherit": "Large teams can handle changing document volumes. Standard input capacity expands with additional paper handling to support recurring shared print work.",
      "short_message": "Handle changing document volumes with input capacity that expands to 2,850 sheets for shared teams.",
      "short_message_safe_to_inherit": "Handle changing document volumes with input capacity that expands for shared teams.",
      "ultra_short": "Capacity that scales",
      "ultra_short_safe_to_inherit": "Capacity that scales"
    },
    "ValueProposition": {
      "headline": "Enterprise printing that fits the fleet",
      "long_message_best_sku": "Give large teams a shared A4 mono printer that keeps black-and-white work moving, strengthens endpoint protection, and fits the fleet standards IT already manages. The HP LaserJet Enterprise 6501dn Printer series supports high-volume departments with automatic two-sided printing, a 4.3-inch color touchscreen, 650-sheet standard input capacity, and paper input expandable to 2,850 sheets, helping users spend less time at the device and teams reduce avoidable interruptions for recurring forms, reports, schedules, and everyday operational documents. Built with HP Wolf security, HP Sure Start, Memory Shield, Connection Inspector, HP FutureSmart firmware, Workpath enablement, OXPd, HP Web Jetadmin, and Hardware Integration Pocket 2nd generation, it gives IT a managed enterprise endpoint that can support policy-aligned deployment, workflow extensibility, and changing department demand without adding unnecessary complexity.",
      "long_message_safe_to_inherit": "Give large teams a shared A4 mono printer that keeps black-and-white work moving, strengthens endpoint protection, and fits the fleet standards IT already manages. The HP LaserJet Enterprise 6501dn Printer series supports high-volume departments with automatic two-sided printing, an intuitive touchscreen, substantial standard input capacity, and expandable paper input, helping users spend less time at the device and teams reduce avoidable interruptions for recurring forms, reports, schedules, and everyday operational documents. Built with HP Wolf security, embedded HP protection technologies, enterprise firmware, workflow enablement, fleet management tools, and an integration pocket, it gives IT a managed enterprise endpoint that can support policy-aligned deployment, workflow extensibility, and changing department demand without adding unnecessary complexity.",
      "mid_length": "Keep shared A4 mono printing moving with HP Wolf security, fleet-ready firmware, automatic duplexing, and scalable paper capacity for large teams.",
      "mid_length_safe_to_inherit": "Keep shared A4 mono printing moving with HP Wolf security, fleet-ready firmware, automatic duplexing, and scalable paper capacity for large teams.",
      "short_message": "Shared A4 mono printing with embedded security, fleet manageability, duplexing, and scalable capacity.",
      "ultra_short": "Enterprise print ready"
    },
    "_chatSession": {
      "responseId": "resp_0f1982f131b4e532006aa12a8d9c2c8193a10869b8359d26a5",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Tassel",
  "camera_tag": "Printer_Front_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging consistently points to a shared enterprise office print environment for large teams, recurring forms, reports, schedules, and department document workflows. The selected close, level front view supports only a minimal local setting without props or people.",
  "count_explanation": "Four KSPs contain useful workplace or shared-team cues, but they overlap into one office scenario and the tight view allows no visible props or background details. Returned one consolidated prompt.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring reports, forms, and packets flowing through busy workdays"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The shared document-work cue supports an office work area, but reports, forms, packets, and walk-up activity were omitted because this close level preset permits no props or people."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "Shared print environments can reduce endpoint risk while keeping work accessible to authorized users."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The shared environment supports the office family. Endpoint security and authorized access are abstract benefits, so they were not visualized as guards, badges, or technical displays."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "helping administrators align shared print deployments with fleet visibility, firmware planning, and standardized management practices"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The administrator and shared-deployment wording reinforces an enterprise office context. Fleet tools, firmware planning, and management practices are not directly visible in this tight view."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Large teams can handle changing document volumes with fewer paper interruptions."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Large-team document volume supports a shared office work area. Paper stacks and workload cues were omitted to respect the no-prop limit for the selected view."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "recurring forms, reports, schedules, and everyday operational documents"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The value proposition consolidates the department document workflow context into a simple shared office setting, without adding visible documents due to the camera limits."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Clean laminate counter",
        "Soft overhead light",
        "Plain neutral backdrop"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Front_CloseUp",
    "resolved_tag": "Printer_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "Visible reports, forms, packets, schedules, and paper stacks",
          "Walk-up users, administrators, and large-team activity",
          "Fleet, firmware, security, and endpoint-management concepts"
        ],
        "explanation": "The product resolved by alias to a supported printer, and the exact camera tag resolves to a tight, level preset with zero local props, zero background details, and no people. The prompt retains only a shared office surface, simple light, and neutral backdrop."
      }
    ],
    "requested_product": "Tassel",
    "resolved_product": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "1353b569837d887b8d44f6af5d8865061b69899b6b51625f474721fbafe808e2",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "160db92655412f4d41d349bbf6f930adc248c6485b804ff4cade8824355b5710",
  "input_raw_sha256": "5f1f88a4f02cfc3aea84b9ed0fbc9d2705d28a89a9c3e877b8bd503d71453345",
  "recorded_input_semantic_sha256": "438b3b96fc6802fd17b066829bad717faab4c388afb036b1f0ff9645c9a8242b",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-Ebvw13P964zv21rI43JJ5ok3EaEG9",
  "usage": {
    "completion_tokens": 1343,
    "prompt_tokens": 12969,
    "total_tokens": 14312,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 512,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 3840,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 314,
      "engine_ttlt_ms": 12137,
      "pre_inference_ms": 321,
      "service_tbt_ms": 9,
      "service_ttft_ms": 985,
      "service_ttlt_ms": 12803,
      "user_visible_ttft_ms": 664
    }
  },
  "attempt": 1,
  "latency_seconds": 13.591,
  "started_at": "2026-10-22T22:52:24.442138+00:00",
  "completed_at": "2026-10-22T22:52:38.033060+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "11_actual_printer_tassel_front_closeup",
  "source_id": "160db92655412f4d",
  "product_name": "Tassel",
  "camera_tag": "Printer_Front_CloseUp",
  "purpose": "Second actual printer source with the PDF-only Tassel registry entry.",
  "input_path": "inputs/11_actual_printer_tassel_front_closeup.json",
  "input_raw_sha256": "5f1f88a4f02cfc3aea84b9ed0fbc9d2705d28a89a9c3e877b8bd503d71453345",
  "input_semantic_sha256": "438b3b96fc6802fd17b066829bad717faab4c388afb036b1f0ff9645c9a8242b",
  "source_kind": "actual",
  "source_semantic_sha256": "160db92655412f4d41d349bbf6f930adc248c6485b804ff4cade8824355b5710",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/160db92655412f4d.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2299778737384020264.zip",
      "member": "Source Messaging - 71bd2bda-ecc2-4841-bd21-30a6c05673a9.json",
      "sha256": "afdf3ed48a702c2d4bb475ddd54274754fda7bebf6d542c6abb3c41624428943"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Front_CloseUp",
    "resolved_tag": "Printer_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Tassel",
    "resolved_product": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "11_actual_printer_tassel_front_closeup",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/11_actual_printer_tassel_front_closeup.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 18,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Front_CloseUp",
    "resolved_tag": "Printer_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Tassel",
    "resolved_product": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Front_CloseUp",
    "resolved_tag": "Printer_Front_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Tassel",
    "resolved_product": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 12_synthetic_gaming_cheddar_front_right_wide

Synthetic grounded Gaming cues under a known wide laptop view.

- Requested product: `Cheddar`
- Requested camera: `Laptop_Front_Right_Wide`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Gaming**

A comfortable home play desk with a smooth wooden surface, a game controller, and a soft desk mat. A short shelf of favorite collectibles sits quietly in the background under relaxed evening light.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Front_Right_Wide",
  "resolved_tag": "Laptop_Front_Right_Wide",
  "resolution": "exact",
  "requested_product": "Cheddar",
  "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Front_Right_Wide",
  "effective_profile": {
    "framing": "wide",
    "elevation": "oblique",
    "max_local_props": 3,
    "max_background_details": 2,
    "people_policy": "optional_if_supported_and_unobtrusive"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Wide.png`

SHA-256: `572ca8fd51b9dbf174c9b8b5032290beb89569b07fb7e9e95152146cd311eb6a`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
  "source_camera_name": "Front_Right_Wide",
  "catalog": {
    "device_id": "camera_laptop.locator_Cheddar-13_NaturalSilver.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Cheddar-13_NaturalSilver.laptop.usdz",
    "camera_name_exact": "Front_Right_Wide",
    "zip_filename": "Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Wide.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Wide.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 25625,
    "sha256": "572ca8fd51b9dbf174c9b8b5032290beb89569b07fb7e9e95152146cd311eb6a",
    "zip_crc32": "81add345"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Wide.png",
    "bytes": 25625,
    "sha256": "572ca8fd51b9dbf174c9b8b5032290beb89569b07fb7e9e95152146cd311eb6a",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "long_message_best_sku": "Evening gaming at home with a comfortable desk setup and a shelf of favorite collectibles."
    },
    "ValueProposition": {
      "headline": "A relaxing space for play"
    }
  },
  "product_name": "Cheddar",
  "camera_tag": "Laptop_Front_Right_Wide"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "KSP1 provides a concrete home gaming setting with a desk and collectibles. The value proposition reinforces a relaxed play space.",
  "count_explanation": "There is 1 KSP with useful explicit scene cues, so 1 prompt was returned.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "Evening gaming at home with a comfortable desk setup and a shelf of favorite collectibles."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Used the home gaming, desk, evening, and collectibles cues while keeping the scene local to the wide oblique view."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.headline",
        "quote": "A relaxing space for play"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "Used to support the relaxed gaming mood and subdued evening light."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Smooth wooden surface added as a plausible local desk material.",
        "Game controller and soft desk mat added as ordinary gaming-context props within the wide-view limits."
      ]
    }
  ],
  "ignored_fields": [],
  "camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "No full room layout or person added.",
          "Collectibles simplified to one short background shelf.",
          "Desk setup kept free of extra computing hardware."
        ],
        "explanation": "The selected wide oblique preset allows up to three nearby props and two simple background details, so the prompt keeps two local props and one subordinate shelf detail without describing the target device or changing the view."
      }
    ],
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "90290b0899dc2795dbc43f225961ce8cef15acc1edfc6ccf81abed330ff9b4ca",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "048217039fd093b2ad6819c601d3e2293a8616e943eeb6b605d56e3063d9a56f",
  "input_raw_sha256": "2b67741813b00812a8f4b99d68dfeb6a003993f39e2dadfe032db676f1fafccb",
  "recorded_input_semantic_sha256": "73daac251459c36be483f6ac27385166bf439e6ac08158bde40cc44897bed6fb",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvwEQwbQalImhpVyREK3VSBaVucT",
  "usage": {
    "completion_tokens": 837,
    "prompt_tokens": 6656,
    "total_tokens": 7493,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 345,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 3840,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 309,
      "engine_ttlt_ms": 7744,
      "pre_inference_ms": 339,
      "service_tbt_ms": 9,
      "service_ttft_ms": 1120,
      "service_ttlt_ms": 8472,
      "user_visible_ttft_ms": 781
    }
  },
  "attempt": 1,
  "latency_seconds": 9.714,
  "started_at": "2026-10-22T22:52:38.057499+00:00",
  "completed_at": "2026-10-22T22:52:47.771430+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "12_synthetic_gaming_cheddar_front_right_wide",
  "source_id": "048217039fd093b2",
  "product_name": "Cheddar",
  "camera_tag": "Laptop_Front_Right_Wide",
  "purpose": "Synthetic grounded Gaming cues under a known wide laptop view.",
  "input_path": "inputs/12_synthetic_gaming_cheddar_front_right_wide.json",
  "input_raw_sha256": "2b67741813b00812a8f4b99d68dfeb6a003993f39e2dadfe032db676f1fafccb",
  "input_semantic_sha256": "73daac251459c36be483f6ac27385166bf439e6ac08158bde40cc44897bed6fb",
  "source_kind": "synthetic",
  "source_semantic_sha256": "048217039fd093b2ad6819c601d3e2293a8616e943eeb6b605d56e3063d9a56f",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/gaming.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/gaming.json",
      "member": null,
      "synthetic": true
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "12_synthetic_gaming_cheddar_front_right_wide",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/12_synthetic_gaming_cheddar_front_right_wide.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 33,
      "environment": "Gaming"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 1,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Front_Right_Wide",
    "resolved_tag": "Laptop_Front_Right_Wide",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "wide",
    "elevation": "oblique",
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 13_empty_source_unknown_camera

Empty source plus unknown camera must use the conservative minimal fallback.

- Requested product: `Magic`
- Requested camera: `Printer_Unregistered_View`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Home**

A simple clean work surface in soft natural light with a calm neutral background.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Unregistered_View",
  "resolved_tag": null,
  "resolution": "unknown",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": null,
  "source_camera_name": null,
  "effective_profile": {
    "framing": "unknown",
    "elevation": "unknown",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": true
}
```

### Matching offline camera reference

Unavailable: `camera_unknown_or_missing`.

```json
{
  "available": false,
  "reason": "camera_unknown_or_missing"
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {},
  "product_name": "Magic",
  "camera_tag": "Printer_Unregistered_View"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "source_messaging is empty, so no KSP or ValueProposition scene cues were available. Product matched an explicit alias, but the requested camera tag is unregistered, requiring the conservative minimal scene policy.",
  "count_explanation": "With no usable numbered KSPs and an unknown camera, one minimal fallback prompt was returned.",
  "used_fallback": true,
  "ksp_mappings": [],
  "value_proposition": {
    "source_evidence": [],
    "prompt_ids": [],
    "explanation": "No ValueProposition was present."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Clean local work surface",
        "Soft natural light",
        "Neutral background tone"
      ]
    }
  ],
  "ignored_fields": [],
  "camera": {
    "requested_tag": "Printer_Unregistered_View",
    "resolved_tag": null,
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "unknown",
    "framing": "unknown",
    "elevation": "unknown",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "No props",
          "No people",
          "No named room fixtures",
          "No source-specific scenario"
        ],
        "explanation": "The camera tag is unregistered, so the prompt keeps only a minimal support surface, light, and neutral background without assuming view capacity or product-camera compatibility."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "13c5562297acd0efb0f4306d37514f285b87fcba507d7318e7679a7c9f232695",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
  "input_raw_sha256": "668d28944f2236be9d4298ddc5754dc8ad9abc09908d0288d7196fa0ee7292a1",
  "recorded_input_semantic_sha256": "d82300a54459013135a546936a12997f8c06dd25c611ed8766c1453d94af535e",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvwO1HCIuBHnzwc2szGRxp3RCIWH",
  "usage": {
    "completion_tokens": 547,
    "prompt_tokens": 6596,
    "total_tokens": 7143,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 211,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 319,
      "engine_ttlt_ms": 5148,
      "pre_inference_ms": 139,
      "service_tbt_ms": 9,
      "service_ttft_ms": 906,
      "service_ttlt_ms": 5706,
      "user_visible_ttft_ms": 767
    }
  },
  "attempt": 1,
  "latency_seconds": 6.239,
  "started_at": "2026-10-22T22:52:47.794929+00:00",
  "completed_at": "2026-10-22T22:52:54.033657+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "13_empty_source_unknown_camera",
  "source_id": "44136fa355b3678a",
  "product_name": "Magic",
  "camera_tag": "Printer_Unregistered_View",
  "purpose": "Empty source plus unknown camera must use the conservative minimal fallback.",
  "input_path": "inputs/13_empty_source_unknown_camera.json",
  "input_raw_sha256": "668d28944f2236be9d4298ddc5754dc8ad9abc09908d0288d7196fa0ee7292a1",
  "input_semantic_sha256": "d82300a54459013135a546936a12997f8c06dd25c611ed8766c1453d94af535e",
  "source_kind": "synthetic",
  "source_semantic_sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/empty.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/empty.json",
      "member": null,
      "synthetic": true
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Unregistered_View",
    "resolved_tag": null,
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "unknown",
    "framing": "unknown",
    "elevation": "unknown",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "13_empty_source_unknown_camera",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/13_empty_source_unknown_camera.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 14,
      "environment": "Home"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 0,
  "used_fallback": true,
  "expected_camera": {
    "requested_tag": "Printer_Unregistered_View",
    "resolved_tag": null,
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "unknown",
    "framing": "unknown",
    "elevation": "unknown",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Unregistered_View",
    "resolved_tag": null,
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "unknown",
    "framing": "unknown",
    "elevation": "unknown",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 14_technical_only_known_tight_camera

Technical-only source under a known tight camera must not invent a technical scene.

- Requested product: `Koki`
- Requested camera: `Laptop_Back_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Home**

A calm home work surface in pale wood, lit by soft daylight against a simple neutral backdrop.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Back_CloseUp",
  "resolved_tag": "Laptop_Back_CloseUp",
  "resolution": "exact",
  "requested_product": "Koki",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Back_CloseUp",
  "effective_profile": {
    "framing": "tight",
    "elevation": "level",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Back_CloseUp.png`

SHA-256: `fdf14775fd8edce685455301419da881d87b7cfe94a7d28bfcacc58e17ad57e9`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
  "source_camera_name": "Back_CloseUp",
  "catalog": {
    "device_id": "camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "camera_name_exact": "Back_CloseUp",
    "zip_filename": "Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Back_CloseUp.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Back_CloseUp.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 61635,
    "sha256": "fdf14775fd8edce685455301419da881d87b7cfe94a7d28bfcacc58e17ad57e9",
    "zip_crc32": "476a6c6c"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop/camera_laptop.locator_Koki-Omnibook_Eclipes-Gray.laptop_Back_CloseUp.png",
    "bytes": 61635,
    "sha256": "fdf14775fd8edce685455301419da881d87b7cfe94a7d28bfcacc58e17ad57e9",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "long_message_best_sku": "32 GB RAM, 1 TB SSD, 12-core CPU."
    },
    "KSP2": {
      "long_message_best_sku": "Wi-Fi 7 and hardware-enforced encryption."
    },
    "ValueProposition": {
      "headline": "Fast and secure technology"
    }
  },
  "product_name": "Koki",
  "camera_tag": "Laptop_Back_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging is limited to technical specifications and abstract security/performance claims, with no explicit setting, activity, people, or concrete materials. Product matched by explicit alias; camera matched exactly.",
  "count_explanation": "Useful scene-cue KSP count U=0, so one minimal fallback prompt was returned. The tight level view permits no visible props or background details.",
  "used_fallback": true,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "32 GB RAM, 1 TB SSD, 12-core CPU."
        }
      ],
      "prompt_ids": [],
      "explanation": "Technical hardware specifications do not provide a concrete lifestyle setting or activity cue."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "Wi-Fi 7 and hardware-enforced encryption."
        }
      ],
      "prompt_ids": [],
      "explanation": "Connectivity and encryption claims are abstract benefits here; they were not converted into a visible location, security scene, or extra props."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.headline",
        "quote": "Fast and secure technology"
      }
    ],
    "prompt_ids": [],
    "explanation": "The value proposition supports a general clean workspace mood but is too abstract to ground a distinct scene."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wooden local work surface",
        "Soft daylight",
        "Simple neutral backdrop"
      ]
    }
  ],
  "ignored_fields": [],
  "camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "RAM, storage, and CPU specifications",
          "Wi-Fi and encryption visualization",
          "Props, people, and named room fixtures"
        ],
        "explanation": "The retained scene is limited to a local support surface, light, and plain backdrop because this tight level preset allows zero props and zero background details, and the source contains no concrete scene cues."
      }
    ],
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "6e71976f42eff06237c88bb73b7edeb8dd108195e33abc6abf437faac4e00503",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "49aa979045b3b3d63ccf450a1267d24a849fe23da3777dcc2281b1f951911bdf",
  "input_raw_sha256": "1c43221ec3e1e2336f1cd312ab004bdc80851dda02d7265ef3170cc03698fd0b",
  "recorded_input_semantic_sha256": "53af3123f37206ffbf4acb723351eefe551d3706208fd407a2f985c1211f5180",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvwUyW6BSqRPpN2dqh9VPlPZM0PY",
  "usage": {
    "completion_tokens": 951,
    "prompt_tokens": 6678,
    "total_tokens": 7629,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 406,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 358,
      "engine_ttlt_ms": 9680,
      "pre_inference_ms": 200,
      "service_tbt_ms": 10,
      "service_ttft_ms": 856,
      "service_ttlt_ms": 10171,
      "user_visible_ttft_ms": 656
    }
  },
  "attempt": 1,
  "latency_seconds": 10.702,
  "started_at": "2026-10-22T22:52:54.056649+00:00",
  "completed_at": "2026-10-22T22:53:04.759043+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "14_technical_only_known_tight_camera",
  "source_id": "49aa979045b3b3d6",
  "product_name": "Koki",
  "camera_tag": "Laptop_Back_CloseUp",
  "purpose": "Technical-only source under a known tight camera must not invent a technical scene.",
  "input_path": "inputs/14_technical_only_known_tight_camera.json",
  "input_raw_sha256": "1c43221ec3e1e2336f1cd312ab004bdc80851dda02d7265ef3170cc03698fd0b",
  "input_semantic_sha256": "53af3123f37206ffbf4acb723351eefe551d3706208fd407a2f985c1211f5180",
  "source_kind": "synthetic",
  "source_semantic_sha256": "49aa979045b3b3d63ccf450a1267d24a849fe23da3777dcc2281b1f951911bdf",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/technical_only.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/edge_cases/technical_only.json",
      "member": null,
      "synthetic": true
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "14_technical_only_known_tight_camera",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/14_technical_only_known_tight_camera.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 17,
      "environment": "Home"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 0,
  "used_fallback": true,
  "expected_camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Koki",
    "resolved_product": "Koki-Omnibook_Eclipes-Gray.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 15_known_type_conflict_magic_laptop_camera

Known printer product with a known laptop camera must resolve as incompatible.

- Requested product: `Magic`
- Requested camera: `Laptop_Back_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A simple neutral work surface in soft daylight, with a clean backdrop and minimal surrounding detail.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Back_CloseUp",
  "resolved_tag": "Laptop_Back_CloseUp",
  "resolution": "exact",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "incompatible",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Back_CloseUp",
  "effective_profile": {
    "framing": "unknown",
    "elevation": "unknown",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": "product_family_conflicts_with_camera_family",
  "used_minimal_fallback": true
}
```

### Matching offline camera reference

Unavailable: `product_family_conflicts_with_camera_family`.

```json
{
  "available": false,
  "reason": "product_family_conflicts_with_camera_family"
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Included ink value\n\nOR\n\nPrint longer between refills",
      "long_message_best_sku": "Print longer with fewer refill interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "long_message_safe_to_inherit": "Print longer with fewer refill interruptions. This HP Smart Tank all-in-one includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "mid_length": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "mid_length_safe_to_inherit": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "short_message": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "ultra_short": "Fewer refill interruptions",
      "ultra_short_safe_to_inherit": "Fewer refill interruptions"
    },
    "KSP2": {
      "headline": "Ready for recurring print work\n\nOR\n\nEveryday output that keeps moving",
      "long_message_best_sku": "Keep recurring print work moving through busy stretches. HP Smart Tank 7602 All-in-One is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "long_message_safe_to_inherit": "Keep recurring print work moving through busy stretches. This HP Smart Tank all-in-one is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "mid_length": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "mid_length_safe_to_inherit": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "short_message": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "short_message_safe_to_inherit": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "ultra_short": "Everyday productivity",
      "ultra_short_safe_to_inherit": "Everyday productivity"
    },
    "KSP3": {
      "headline": "Less handling for longer tasks\n\nOR\n\nMulti-page work made easier",
      "long_message_best_sku": "Move through multi-page tasks with fewer manual steps. HP Smart Tank 7602 All-in-One pairs a 35-page auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "long_message_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. This HP Smart Tank all-in-one pairs an auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "mid_length": "Move through multi-page tasks with fewer manual steps. A 35-page auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "mid_length_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. An auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "short_message": "A 35-page auto document feeder and automatic two-sided printing reduce manual handling.",
      "short_message_safe_to_inherit": "An auto document feeder and automatic two-sided printing reduce manual handling.",
      "ultra_short": "Fewer manual steps",
      "ultra_short_safe_to_inherit": "Fewer manual steps"
    },
    "KSP4": {
      "headline": "Connections that fit your setup\n\nOR\n\nFlexible ways to get printing",
      "long_message_best_sku": "Connect the way your devices work. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "long_message_safe_to_inherit": "Connect the way your devices work. This HP Smart Tank all-in-one supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "mid_length": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "mid_length_safe_to_inherit": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "short_message": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "short_message_safe_to_inherit": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "ultra_short": "Flexible connections",
      "ultra_short_safe_to_inherit": "Flexible connections"
    },
    "ValueProposition": {
      "headline": "Print more with fewer interruptions",
      "long_message_best_sku": "Keep recurring print, scan, copy, and fax work moving with a high-capacity all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. HP Smart Tank 7602 All-in-One pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, a 35-page auto document feeder, fax, and a 3-inch touchscreen, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "long_message_safe_to_inherit": "Keep recurring print, scan, copy, and fax work moving with a high-capacity HP Smart Tank all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. It pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, an auto document feeder, fax, and touchscreen control, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "mid_length": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "mid_length_safe_to_inherit": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "short_message": "Included ink, workflow tools, and flexible connections keep recurring printing moving.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0d2b454316ccbd87006aa461cfe69c81978dbfd3b1d9a87744",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Magic",
  "camera_tag": "Laptop_Back_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "Source messaging centers on recurring document output, forms, records, handouts, admin paperwork, and shared connectivity. The requested product resolves to a printer alias, but the requested camera is a laptop-family preset, so the scene was reduced to a minimal compatible surface-and-light fallback.",
  "count_explanation": "Several KSPs contain useful paperwork or desk activity cues, but the incompatible product-camera pairing requires a single minimal prompt with no props, people, or named room fixtures.",
  "used_fallback": true,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring document and color jobs"
        }
      ],
      "prompt_ids": [],
      "explanation": "The recurring print-work cue is useful, but visible job materials were omitted because the product-camera combination is incompatible and requires a minimal fallback."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, records, handouts, and color materials"
        }
      ],
      "prompt_ids": [],
      "explanation": "Forms, records, handouts, and color materials suggest a paperwork setting, but props were omitted under the incompatible-camera fallback."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "forms, records, and everyday admin work easier to complete at the desk"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The desk/admin-work cue supports a simple local work surface, simplified to avoid visible paperwork or handling details in the fallback view."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "nearby devices or a shared network"
        }
      ],
      "prompt_ids": [],
      "explanation": "The shared setup cue is useful context, but devices, networks, and additional desk items were not represented because the fallback permits no props or room details."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "regular document queues, household administration, and everyday business paperwork"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The value proposition supports a practical paperwork/work-surface context, reduced to a neutral local surface because of the incompatible camera-product pairing."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Neutral work surface",
        "Soft daylight",
        "Clean minimal backdrop"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "unknown",
    "elevation": "unknown",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "paperwork props",
          "forms and records",
          "handouts and color materials",
          "nearby devices and shared-network cues",
          "people and room fixtures"
        ],
        "explanation": "The camera tag is a registered laptop preset, while the requested product resolves by alias to the Magic printer asset. Because this is an unsupported family combination, the prompt keeps only a local support surface, soft light, and a plain backdrop."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "incompatible"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "f3ceec0b094b7af10b671a6f16446ef6ae40c2d8edb878567337c68e0d5daf19",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "input_raw_sha256": "a9da453e292578696b7bc658d3ff951014ed9ea664b2a7d39904f456da499b8a",
  "recorded_input_semantic_sha256": "8efbbb838b545dd836b801234af8a36f1ad805a10c993ffb313303a9e0b4cda2",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvwfTraKS3nVv2qRpekFEXZaNNWS",
  "usage": {
    "completion_tokens": 1803,
    "prompt_tokens": 13014,
    "total_tokens": 14817,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 12544,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 323,
      "engine_ttlt_ms": 17689,
      "pre_inference_ms": 145,
      "service_tbt_ms": 10,
      "service_ttft_ms": 898,
      "service_ttlt_ms": 18258,
      "user_visible_ttft_ms": 753
    }
  },
  "attempt": 1,
  "latency_seconds": 18.988,
  "started_at": "2026-10-22T22:53:04.785030+00:00",
  "completed_at": "2026-10-22T22:53:23.772898+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "15_known_type_conflict_magic_laptop_camera",
  "source_id": "ee810cf51bb82bb4",
  "product_name": "Magic",
  "camera_tag": "Laptop_Back_CloseUp",
  "purpose": "Known printer product with a known laptop camera must resolve as incompatible.",
  "input_path": "inputs/15_known_type_conflict_magic_laptop_camera.json",
  "input_raw_sha256": "a9da453e292578696b7bc658d3ff951014ed9ea664b2a7d39904f456da499b8a",
  "input_semantic_sha256": "8efbbb838b545dd836b801234af8a36f1ad805a10c993ffb313303a9e0b4cda2",
  "source_kind": "actual",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
      "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "member": null,
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "unknown",
    "elevation": "unknown",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "incompatible"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "15_known_type_conflict_magic_laptop_camera",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/15_known_type_conflict_magic_laptop_camera.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 16,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 4,
  "used_fallback": true,
  "expected_camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "unknown",
    "elevation": "unknown",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "incompatible"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Back_CloseUp",
    "resolved_tag": "Laptop_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "unknown",
    "elevation": "unknown",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "incompatible"
  }
}
```

</details>

## 16_unknown_product_known_printer_camera

Unknown product with a known camera must use the conservative camera base.

- Requested product: `Unregistered_Product`
- Requested camera: `Printer_Back_CloseUp`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A practical office desk surface in pale wood, kept uncluttered under soft daylight with a simple neutral backdrop.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Back_CloseUp",
  "resolved_tag": "Printer_Back_CloseUp",
  "resolution": "exact",
  "requested_product": "Unregistered_Product",
  "resolved_product": null,
  "product_resolution": "unknown",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Back_CloseUp",
  "effective_profile": {
    "framing": "tight",
    "elevation": "level",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Unavailable: `product_unknown_or_missing`.

```json
{
  "available": false,
  "reason": "product_unknown_or_missing"
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Included ink value\n\nOR\n\nPrint longer between refills",
      "long_message_best_sku": "Print longer with fewer refill interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "long_message_safe_to_inherit": "Print longer with fewer refill interruptions. This HP Smart Tank all-in-one includes Original HP Ink in the box and uses a refillable tank system designed for frequent printing, giving recurring document and color jobs a more predictable supply path. You spend less time thinking about replacement ink and more time finishing the pages you need.",
      "mid_length": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "mid_length_safe_to_inherit": "Print longer with fewer refill interruptions. Included Original HP Ink and a refillable tank system help make recurring print needs easier to manage.",
      "short_message": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps recurring print jobs move with fewer refill interruptions.",
      "ultra_short": "Fewer refill interruptions",
      "ultra_short_safe_to_inherit": "Fewer refill interruptions"
    },
    "KSP2": {
      "headline": "Ready for recurring print work\n\nOR\n\nEveryday output that keeps moving",
      "long_message_best_sku": "Keep recurring print work moving through busy stretches. HP Smart Tank 7602 All-in-One is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "long_message_safe_to_inherit": "Keep recurring print work moving through busy stretches. This HP Smart Tank all-in-one is designed for frequent everyday printing, with a monthly duty cycle and published black and color print speeds that support regular document production. It helps manage forms, records, handouts, and color materials without treating each print run like a special project.",
      "mid_length": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "mid_length_safe_to_inherit": "Keep recurring print work moving through busy stretches. A monthly duty cycle and published black and color print speeds support everyday document output.",
      "short_message": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "short_message_safe_to_inherit": "Designed for frequent printing, it helps recurring documents and color pages keep moving.",
      "ultra_short": "Everyday productivity",
      "ultra_short_safe_to_inherit": "Everyday productivity"
    },
    "KSP3": {
      "headline": "Less handling for longer tasks\n\nOR\n\nMulti-page work made easier",
      "long_message_best_sku": "Move through multi-page tasks with fewer manual steps. HP Smart Tank 7602 All-in-One pairs a 35-page auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "long_message_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. This HP Smart Tank all-in-one pairs an auto document feeder with automatic two-sided printing, so longer paperwork and repeated document sets require less hands-on page handling. It helps make forms, records, and everyday admin work easier to complete at the desk.",
      "mid_length": "Move through multi-page tasks with fewer manual steps. A 35-page auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "mid_length_safe_to_inherit": "Move through multi-page tasks with fewer manual steps. An auto document feeder and automatic two-sided printing reduce hands-on page handling.",
      "short_message": "A 35-page auto document feeder and automatic two-sided printing reduce manual handling.",
      "short_message_safe_to_inherit": "An auto document feeder and automatic two-sided printing reduce manual handling.",
      "ultra_short": "Fewer manual steps",
      "ultra_short_safe_to_inherit": "Fewer manual steps"
    },
    "KSP4": {
      "headline": "Connections that fit your setup\n\nOR\n\nFlexible ways to get printing",
      "long_message_best_sku": "Connect the way your devices work. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "long_message_safe_to_inherit": "Connect the way your devices work. This HP Smart Tank all-in-one supports dual-band Wi-Fi and Ethernet, giving everyday setups flexible paths for printing from nearby devices or a shared network. It helps reduce connection friction when print needs move between phones, laptops, and desks.",
      "mid_length": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "mid_length_safe_to_inherit": "Connect the way your devices work. Dual-band Wi-Fi and Ethernet give everyday setups flexible paths for nearby devices and shared networks.",
      "short_message": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "short_message_safe_to_inherit": "Dual-band Wi-Fi and Ethernet provide flexible paths for devices and shared networks.",
      "ultra_short": "Flexible connections",
      "ultra_short_safe_to_inherit": "Flexible connections"
    },
    "ValueProposition": {
      "headline": "Print more with fewer interruptions",
      "long_message_best_sku": "Keep recurring print, scan, copy, and fax work moving with a high-capacity all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. HP Smart Tank 7602 All-in-One pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, a 35-page auto document feeder, fax, and a 3-inch touchscreen, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "long_message_safe_to_inherit": "Keep recurring print, scan, copy, and fax work moving with a high-capacity HP Smart Tank all-in-one that reduces refill interruptions, handles everyday document tasks, and gives multiple users practical ways to connect, so recurring jobs are easier to plan and less dependent on last-minute supply checks. It pairs included Original HP Ink with a refillable tank design, automatic two-sided printing, an auto document feeder, fax, and touchscreen control, so paperwork, forms, records, and color documents are easier to manage from one device for regular document queues, household administration, and everyday business paperwork. Dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, HP app support, Apple AirPrint, and HP Print Service Plugin help phones, laptops, and shared networks print with less setup friction, while Original HP quality supports sharp everyday output for frequent use.",
      "mid_length": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "mid_length_safe_to_inherit": "Print more confidently with included Original HP Ink, automatic two-sided printing, ADF document handling, and flexible mobile, wireless, wired, and USB connections.",
      "short_message": "Included ink, workflow tools, and flexible connections keep recurring printing moving.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0d2b454316ccbd87006aa461cfe69c81978dbfd3b1d9a87744",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Unregistered_Product",
  "camera_tag": "Printer_Back_CloseUp"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The camera tag is registered and resolved exactly. The product name is unregistered, so the registered camera base was used conservatively without product overrides. The source messaging contains recurring paperwork, forms, records, and desk-administration cues, but the tight level view permits no visible props or background details.",
  "count_explanation": "Four numbered KSPs were present. Several cues overlap around recurring document and admin work, and the tight view cannot support separate visible paperwork scenarios, so one concise Office prompt was returned.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "recurring document and color jobs"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The cue supports an everyday work context, but visible pages or supplies were omitted because the resolved tight level view allows no props."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, records, handouts, and color materials"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The paperwork cue supports an office administration environment. Specific forms, records, and handouts were not shown because props are not permitted for this view."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "everyday admin work easier to complete at the desk"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "This directly supports the office desk surface in the prompt. Multi-page handling details were simplified away to keep the tight view clear."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "nearby devices or a shared network"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "phones, laptops, and desks"
        }
      ],
      "prompt_ids": [],
      "explanation": "The shared setup cue is useful context, but extra devices and network indicators would introduce additional hardware or props, so they were omitted."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "regular document queues, household administration, and everyday business paperwork"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The value proposition reinforces an everyday paperwork context. The prompt uses only the local office surface because the selected view is tight."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wood surface was added as a plausible office material.",
        "Soft daylight and a neutral backdrop were added to create a believable local setting without adding props."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "visible forms, records, handouts, and color materials",
          "nearby phones, laptops, shared-network indicators, and other devices",
          "multi-page task activity or hands"
        ],
        "explanation": "The effective profile is a tight level view with zero local props, zero background details, and no people. The retained office desk surface and soft light preserve the strongest desk-administration cue without requiring extra visible space."
      }
    ],
    "requested_product": "Unregistered_Product",
    "resolved_product": null,
    "product_resolution": "unknown"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "72d20430cd5e0fe53cc3690d9673c2cb7b3e3a6db52ed7d29c1c35ebf3f5e2f6",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "0098afc83adef191a75fc51fcf114aa2791de2fcca5f7f9eab0a12288fc97da7",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "input_raw_sha256": "3ab6114f20d62e1f85515e882cf1768919472470a56bdf8d3b8056857b4e1886",
  "recorded_input_semantic_sha256": "751484e7da07a89980b5ca5311e801e5818634e87b8b0568eb6fbf72e07f21f3",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvwycWZjNCldoF6MsOcDewd4t6jK",
  "usage": {
    "completion_tokens": 1836,
    "prompt_tokens": 13016,
    "total_tokens": 14852,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 12544,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 387,
      "engine_ttlt_ms": 18872,
      "pre_inference_ms": 315,
      "service_tbt_ms": 10,
      "service_ttft_ms": 1338,
      "service_ttlt_ms": 19641,
      "user_visible_ttft_ms": 1023
    }
  },
  "attempt": 1,
  "latency_seconds": 20.531,
  "started_at": "2026-10-22T22:53:23.797468+00:00",
  "completed_at": "2026-10-22T22:53:44.329176+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "16_unknown_product_known_printer_camera",
  "source_id": "ee810cf51bb82bb4",
  "product_name": "Unregistered_Product",
  "camera_tag": "Printer_Back_CloseUp",
  "purpose": "Unknown product with a known camera must use the conservative camera base.",
  "input_path": "inputs/16_unknown_product_known_printer_camera.json",
  "input_raw_sha256": "3ab6114f20d62e1f85515e882cf1768919472470a56bdf8d3b8056857b4e1886",
  "input_semantic_sha256": "751484e7da07a89980b5ca5311e801e5818634e87b8b0568eb6fbf72e07f21f3",
  "source_kind": "actual",
  "source_semantic_sha256": "ee810cf51bb82bb4ef2eb98d5c2c99b442822692029d25d7977e2c53d32d6a25",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/ee810cf51bb82bb4.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK1048202654963318374.zip",
      "member": "Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - d2bde90b-5fb6-4e04-b75a-b07d1e579cce.json",
      "member": null,
      "sha256": "6aa2a350d6b3b5a687b55c99c044a4163310104b55df379bf9bb4c838363a8b4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Unregistered_Product",
    "resolved_product": null,
    "product_resolution": "unknown"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "16_unknown_product_known_printer_camera",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/16_unknown_product_known_printer_camera.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 18,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Unregistered_Product",
    "resolved_product": null,
    "product_resolution": "unknown"
  },
  "actual_camera": {
    "requested_tag": "Printer_Back_CloseUp",
    "resolved_tag": "Printer_Back_CloseUp",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "tight",
    "elevation": "level",
    "requested_product": "Unregistered_Product",
    "resolved_product": null,
    "product_resolution": "unknown"
  }
}
```

</details>

## 17_actual_laptop_cashmere_front_right_medium

Previously uncovered actual convertible-laptop source under a medium oblique view.

- Requested product: `Cashmere`
- Requested camera: `Laptop_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A creative office tabletop in lightly grained wood, with a cropped sketch sheet and a single felt-tip pen. Soft daylight and a muted meeting-room wall keep the setting focused.

**p2 · Office**

A clean conference table surface with a meeting agenda and a ceramic cup, lit by diffuse daylight. A softly blurred chair in the background suggests a quiet call-ready workspace.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Front_Right_Medium",
  "resolved_tag": "Laptop_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Cashmere",
  "resolved_product": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop_Front_Right_Medium.png`

SHA-256: `e6c2b22b3abdb4757d0669bd3ad9baed74d65a00e5d4788dcc288557ab15d854`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 50826,
    "sha256": "e6c2b22b3abdb4757d0669bd3ad9baed74d65a00e5d4788dcc288557ab15d854",
    "zip_crc32": "79c155c6"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop/camera_laptop.locator_Cashmere-ElitebookX-14_Atmospheric-Blue.laptop_Front_Right_Medium.png",
    "bytes": 50826,
    "sha256": "e6c2b22b3abdb4757d0669bd3ad9baed74d65a00e5d4788dcc288557ab15d854",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Move freely across every work mode\n\nOR\n\nOne device for every work mode",
      "long_message_best_sku": "Keep ideas moving from first thought to shared direction. The HP EliteBook X Flip G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition gives you a 14-inch 2-in-1 convertible design with touch input, so you can sketch in tablet mode, present in tent mode, and collaborate in PC mode without changing devices. Work the way the moment calls for it, with one PC built to adapt.",
      "long_message_safe_to_inherit": "Keep ideas moving from first thought to shared direction. This HP EliteBook 14-inch 2-in-1 convertible design with touch input lets you sketch in tablet mode, present in tent mode, and collaborate in PC mode without changing devices. Work the way the moment calls for it, with one PC built to adapt.",
      "mid_length": "Keep ideas moving across modes with a 14-inch 2-in-1 convertible design, touch input, and tablet, tent, and PC modes.",
      "mid_length_safe_to_inherit": "Keep ideas moving across modes with a 14-inch 2-in-1 convertible design, touch input, and tablet, tent, and PC modes.",
      "short_message": "Move from sketching to presenting to collaboration with a flexible 14-inch 2-in-1 PC.",
      "short_message_safe_to_inherit": "Move from sketching to presenting to collaboration with a flexible 14-inch 2-in-1 PC.",
      "ultra_short": "Flexible work modes",
      "ultra_short_safe_to_inherit": "Flexible work modes"
    },
    "KSP2": {
      "headline": "AI support for modern work\n\nOR\n\nWorkflows ready for the AI era",
      "long_message_best_sku": "Support new ways of working without adding friction. The HP EliteBook X Flip G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition features an Intel® Core™ Ultra processor[2] with three compute engines that manage AI workloads, help improve video conferencing, and allow advanced content creation. Windows 11 and Microsoft Copilot experiences[1] help with summarizing, rewriting, recommendations, and organization, so work can move from input to action with less manual effort.",
      "long_message_safe_to_inherit": "Support new ways of working without adding friction. This HP EliteBook features AI-enabled processing that helps manage AI workloads, improve video conferencing, and support advanced content creation. Windows 11 and Microsoft Copilot experiences[1] help with summarizing, rewriting, recommendations, and organization, so work can move from input to action with less manual effort.",
      "mid_length": "Support AI-enhanced work with Intel® Core™ Ultra processing[2], three compute engines, and Windows 11 with Microsoft Copilot experiences[1].",
      "mid_length_safe_to_inherit": "Support AI-enhanced work with AI-enabled processing, compute resources for modern workloads, and Windows 11 with Microsoft Copilot experiences[1].",
      "short_message": "Support AI-enhanced work with Intel® Core™ Ultra processing[2] and Copilot experiences[1].",
      "short_message_safe_to_inherit": "Support AI-enhanced work with capable processing and Microsoft Copilot experiences[1].",
      "ultra_short": "AI-enhanced work",
      "ultra_short_safe_to_inherit": "AI-enhanced work"
    },
    "KSP3": {
      "headline": "Show up clearly in meetings\n\nOR\n\nBe seen and heard clearly",
      "long_message_best_sku": "Bring a clearer presence to every call. The HP EliteBook X Flip G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition uses Poly Camera Pro[5] with smart background adjustments and spotlight to help keep you framed and distraction-free. Dynamic Voice Leveling[8] optimizes microphone gain for voice clarity within 3 meters, while AI Noise Reduction[8] enhances audio conferencing, including while wearing a mask.",
      "long_message_safe_to_inherit": "Bring a clearer presence to every call. This HP EliteBook uses Poly Camera Pro[5] with smart background adjustments and spotlight to help keep you framed and distraction-free. Dynamic Voice Leveling[8] optimizes microphone gain for voice clarity within 3 meters, while AI Noise Reduction[8] enhances audio conferencing, including while wearing a mask.",
      "mid_length": "Bring a clearer meeting presence with Poly Camera Pro[5], smart background adjustments, Dynamic Voice Leveling[8], and AI Noise Reduction[8].",
      "mid_length_safe_to_inherit": "Bring a clearer meeting presence with Poly Camera Pro[5], smart background adjustments, Dynamic Voice Leveling[8], and AI Noise Reduction[8].",
      "short_message": "Be seen and heard clearly with Poly Camera Pro[5] and AI Noise Reduction[8].",
      "short_message_safe_to_inherit": "Be seen and heard clearly with Poly Camera Pro[5] and AI Noise Reduction[8].",
      "ultra_short": "Clear meeting presence",
      "ultra_short_safe_to_inherit": "Clear meeting presence"
    },
    "KSP4": {
      "headline": "Security for mobile AI work\n\nOR\n\nProtection built below the surface",
      "long_message_best_sku": "Work across locations with protection built into the PC experience. HP Wolf Security for Business[6] helps create a hardware-enforced, always-on, resilient defense from BIOS to browser and above, in, and below the OS. It gives business and IT teams added confidence as AI-enhanced work moves with the user.",
      "long_message_safe_to_inherit": "Work across locations with protection built into the PC experience. HP Wolf Security for Business[6] helps create a hardware-enforced, always-on, resilient defense from BIOS to browser and above, in, and below the OS. It gives business and IT teams added confidence as AI-enhanced work moves with the user.",
      "mid_length": "Work across locations with HP Wolf Security for Business[6], providing hardware-enforced, always-on, resilient defense from BIOS to browser.",
      "mid_length_safe_to_inherit": "Work across locations with HP Wolf Security for Business[6], providing hardware-enforced, always-on, resilient defense from BIOS to browser.",
      "short_message": "HP Wolf Security for Business[6] helps protect mobile AI-enhanced work across layers.",
      "short_message_safe_to_inherit": "HP Wolf Security for Business[6] helps protect mobile AI-enhanced work across layers.",
      "ultra_short": "Protected mobile work",
      "ultra_short_safe_to_inherit": "Protected mobile work"
    },
    "ValueProposition": {
      "headline": "Turn ideas into action in every mode",
      "long_message_best_sku": "Move from concept to presentation with one secure PC built for the way work shifts. The HP EliteBook X Flip G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition combines a 14-inch 2-in-1 convertible design with touch input, so you can sketch in tablet mode, present in tent mode, and collaborate in PC mode. Intel® Core™ Ultra processing[2] with three compute engines supports AI workloads, video conferencing, and advanced content creation, while Windows 11 and Microsoft Copilot experiences[1] help with summarizing, rewriting, recommendations, and organization. Poly Camera Pro[5], Dynamic Voice Leveling[8], and AI Noise Reduction[8] help you show up clearly in meetings, while HP Wolf Security for Business[6] helps create a hardware-enforced, always-on, resilient defense from BIOS to browser and above, in, and below the OS.",
      "long_message_safe_to_inherit": "Move from concept to presentation with one secure PC built for the way work shifts. This HP EliteBook combines a 14-inch 2-in-1 convertible design with touch input, so you can sketch in tablet mode, present in tent mode, and collaborate in PC mode. AI-enabled processing supports AI workloads, video conferencing, and advanced content creation, while Windows 11 and Microsoft Copilot experiences[1] help with summarizing, rewriting, recommendations, and organization. Poly Camera Pro[5], Dynamic Voice Leveling[8], and AI Noise Reduction[8] help you show up clearly in meetings, while HP Wolf Security for Business[6] helps create a hardware-enforced, always-on, resilient defense from BIOS to browser and above, in, and below the OS.",
      "mid_length": "Turn ideas into action across modes with 2-in-1 flexibility, AI-enhanced support, clearer collaboration, and HP Wolf Security for Business[6].",
      "mid_length_safe_to_inherit": "Turn ideas into action across modes with 2-in-1 flexibility, AI-enhanced support, clearer collaboration, and HP Wolf Security for Business[6].",
      "short_message": "Turn ideas into action with flexible modes, AI support, collaboration tools, and built-in protection.",
      "ultra_short": "Work across modes"
    },
    "_chatSession": {
      "responseId": "resp_00de8dbd4d6d78f7006aa34f65d1e481978a510d3a60ed71c6",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Cashmere",
  "camera_tag": "Laptop_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging contains four numbered KSPs and a ValueProposition. Usable scene cues include sketching, presenting, collaboration, video conferencing, meetings, organization, and mobile work across locations; technical processor, AI, and security claims were treated as context rather than visual requirements.",
  "count_explanation": "Four KSPs contain at least some usable activity or setting cue, but the medium oblique view supports only a local setting with at most two nearby props and one background detail. Two prompts were returned because the strongest distinct cues are creative sketch-to-collaboration work and meeting/call preparation; overlapping AI workflow and security language was simplified into ordinary office context.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "sketch in tablet mode, present in tent mode, and collaborate in PC mode"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The sketching and collaboration cue supports the cropped sketch sheet and pen on a local creative office surface. Device modes and hardware references were omitted from the prompt text."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "video conferencing, and allow advanced content creation"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "summarizing, rewriting, recommendations, and organization"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "The video conferencing and organization cues support a meeting agenda on a conference table. Processor, AI workload, operating system, and assistant references were omitted because they are not environment details."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "Bring a clearer presence to every call."
        },
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "audio conferencing"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "The call and conferencing cues support the meeting-ready office surface and subdued chair detail. Camera, microphone, background adjustment, and noise-reduction claims were not visualized."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Work across locations with protection built into the PC experience."
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "The mobile work cue supports flexible professional office settings, but the security architecture claims do not translate into visible props and were omitted."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "Move from concept to presentation with one secure PC built for the way work shifts."
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "sketch in tablet mode, present in tent mode, and collaborate in PC mode"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2"
    ],
    "explanation": "The value proposition reinforced the concept-to-presentation and collaboration context, which was simplified into local office tabletop scenes without naming or depicting device behavior."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Lightly grained wood surface, felt-tip pen, soft daylight, and muted meeting-room wall are ordinary invented details used to ground the sketching and collaboration cue within the view limits."
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Ceramic cup, diffuse daylight, and softly blurred chair are plausible invented office details added to support the meeting and organization cues without exceeding the prop and background limits."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "tablet, tent, and PC modes",
          "full presentation setup",
          "people collaborating",
          "extra office supplies"
        ],
        "explanation": "The resolved medium oblique preset allows a local surface, up to two props, and one background detail. The sketching cue was retained through a cropped sketch sheet and pen while broader collaboration and presentation activity was kept implied."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "visible conferencing hardware",
          "full meeting participants",
          "AI workflow details",
          "security claims"
        ],
        "explanation": "The resolved view supports a modest local meeting context but not a busy conference scene. The meeting agenda, cup, and single blurred chair retain the call and organization cues within the prop and background ceilings."
      }
    ],
    "requested_product": "Cashmere",
    "resolved_product": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "525a2023b91ba4e6a1545710ed7f8762b7310f5bfcccb604d681a924bb5061ba",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "a6750b3f3034a80926c0519f4651865f3c48c5544bb63e1a742aeb17f08ca9e1",
  "source_semantic_sha256": "d60e13e4457fd44cf5b7f89a6e754211bfe13d5dcd4c368f30d484ab85c65812",
  "input_raw_sha256": "5c1d50f3fc1afe9d7fed7e1e1fe81595ee7a72db242895ec888dca9c393f8d5c",
  "recorded_input_semantic_sha256": "60454fb0f7273f3b23b84ce25bcd343242526055131e2164746857d013e90a13",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvyE7Anh1h6xRIhLpplp3h6hAzrZ",
  "usage": {
    "completion_tokens": 2672,
    "prompt_tokens": 13208,
    "total_tokens": 15880,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1536,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 326,
      "engine_ttlt_ms": 26437,
      "pre_inference_ms": 155,
      "service_tbt_ms": 10,
      "service_ttft_ms": 1123,
      "service_ttlt_ms": 27215,
      "user_visible_ttft_ms": 968
    }
  },
  "attempt": 1,
  "latency_seconds": 28.21,
  "started_at": "2026-10-22T22:54:41.599064+00:00",
  "completed_at": "2026-10-22T22:55:09.809700+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "17_actual_laptop_cashmere_front_right_medium",
  "source_id": "d60e13e4457fd44c",
  "product_name": "Cashmere",
  "camera_tag": "Laptop_Front_Right_Medium",
  "purpose": "Previously uncovered actual convertible-laptop source under a medium oblique view.",
  "input_path": "inputs/17_actual_laptop_cashmere_front_right_medium.json",
  "input_raw_sha256": "5c1d50f3fc1afe9d7fed7e1e1fe81595ee7a72db242895ec888dca9c393f8d5c",
  "input_semantic_sha256": "60454fb0f7273f3b23b84ce25bcd343242526055131e2164746857d013e90a13",
  "source_kind": "actual",
  "source_semantic_sha256": "d60e13e4457fd44cf5b7f89a6e754211bfe13d5dcd4c368f30d484ab85c65812",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/d60e13e4457fd44c.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2703900895627379394.zip",
      "member": "Source Messaging - 8e56189b-2c04-4066-bd8c-08fb6359588d.json",
      "sha256": "a61986ad16478088e9290cb1ebb44520e91e206c45b6b5e2cc11f12b3a354ca6"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 8e56189b-2c04-4066-bd8c-08fb6359588d.json",
      "member": null,
      "sha256": "a61986ad16478088e9290cb1ebb44520e91e206c45b6b5e2cc11f12b3a354ca6"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Cashmere",
    "resolved_product": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "17_actual_laptop_cashmere_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/17_actual_laptop_cashmere_front_right_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 29,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 29,
      "environment": "Office"
    }
  ],
  "prompt_count": 2,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Cashmere",
    "resolved_product": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Cashmere",
    "resolved_product": "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 18_actual_laptop_cheddar_front_right_medium

Previously uncovered actual mobile-work laptop source under a medium oblique view.

- Requested product: `Cheddar`
- Requested camera: `Laptop_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A collaborative worktable in light wood with a paper sketch sheet and a single pen, lit by soft daylight. A blurred meeting chair suggests a shared workspace nearby.

**p2 · Office**

A tidy meeting table with a printed agenda and ceramic cup in gentle daylight. A softly defined conference chair adds context without crowding the local surface.

### Exact resolved profile limits

```json
{
  "requested_tag": "Laptop_Front_Right_Medium",
  "resolved_tag": "Laptop_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Cheddar",
  "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "laptop",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Medium.png`

SHA-256: `e09529cd40f579a8b7de594a24ead9d9c6977cd9b08f711766e6ae1208846bfa`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_laptop.locator_Cheddar-13_NaturalSilver.laptop",
    "device_family": "laptop",
    "device_asset_name_from_folder": "Cheddar-13_NaturalSilver.laptop.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 76538,
    "sha256": "e09529cd40f579a8b7de594a24ead9d9c6977cd9b08f711766e6ae1208846bfa",
    "zip_crc32": "878abe8e"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop/camera_laptop.locator_Cheddar-13_NaturalSilver.laptop_Front_Right_Medium.png",
    "bytes": 76538,
    "sha256": "e09529cd40f579a8b7de594a24ead9d9c6977cd9b08f711766e6ae1208846bfa",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Flex across every work mode\n\nOR\n\nFrom sketch to presentation",
      "long_message_best_sku": "Move from idea to presentation without losing momentum. The 14-inch 2-in-1 convertible design with touch input supports sketching in tablet mode, presenting in tent mode, and collaborating in PC mode, so your device adapts as the conversation changes. That flexibility helps keep thinking, sharing, and teamwork in one flow.",
      "long_message_safe_to_inherit": "Move from idea to presentation without losing momentum. The 14-inch 2-in-1 convertible design with touch input supports sketching in tablet mode, presenting in tent mode, and collaborating in PC mode, so your device adapts as the conversation changes. That flexibility helps keep thinking, sharing, and teamwork in one flow.",
      "mid_length": "Move from idea to presentation without losing momentum. Touch input and tablet, tent, and PC modes keep thinking and sharing in one flow.",
      "mid_length_safe_to_inherit": "Move from idea to presentation without losing momentum. Touch input and tablet, tent, and PC modes keep thinking and sharing in one flow.",
      "short_message": "Move from idea to presentation with touch-enabled tablet, tent, and PC modes.",
      "short_message_safe_to_inherit": "Move from idea to presentation with touch-enabled tablet, tent, and PC modes.",
      "ultra_short": "Flexible work modes",
      "ultra_short_safe_to_inherit": "Flexible work modes"
    },
    "KSP2": {
      "headline": "Built for emerging AI workflows\n\nOR\n\nAI support for what comes next",
      "long_message_best_sku": "Take on emerging workflows with more confidence. The latest Intel® Core™ Ultra processor [2] uses three compute engines to manage AI workloads [3], help improve video conferencing, and allow advanced content creation, giving mobile professionals a practical foundation for AI-powered work.",
      "long_message_safe_to_inherit": "Take on emerging workflows with more confidence. An Intel® Core™ Ultra processor [2] uses three compute engines to manage AI workloads [3], help improve video conferencing, and allow advanced content creation, giving mobile professionals a practical foundation for AI-powered work.",
      "mid_length": "Take on emerging workflows with more confidence. Intel® Core™ Ultra [2] uses three compute engines for AI workloads [3], conferencing, and content creation.",
      "mid_length_safe_to_inherit": "Take on emerging workflows with more confidence. Intel® Core™ Ultra [2] uses three compute engines for AI workloads [3], conferencing, and content creation.",
      "short_message": "Handle emerging workflows confidently with Intel® Core™ Ultra [2] and three compute engines.",
      "short_message_safe_to_inherit": "Handle emerging workflows confidently with Intel® Core™ Ultra [2] and three compute engines.",
      "ultra_short": "AI workflow foundation",
      "ultra_short_safe_to_inherit": "AI workflow foundation"
    },
    "KSP3": {
      "headline": "Look and sound prepared\n\nOR\n\nClearer presence in meetings",
      "long_message_best_sku": "Show up clearly and confidently in important conversations. Poly Camera Pro [5] keeps users framed and distraction-free with smart background adjustments and spotlight, while Dynamic Voice Leveling and AI Noise Reduction [8] help optimize voice clarity within 3 meters of the PC. Together, they help you focus on the meeting instead of the setup.",
      "long_message_safe_to_inherit": "Show up clearly and confidently in important conversations. Poly Camera Pro [5] keeps users framed and distraction-free with smart background adjustments and spotlight, while Dynamic Voice Leveling and AI Noise Reduction [8] help optimize voice clarity within 3 meters of the PC. Together, they help you focus on the meeting instead of the setup.",
      "mid_length": "Show up clearly and confidently in important conversations. Poly Camera Pro [5] and AI audio tools [8] help improve focus and voice clarity.",
      "mid_length_safe_to_inherit": "Show up clearly and confidently in important conversations. Poly Camera Pro [5] and AI audio tools [8] help improve focus and voice clarity.",
      "short_message": "Show up clearly in meetings with Poly Camera Pro [5] and AI audio tools [8].",
      "short_message_safe_to_inherit": "Show up clearly in meetings with Poly Camera Pro [5] and AI audio tools [8].",
      "ultra_short": "Clear meeting presence",
      "ultra_short_safe_to_inherit": "Clear meeting presence"
    },
    "KSP4": {
      "headline": "Protection built for mobile work\n\nOR\n\nSecurity from BIOS to browser",
      "long_message_best_sku": "Work across locations with protection that stays active. HP Wolf Security for Business [6] provides hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, helping protect mobile work from the device level.",
      "long_message_safe_to_inherit": "Work across locations with protection that stays active. HP Wolf Security for Business [6] provides hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, helping protect mobile work from the device level.",
      "mid_length": "Work across locations with protection that stays active. HP Wolf Security for Business [6] defends from BIOS to browser across OS layers.",
      "mid_length_safe_to_inherit": "Work across locations with protection that stays active. HP Wolf Security for Business [6] defends from BIOS to browser across OS layers.",
      "short_message": "Stay protected across locations with hardware-enforced HP Wolf Security for Business [6].",
      "short_message_safe_to_inherit": "Stay protected across locations with hardware-enforced HP Wolf Security for Business [6].",
      "ultra_short": "Built-in business protection",
      "ultra_short_safe_to_inherit": "Built-in business protection"
    },
    "ValueProposition": {
      "headline": "Executive precision in motion",
      "long_message_best_sku": "Move from idea to impact with a flexible business PC that supports the way work shifts through the day. The HP EliteBook X Flip G2i 14 inch Notebook Next Gen AI PC Wolf Pro Security Edition brings together a 14-inch 2-in-1 design with touch input for sketching in tablet mode, presenting in tent mode, and collaborating in PC mode, plus Next Gen AI PC support [3] with the latest Intel® Core™ Ultra processor [2] and Microsoft Copilot support [1] for summarizing, rewriting, recommendations, and organization. Poly Camera Pro [5], Dynamic Voice Leveling, and AI Noise Reduction [8] help you stay framed, distraction-free, and clear in meetings, while HP Wolf Security for Business [6] provides hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so mobile professionals can work flexibly, collaborate confidently, and stay protected across locations.",
      "long_message_safe_to_inherit": "Move from idea to impact with a flexible business PC that supports the way work shifts through the day. This 14-inch 2-in-1 Next Gen AI PC [3] brings together touch input for sketching in tablet mode, presenting in tent mode, and collaborating in PC mode, plus Intel® Core™ Ultra processor support [2] and Microsoft Copilot support [1] for summarizing, rewriting, recommendations, and organization. Poly Camera Pro [5], Dynamic Voice Leveling, and AI Noise Reduction [8] help you stay framed, distraction-free, and clear in meetings, while HP Wolf Security for Business [6] provides hardware-enforced, always-on, resilient defense from BIOS to browser, above, in, and below the OS, so mobile professionals can work flexibly, collaborate confidently, and stay protected across locations.",
      "mid_length": "Move from idea to impact with 2-in-1 flexibility, Intel® Core™ Ultra AI support [2], Poly collaboration tools [5], and HP Wolf Security [6].",
      "mid_length_safe_to_inherit": "Move from idea to impact with 2-in-1 flexibility, Intel® Core™ Ultra AI support [2], Poly collaboration tools [5], and HP Wolf Security [6].",
      "short_message": "Work flexibly with AI support [3], clearer collaboration, and HP Wolf Security [6].",
      "ultra_short": "Flexible secure AI work"
    },
    "_chatSession": {
      "responseId": "resp_0b3cb35f015fa8c3006aa3538be83c8193a8759780d2e4dc3e",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Cheddar",
  "camera_tag": "Laptop_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging provides concrete work cues around sketching, presenting, collaboration, meetings, conferencing, and work across locations. Technical AI, processor, security, and product-mode claims were treated as messaging context rather than visible scene requirements.",
  "count_explanation": "Four numbered KSPs are present. KSP1 and KSP3 provide the strongest distinct visual settings, while KSP2 overlaps with meeting/content work and KSP4 is mostly abstract security with a broad mobile-work cue. Two concise prompts cover the useful, compatible cues within the medium oblique view limits.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "supports sketching in tablet mode, presenting in tent mode, and collaborating in PC mode"
        },
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "thinking, sharing, and teamwork"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Sketching and collaboration were translated into a local worktable with a sketch sheet and pen. Product modes and device references were omitted from the scene prose."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "help improve video conferencing, and allow advanced content creation"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "mobile professionals"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "The conferencing and professional-work cues support a meeting-table environment. Processor, AI workload, and compute-engine claims were not rendered as visible scene elements."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "important conversations"
        },
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "focus on the meeting instead of the setup"
        }
      ],
      "prompt_ids": [
        "p2"
      ],
      "explanation": "Meeting presence became a tidy local meeting table with a printed agenda. User framing, background adjustment, and audio features were omitted because they describe product capability rather than environment."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Work across locations"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "mobile work"
        }
      ],
      "prompt_ids": [],
      "explanation": "The mobile-work cue is usable but not distinct enough to require another prompt. Security defenses from BIOS to browser were omitted because they are not visible lifestyle setting details."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "Move from idea to impact with a flexible business PC that supports the way work shifts through the day"
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "sketching in tablet mode, presenting in tent mode, and collaborating in PC mode"
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "stay framed, distraction-free, and clear in meetings"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2"
    ],
    "explanation": "The value proposition reinforced the office-work arc from ideation to collaboration and meetings. Product names, hardware features, AI support, and security claims were not included in scene prose."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Light wood surface",
        "Single pen",
        "Blurred meeting chair",
        "Soft daylight"
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Printed agenda",
        "Ceramic cup",
        "Softly defined conference chair",
        "Gentle daylight"
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession",
    "_chatSession.responseId",
    "_chatSession.model",
    "_chatSession.systemInstructions"
  ],
  "camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "Product modes",
          "Presentation setup",
          "Full teamwork scene",
          "Extra office furnishings"
        ],
        "explanation": "The medium oblique preset allows a local surface, at most two nearby props, and one subordinate background detail. The sketching and collaboration cues were retained as a sketch sheet, pen, and blurred chair."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "Visible conferencing equipment",
          "Full meeting participants",
          "AI audio and camera features",
          "Security messaging"
        ],
        "explanation": "The meeting cue was kept local with an agenda, cup, and one soft background chair. People and additional room details were avoided to preserve the selected medium framing."
      }
    ],
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "78be3e8934694d33e2a6882f12e37631ce9eb284b78d26e065e994e3500e1a66",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "a6750b3f3034a80926c0519f4651865f3c48c5544bb63e1a742aeb17f08ca9e1",
  "source_semantic_sha256": "fecec52a5c57c7bb45dedfc39771fa53a1af96e1abdde37fa8a1bb3420af2fb4",
  "input_raw_sha256": "86ba92602d75078017c8c872fca4b93d90301f6e5d5d46624c1e5f4e371093f3",
  "recorded_input_semantic_sha256": "894549da15db55e8bbfc829ed2a489a67d4c5f1cc4abb289136b3d29a42fe0fb",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvygQO9RWxetv0yJSgO8EcR4j0ek",
  "usage": {
    "completion_tokens": 1619,
    "prompt_tokens": 13077,
    "total_tokens": 14696,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 512,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 402,
      "engine_ttlt_ms": 14301,
      "pre_inference_ms": 204,
      "service_tbt_ms": 9,
      "service_ttft_ms": 1036,
      "service_ttlt_ms": 14928,
      "user_visible_ttft_ms": 832
    }
  },
  "attempt": 1,
  "latency_seconds": 15.929,
  "started_at": "2026-10-22T22:55:09.835034+00:00",
  "completed_at": "2026-10-22T22:55:25.764647+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "18_actual_laptop_cheddar_front_right_medium",
  "source_id": "fecec52a5c57c7bb",
  "product_name": "Cheddar",
  "camera_tag": "Laptop_Front_Right_Medium",
  "purpose": "Previously uncovered actual mobile-work laptop source under a medium oblique view.",
  "input_path": "inputs/18_actual_laptop_cheddar_front_right_medium.json",
  "input_raw_sha256": "86ba92602d75078017c8c872fca4b93d90301f6e5d5d46624c1e5f4e371093f3",
  "input_semantic_sha256": "894549da15db55e8bbfc829ed2a489a67d4c5f1cc4abb289136b3d29a42fe0fb",
  "source_kind": "actual",
  "source_semantic_sha256": "fecec52a5c57c7bb45dedfc39771fa53a1af96e1abdde37fa8a1bb3420af2fb4",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/fecec52a5c57c7bb.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK2745132682490047977.zip",
      "member": "Source Messaging - 44b611c4-b58f-4614-a9e0-81a3d669f1d3.json",
      "sha256": "fd5ba38ec95e50344ac856198f7dccdb6ce43a6f946c5fcd8b3ae9bb2a32ccaa"
    }
  ],
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "18_actual_laptop_cheddar_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/18_actual_laptop_cheddar_front_right_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 28,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 26,
      "environment": "Office"
    }
  ],
  "prompt_count": 2,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Laptop_Front_Right_Medium",
    "resolved_tag": "Laptop_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Cheddar",
    "resolved_product": "Cheddar-13_NaturalSilver.laptop.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 19_actual_printer_magic_front_right_medium

Previously uncovered actual ink-tank printer source under a medium oblique view.

- Requested product: `Magic`
- Requested camera: `Printer_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A clean office work surface in pale wood with a compact stack of forms and a single pen. A softly blurred filing tray suggests routine admin work in daylight.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Front_Right_Medium",
  "resolved_tag": "Printer_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png`

SHA-256: `66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 79199,
    "sha256": "66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda",
    "zip_crc32": "6993477e"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "bytes": 79199,
    "sha256": "66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Print longer between refills\n\nOR\n\nStart with more ink confidence",
      "long_message_best_sku": "Print more with less supply friction. HP Smart Tank 7602 All-in-One uses a high-capacity refillable ink tank system and includes Original HP Ink in the box, helping reduce early refill decisions for frequent document and color printing. That gives recurring print needs a more predictable start without sacrificing all-in-one convenience.",
      "long_message_safe_to_inherit": "Print more with less supply friction. This HP Smart Tank all-in-one uses a high-capacity refillable ink tank system and includes Original HP Ink in the box, helping reduce early refill decisions for frequent document and color printing. That gives recurring print needs a more predictable start without sacrificing all-in-one convenience.",
      "mid_length": "Print more with less supply friction, thanks to a high-capacity refillable ink tank system and Original HP Ink included in the box.",
      "mid_length_safe_to_inherit": "Print more with less supply friction, thanks to a high-capacity refillable ink tank system and Original HP Ink included in the box.",
      "short_message": "Print more with less refill friction using included Original HP Ink and refillable tanks.",
      "short_message_safe_to_inherit": "Print more with less refill friction using included Original HP Ink and refillable tanks.",
      "ultra_short": "More ink confidence",
      "ultra_short_safe_to_inherit": "More ink confidence"
    },
    "KSP2": {
      "headline": "Handle multi-page work smoothly\n\nOR\n\nBuilt for document flow",
      "long_message_best_sku": "Keep everyday document work moving. HP Smart Tank 7602 All-in-One brings print, copy, scan, fax, ADF, and wireless functions together with automatic two-sided printing and a 35-page auto document feeder. Multi-page forms, records, packets, and copies take fewer manual steps, so recurring admin work feels easier to manage.",
      "long_message_safe_to_inherit": "Keep everyday document work moving. This HP Smart Tank all-in-one brings print, copy, scan, fax, ADF, and wireless functions together with automatic two-sided printing and an auto document feeder. Multi-page forms, records, packets, and copies take fewer manual steps, so recurring admin work feels easier to manage.",
      "mid_length": "Keep everyday document work moving with print, copy, scan, fax, automatic two-sided printing, and a 35-page auto document feeder.",
      "mid_length_safe_to_inherit": "Keep everyday document work moving with print, copy, scan, fax, automatic two-sided printing, and an auto document feeder.",
      "short_message": "Handle multi-page workflows with all-in-one functions, automatic duplex, and a 35-page ADF.",
      "short_message_safe_to_inherit": "Handle multi-page workflows with all-in-one functions, automatic duplex, and an ADF.",
      "ultra_short": "Document flow simplified",
      "ultra_short_safe_to_inherit": "Document flow simplified"
    },
    "KSP3": {
      "headline": "Connect the way you work\n\nOR\n\nFlexible printing access",
      "long_message_best_sku": "Print from the devices and connections that fit your space. HP Smart Tank 7602 All-in-One supports dual-band Wi-Fi, Wi-Fi Direct, Ethernet, Hi-Speed USB 2.0, the HP app, Apple AirPrint, and HP Print Service Plugin for Android. That flexibility helps phones, computers, wired networks, and direct wireless connections share one dependable print hub.",
      "long_message_safe_to_inherit": "Print from the devices and connections that fit your space. This HP Smart Tank all-in-one supports wireless, direct wireless, wired network, USB, mobile app, Apple AirPrint, and Android printing connections. That flexibility helps phones, computers, wired networks, and direct wireless connections share one dependable print hub.",
      "mid_length": "Print from phones, computers, wired networks, or direct wireless connections with dual-band Wi-Fi, Wi-Fi Direct, Ethernet, and mobile print support.",
      "mid_length_safe_to_inherit": "Print from phones, computers, wired networks, or direct wireless connections with wireless, direct wireless, wired network, and mobile print support.",
      "short_message": "Connect through wireless, direct wireless, Ethernet, USB, and mobile print options.",
      "short_message_safe_to_inherit": "Connect through wireless, direct wireless, wired network, USB, and mobile print options.",
      "ultra_short": "Flexible print access",
      "ultra_short_safe_to_inherit": "Flexible print access"
    },
    "KSP4": {
      "headline": "Control feels simple\n\nOR\n\nA smarter tank experience",
      "long_message_best_sku": "Manage printing with less guesswork. HP Smart Tank 7602 All-in-One includes a 3-inch touchscreen mono graphics display, guided mobile setup, and customizable shortcuts on your phone through the HP app. Everyday setup, scanning, and repeat tasks feel more direct from the device or your mobile screen.",
      "long_message_safe_to_inherit": "Manage printing with less guesswork. This HP Smart Tank all-in-one includes an intuitive display, guided mobile setup, and customizable shortcuts on your phone through the HP app. Everyday setup, scanning, and repeat tasks feel more direct from the device or your mobile screen.",
      "mid_length": "Manage printing with less guesswork using a 3-inch touchscreen, guided mobile setup, and customizable phone shortcuts through the HP app.",
      "mid_length_safe_to_inherit": "Manage printing with less guesswork using an intuitive display, guided mobile setup, and customizable phone shortcuts through the HP app.",
      "short_message": "Use the touchscreen, guided setup, and phone shortcuts to simplify repeat tasks.",
      "short_message_safe_to_inherit": "Use the display, guided setup, and phone shortcuts to simplify repeat tasks.",
      "ultra_short": "Simple guided control",
      "ultra_short_safe_to_inherit": "Simple guided control"
    },
    "ValueProposition": {
      "headline": "High-capacity printing with everyday productivity",
      "long_message_best_sku": "Frequent printing should feel easier to plan, connect, and manage. HP Smart Tank 7602 All-in-One combines a high-capacity refillable ink tank system with Original HP Ink included in the box, giving recurring document and color output a more confident start. Print, copy, scan, and fax from one device, move through multi-page jobs with automatic two-sided printing and a 35-page auto document feeder, and connect through dual-band Wi-Fi, Wi-Fi Direct, Ethernet, USB, the HP app, Apple AirPrint, and Android printing support. A 3-inch touchscreen, guided mobile setup, and customizable phone shortcuts help make setup, scanning, and repeat tasks more direct, so everyday print workflows stay organized with fewer supply and process interruptions.",
      "long_message_safe_to_inherit": "Frequent printing should feel easier to plan, connect, and manage. This HP Smart Tank all-in-one combines a high-capacity refillable ink tank system with Original HP Ink included in the box, giving recurring document and color output a more confident start. Print, copy, scan, and fax from one device, move through multi-page jobs with automatic two-sided printing and an auto document feeder, and connect through wireless, direct wireless, wired network, USB, mobile app, Apple AirPrint, and Android printing support. An intuitive display, guided mobile setup, and customizable phone shortcuts help make setup, scanning, and repeat tasks more direct, so everyday print workflows stay organized with fewer supply and process interruptions.",
      "mid_length": "Print, scan, copy, and fax with high-capacity ink confidence, multi-page productivity, flexible connectivity, and simple guided control from one HP Smart Tank all-in-one.",
      "mid_length_safe_to_inherit": "Print, scan, copy, and fax with high-capacity ink confidence, multi-page productivity, flexible connectivity, and simple guided control from one HP Smart Tank all-in-one.",
      "short_message": "High-capacity ink, all-in-one productivity, flexible connectivity, and guided control simplify frequent printing.",
      "ultra_short": "Print more confidently"
    },
    "_chatSession": {
      "responseId": "resp_0227ad8c836de25b006aa461cfdcdc8196b37269d742b509cc",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging is mostly product-feature copy, with usable setting cues around frequent document output, multi-page forms, copies, and recurring admin work. The selected view supports a local office surface with a few modest nearby details.",
  "count_explanation": "Four numbered KSPs are present. KSP1, KSP2, and KSP4 contain useful activity cues, but they overlap around recurring document workflows, so one combined Office prompt is the strongest compatible choice for the medium oblique view.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "frequent document and color printing"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Frequent document output supports an office work surface. Ink tank and refill claims were not visualized as props because they are product-specific and not suitable environment details."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "Multi-page forms, records, packets, and copies take fewer manual steps, so recurring admin work feels easier to manage."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "This is the main scene cue. It is represented with a compact stack of forms and a pen, plus one subtle filing-tray background detail."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": false,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "phones, computers, wired networks, and direct wireless connections share one dependable print hub"
        }
      ],
      "prompt_ids": [],
      "explanation": "Connectivity and device-sharing claims are useful product messaging but do not create a distinct environment cue. Extra phones, computers, cables, or network hardware were omitted to avoid product-dependent clutter."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Everyday setup, scanning, and repeat tasks feel more direct from the device or your mobile screen."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Repeat-task workflow overlaps with the admin-work setting. Product controls, mobile screens, and scanning interactions were simplified into routine office paperwork."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "everyday print workflows stay organized with fewer supply and process interruptions."
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "The value proposition reinforces organized everyday workflows, which informed the tidy office surface and restrained document-management details."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Pale wooden work surface chosen as a plausible neutral office material not specified in the source.",
        "Single pen added as an ordinary document-work prop within the medium-view limit.",
        "Softly blurred filing tray added as one subordinate background detail to suggest recurring admin organization."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "High-capacity ink and refill details",
          "Named product functions and touchscreen details",
          "Phones, computers, cables, and network hardware",
          "People and hand interactions",
          "Multiple document categories beyond one compact forms stack"
        ],
        "explanation": "The medium oblique printer preset allows a local setting with at most two nearby props and one background detail. The prompt retains the strongest source-supported document and admin workflow cue while keeping the surrounding surface clear and avoiding product-specific interactions."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "0fb3d99fe5e3b03e6a727bbcbba0d9f9f454835ad5c879adfa4579d2e6d78ded",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "a6750b3f3034a80926c0519f4651865f3c48c5544bb63e1a742aeb17f08ca9e1",
  "source_semantic_sha256": "8bbf8af1d8cbf4b2d70c755d9cec9030e658408f2076733d8407fbf710863935",
  "input_raw_sha256": "749067a68237d200747fd6c07e49d859bcb4660a7cc3d7976a80cd4737226d76",
  "recorded_input_semantic_sha256": "f3ff9ef6779f3f196e0d339c1cbcc1690b9af628a986ed1b5ecb3d2b0fc69c04",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvywAeIXyiZTTfkWneazXO6DfHCc",
  "usage": {
    "completion_tokens": 1922,
    "prompt_tokens": 13008,
    "total_tokens": 14930,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 403,
      "engine_ttlt_ms": 19096,
      "pre_inference_ms": 442,
      "service_tbt_ms": 10,
      "service_ttft_ms": 1244,
      "service_ttlt_ms": 19906,
      "user_visible_ttft_ms": 802
    }
  },
  "attempt": 1,
  "latency_seconds": 21.133,
  "started_at": "2026-10-22T22:55:25.789528+00:00",
  "completed_at": "2026-10-22T22:55:46.922749+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "19_actual_printer_magic_front_right_medium",
  "source_id": "8bbf8af1d8cbf4b2",
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Medium",
  "purpose": "Previously uncovered actual ink-tank printer source under a medium oblique view.",
  "input_path": "inputs/19_actual_printer_magic_front_right_medium.json",
  "input_raw_sha256": "749067a68237d200747fd6c07e49d859bcb4660a7cc3d7976a80cd4737226d76",
  "input_semantic_sha256": "f3ff9ef6779f3f196e0d339c1cbcc1690b9af628a986ed1b5ecb3d2b0fc69c04",
  "source_kind": "actual",
  "source_semantic_sha256": "8bbf8af1d8cbf4b2d70c755d9cec9030e658408f2076733d8407fbf710863935",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/8bbf8af1d8cbf4b2.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK4748855972432039582.zip",
      "member": "Source Messaging - 8a8e84ff-69e1-4581-a1ca-8eb411354a2a.json",
      "sha256": "fe8d1dc26056d55824e19fce50385c446f6a307feed7d72c0cc85916d07bb688"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "19_actual_printer_magic_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/19_actual_printer_magic_front_right_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 29,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 3,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 20_actual_printer_messi_front_right_medium

Previously uncovered actual shared-space printer source under a medium oblique view.

- Requested product: `Messi`
- Requested camera: `Printer_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A shared office worktable in light wood with a compact stack of forms and a single pen, lit by soft daylight. A muted partition edge in the background suggests a busy document area without clutter.

**p2 · Education**

A school preparation surface in lightly worn wood with the cropped edge of a learning packet and a slim folder, lit by diffuse daylight. A softly blurred classroom noticeboard adds context.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Front_Right_Medium",
  "resolved_tag": "Printer_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Messi",
  "resolved_product": "Messi_Ceramic-White.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png`

SHA-256: `ac16182e6f9217ac2ca1e9de1ce6b7f99390c56d6c155b25e9a071bdf0ab49ca`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Messi_Ceramic-White.printer.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_printer.locator_Messi_Ceramic-White.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Messi_Ceramic-White.printer.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 26168,
    "sha256": "ac16182e6f9217ac2ca1e9de1ce6b7f99390c56d6c155b25e9a071bdf0ab49ca",
    "zip_crc32": "cdb07c0e"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png",
    "bytes": 26168,
    "sha256": "ac16182e6f9217ac2ca1e9de1ce6b7f99390c56d6c155b25e9a071bdf0ab49ca",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Print More Between Refills\n\nOR\n\nLong-Running Ink Confidence",
      "long_message_best_sku": "Keep printing longer with less refill planning. HP Smart Tank 7602 All-in-One includes Original HP Ink bottles in the box and uses a high-capacity ink tank design, helping frequent color and document work stay ready for invoices, forms, learning materials, records, and everyday admin needs.",
      "long_message_safe_to_inherit": "Keep printing longer with less refill planning. This HP Smart Tank all-in-one includes Original HP Ink bottles in the box and uses a high-capacity ink tank design, helping frequent color and document work stay ready for invoices, forms, learning materials, records, and everyday admin needs.",
      "mid_length": "Keep printing longer with less refill planning. Included Original HP Ink bottles and high-capacity tanks support frequent color and document work in shared spaces.",
      "mid_length_safe_to_inherit": "Keep printing longer with less refill planning. Included Original HP Ink bottles and high-capacity tanks support frequent color and document work in shared spaces.",
      "short_message": "Keep printing longer with included Original HP Ink bottles and high-capacity tanks.",
      "short_message_safe_to_inherit": "Keep printing longer with included Original HP Ink bottles and high-capacity tanks.",
      "ultra_short": "Longer print confidence",
      "ultra_short_safe_to_inherit": "Longer print confidence"
    },
    "KSP2": {
      "headline": "Multipage Work Made Easier\n\nOR\n\nDo More With Each Document",
      "long_message_best_sku": "Move multipage document work with fewer manual steps. HP Smart Tank 7602 All-in-One brings print, copy, scan, fax, a 35-page automatic document feeder, and automatic two-sided printing into one device, helping forms, reports, packets, and records move from page to task with less hand-feeding during busy days.",
      "long_message_safe_to_inherit": "Move multipage document work with fewer manual steps. This HP Smart Tank all-in-one brings print, copy, scan, fax, a 35-page automatic document feeder, and automatic two-sided printing into one device, helping forms, reports, packets, and records move from page to task with less hand-feeding during busy days.",
      "mid_length": "Move multipage document work with fewer manual steps. Print, copy, scan, fax, ADF, and automatic two-sided printing help tasks flow during busy days.",
      "mid_length_safe_to_inherit": "Move multipage document work with fewer manual steps. Print, copy, scan, fax, ADF, and automatic two-sided printing help tasks flow during busy days.",
      "short_message": "Print, copy, scan, fax, ADF, and automatic two-sided printing simplify multipage work.",
      "short_message_safe_to_inherit": "Print, copy, scan, fax, ADF, and automatic two-sided printing simplify multipage work.",
      "ultra_short": "Multipage tasks simplified",
      "ultra_short_safe_to_inherit": "Multipage tasks simplified"
    },
    "KSP3": {
      "headline": "Connect Your Way\n\nOR\n\nMore Ways To Print",
      "long_message_best_sku": "Stay connected through the ways your space already works. HP Smart Tank 7602 All-in-One supports built-in Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, the HP app, Apple AirPrint, and HP Print Service Plugin for Android, giving people in shared spaces practical ways to print from common devices without centering the workflow on one connection path.",
      "long_message_safe_to_inherit": "Stay connected through the ways your space already works. This HP Smart Tank all-in-one supports built-in Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, the HP app, Apple AirPrint, and HP Print Service Plugin for Android, giving people in shared spaces practical ways to print from common devices without centering the workflow on one connection path.",
      "mid_length": "Stay connected through the ways your space already works. Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, and mobile printing support common devices.",
      "mid_length_safe_to_inherit": "Stay connected through the ways your space already works. Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, and mobile printing support common devices.",
      "short_message": "Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, and mobile printing support common devices.",
      "short_message_safe_to_inherit": "Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, and mobile printing support common devices.",
      "ultra_short": "Flexible connection choices",
      "ultra_short_safe_to_inherit": "Flexible connection choices"
    },
    "KSP4": {
      "headline": "HP Quality Made Simple\n\nOR\n\nClear Output, Simple Control",
      "long_message_best_sku": "Make everyday pages easier to create and review. HP Smart Tank 7602 All-in-One supports HP-quality black and color output and includes a 3-inch touchscreen mono graphics display, helping documents and color materials move from setup to print with clear, simple control.",
      "long_message_safe_to_inherit": "Make everyday pages easier to create and review. This HP Smart Tank all-in-one supports HP-quality black and color output and includes a 3-inch touchscreen mono graphics display, helping documents and color materials move from setup to print with clear, simple control.",
      "mid_length": "Make everyday pages easier to create and review. HP-quality black and color output and a 3-inch touchscreen help simplify routine print tasks.",
      "mid_length_safe_to_inherit": "Make everyday pages easier to create and review. HP-quality black and color output and a 3-inch touchscreen help simplify routine print tasks.",
      "short_message": "HP-quality black and color output plus a 3-inch touchscreen simplify routine print tasks.",
      "short_message_safe_to_inherit": "HP-quality black and color output plus a 3-inch touchscreen simplify routine print tasks.",
      "ultra_short": "HP-quality output",
      "ultra_short_safe_to_inherit": "HP-quality output"
    },
    "ValueProposition": {
      "headline": "Print More, Manage Less",
      "long_message_best_sku": "Handle recurring document work with fewer ink interruptions, fewer manual steps, and connection choices that fit shared spaces. HP Smart Tank 7602 All-in-One combines a premium high-capacity ink tank design with included Original HP Ink bottles, print, copy, scan, fax, a 35-page automatic document feeder, and automatic two-sided printing, so everyday forms, packets, records, and color documents move through one capable device. Built-in Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, the HP app, Apple AirPrint, and HP Print Service Plugin for Android help people print from the devices they use, while HP-quality black and color output and a 3-inch touchscreen mono graphics display make common tasks easier to manage from setup through final page, creating a practical productivity hub for frequent printing, multipage handling, flexible access, and everyday output across day-to-day work.",
      "long_message_safe_to_inherit": "Handle recurring document work with fewer ink interruptions, fewer manual steps, and connection choices that fit shared spaces. This HP Smart Tank all-in-one combines a premium high-capacity ink tank design with included Original HP Ink bottles, print, copy, scan, fax, a 35-page automatic document feeder, and automatic two-sided printing, so everyday forms, packets, records, and color documents move through one capable device. Built-in Ethernet, dual-band Wi-Fi, Wi-Fi Direct, USB, the HP app, Apple AirPrint, and HP Print Service Plugin for Android help people print from the devices they use, while HP-quality black and color output and a 3-inch touchscreen mono graphics display make common tasks easier to manage from setup through final page, creating a practical productivity hub for frequent printing, multipage handling, flexible access, and everyday output across day-to-day work.",
      "mid_length": "Print more and manage less with high-capacity ink, all-in-one document tools, flexible connectivity, and HP-quality output in one premium device.",
      "mid_length_safe_to_inherit": "Print more and manage less with high-capacity ink, all-in-one document tools, flexible connectivity, and HP-quality output in one HP Smart Tank device.",
      "short_message": "High-capacity ink, document tools, flexible connections, and HP quality keep productivity moving.",
      "ultra_short": "Print more, manage less"
    },
    "_chatSession": {
      "responseId": "resp_0f70e9f7d4bb0c88006aa332fa0e4c81969258ccd581434f8e",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Messi",
  "camera_tag": "Printer_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging provides concrete cues around shared spaces, forms, reports, packets, records, learning materials, and everyday document review. Technical feature claims were treated as context only, not visual requirements.",
  "count_explanation": "Four numbered KSPs contain some usable scene cues, so up to four prompts were allowed. Two prompts were returned because the cues cluster into overlapping office document work and education preparation, and the medium oblique view supports only a local setting with limited props.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "invoices, forms, learning materials, records, and everyday admin needs"
        },
        {
          "path": "KSP1.mid_length",
          "quote": "frequent color and document work in shared spaces"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Office forms and records informed p1; learning materials informed p2. Ink capacity and refill claims were omitted because they are product benefits, not scene elements."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "forms, reports, packets, and records"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "during busy days"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "The document-work cue supports the office forms stack in p1 and the learning packet in p2. Device functions and feeder details were omitted to avoid describing the target product or adding unsupported hardware."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "giving people in shared spaces practical ways to print from common devices"
        },
        {
          "path": "KSP3.mid_length",
          "quote": "common devices"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The shared-space cue supports the office environment in p1. Connection methods and common devices were not visualized because connectivity is technical and extra hardware would exceed the local scene scope."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Make everyday pages easier to create and review"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "documents and color materials"
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Everyday page review and document materials support simple paper-based work surfaces in both prompts. Output quality and touchscreen references were omitted as product-specific claims."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "connection choices that fit shared spaces"
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "everyday forms, packets, records, and color documents"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2"
    ],
    "explanation": "The value proposition reinforces a practical shared document-work context. It did not increase the prompt count, but it helped keep the settings coherent and productivity-oriented."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Light wood worktable, single pen, muted partition edge, and soft daylight are plausible additions used to localize the shared office document setting within the medium view."
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Lightly worn wood, slim folder, diffuse daylight, and a softly blurred classroom noticeboard are plausible additions used to suggest education preparation without requiring a full classroom."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "full shared workspace",
          "people using common devices",
          "multipage workflow details",
          "hardware and connection specifics"
        ],
        "explanation": "The medium oblique profile allows a local surface, no more than two nearby props, and one subordinate background detail. The prompt keeps a compact stack of forms, one pen, and a muted partition edge while avoiding people and busy room detail."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "full classroom",
          "students or teachers",
          "large supply layout",
          "device-specific page handling"
        ],
        "explanation": "The view can support an education cue through a cropped learning packet, one folder, and a single background noticeboard. Broader classroom activity was simplified to preserve the selected product-camera framing."
      }
    ],
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "36c80664c5aa37566415dbc59fc321f7e6d63ff98a2446976f6a2a2923a13f07",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "a6750b3f3034a80926c0519f4651865f3c48c5544bb63e1a742aeb17f08ca9e1",
  "source_semantic_sha256": "8189f3ad5af37a814b680c32ab1023a762aefbfc1c75d0f5d958ff4a6849dd2d",
  "input_raw_sha256": "6d96bb8b09532d60a12f30a1131c99797a68d6374043d9c6613d4e4ad40dc608",
  "recorded_input_semantic_sha256": "e674f69f73dee0826312d0d44ea0faaa0fe1feaddbdfc5d216c60207ecafb5ae",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvzHo3L57Z0HSG7GCPo12u8jzvT3",
  "usage": {
    "completion_tokens": 2141,
    "prompt_tokens": 13091,
    "total_tokens": 15232,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 298,
      "engine_ttlt_ms": 19813,
      "pre_inference_ms": 208,
      "service_tbt_ms": 9,
      "service_ttft_ms": 1137,
      "service_ttlt_ms": 20648,
      "user_visible_ttft_ms": 929
    }
  },
  "attempt": 1,
  "latency_seconds": 21.49,
  "started_at": "2026-10-22T22:55:46.947382+00:00",
  "completed_at": "2026-10-22T22:56:08.437500+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "20_actual_printer_messi_front_right_medium",
  "source_id": "8189f3ad5af37a81",
  "product_name": "Messi",
  "camera_tag": "Printer_Front_Right_Medium",
  "purpose": "Previously uncovered actual shared-space printer source under a medium oblique view.",
  "input_path": "inputs/20_actual_printer_messi_front_right_medium.json",
  "input_raw_sha256": "6d96bb8b09532d60a12f30a1131c99797a68d6374043d9c6613d4e4ad40dc608",
  "input_semantic_sha256": "e674f69f73dee0826312d0d44ea0faaa0fe1feaddbdfc5d216c60207ecafb5ae",
  "source_kind": "actual",
  "source_semantic_sha256": "8189f3ad5af37a814b680c32ab1023a762aefbfc1c75d0f5d958ff4a6849dd2d",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/8189f3ad5af37a81.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK881963376314406021.zip",
      "member": "Source Messaging - cb0d856e-5f4e-4928-bb04-1dd770c491d1.json",
      "sha256": "3be81e2250494efef3678e51095f9356e52c32ce744c5659b6b05e3a3f5b8d06"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "20_actual_printer_messi_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/20_actual_printer_messi_front_right_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 35,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 31,
      "environment": "Education"
    }
  ],
  "prompt_count": 2,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 21_actual_printer_magic_enterprise_front_right_medium

Previously uncovered actual enterprise-printer source under a medium oblique view.

- Requested product: `Magic`
- Requested camera: `Printer_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A shared office counter in durable light laminate, with a compact stack of everyday forms and a single pen. A softly blurred corridor wall adds quiet workplace context in diffuse daylight.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Front_Right_Medium",
  "resolved_tag": "Printer_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Magic",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png`

SHA-256: `66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 79199,
    "sha256": "66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda",
    "zip_crc32": "6993477e"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer/camera_printer.locator_Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer_Front_Right_Medium.png",
    "bytes": 79199,
    "sha256": "66af09c32136047a07733426086781ffc7fadcee388ca1f9583a7088aebe9cda",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Keep shared printing moving\n\nOR\n\nBuilt for daily output demands",
      "long_message_best_sku": "Keep shared print work moving with fewer bottlenecks. The HP LaserJet Enterprise 6501dn Printer supports high-volume A4 mono output with automatic two-sided printing and a recommended monthly page volume of 3,750 to 18,750 pages. Busy teams can produce everyday documents with fewer interruptions.",
      "long_message_safe_to_inherit": "Keep shared print work moving with fewer bottlenecks. The HP LaserJet Enterprise 6501dn Printer supports high-volume A4 mono output with automatic two-sided printing and a workload range designed for shared environments. Busy teams can produce everyday documents with fewer interruptions.",
      "mid_length": "Keep shared print work moving with fewer bottlenecks. Automatic two-sided printing and a 3,750 to 18,750-page recommended monthly volume support high-volume output.",
      "mid_length_safe_to_inherit": "Keep shared print work moving with fewer bottlenecks. Automatic two-sided printing and a workload range designed for shared environments support high-volume output.",
      "short_message": "Keep shared print work moving with automatic two-sided output for high-volume A4 needs.",
      "short_message_safe_to_inherit": "Keep shared print work moving with automatic two-sided output for high-volume A4 needs.",
      "ultra_short": "High-volume output",
      "ultra_short_safe_to_inherit": "High-volume output"
    },
    "KSP2": {
      "headline": "Print endpoint protection\n\nOR\n\nReduce risk across the fleet",
      "long_message_best_sku": "Reduce print endpoint risk without adding extra steps to everyday work. HP Sure Start helps validate firmware integrity, while Memory Shield provides hardware-based runtime intrusion detection and Control Flow Integrity. The result is stronger protection for documents, devices, and connections across shared network printing.",
      "long_message_safe_to_inherit": "Reduce print endpoint risk without adding extra steps to everyday work. HP Sure Start helps validate firmware integrity, while Memory Shield provides hardware-based runtime intrusion detection and Control Flow Integrity. The result is stronger protection for documents, devices, and connections across shared network printing.",
      "mid_length": "Reduce print endpoint risk without adding extra steps. HP Sure Start and Memory Shield support firmware integrity and hardware-based runtime intrusion detection.",
      "mid_length_safe_to_inherit": "Reduce print endpoint risk without adding extra steps. HP Sure Start and Memory Shield support firmware integrity and hardware-based runtime intrusion detection.",
      "short_message": "Reduce endpoint risk with HP Sure Start and Memory Shield protections for shared network printing.",
      "short_message_safe_to_inherit": "Reduce endpoint risk with HP Sure Start and Memory Shield protections for shared network printing.",
      "ultra_short": "Endpoint risk reduction",
      "ultra_short_safe_to_inherit": "Endpoint risk reduction"
    },
    "KSP3": {
      "headline": "Fits your fleet\n\nOR\n\nWorkflows with room to adapt",
      "long_message_best_sku": "Fit shared printing into the systems your teams already use. HP FutureSmart firmware supports fleet consistency, while Workpath and OXPd extensibility help adapt workflows over time. IT can standardize devices across shared print environments while preserving room for workflow needs without creating a separate management burden.",
      "long_message_safe_to_inherit": "Fit shared printing into the systems your teams already use. HP FutureSmart firmware supports fleet consistency, while Workpath and OXPd extensibility help adapt workflows over time. IT can standardize devices across shared print environments while preserving room for workflow needs without creating a separate management burden.",
      "mid_length": "Fit shared printing into systems your teams already use. FutureSmart firmware and Workpath with OXPd extensibility support fleet consistency and adaptable workflows.",
      "mid_length_safe_to_inherit": "Fit shared printing into systems your teams already use. FutureSmart firmware and Workpath with OXPd extensibility support fleet consistency and adaptable workflows.",
      "short_message": "Fit shared printing into existing systems with FutureSmart firmware and Workpath extensibility.",
      "short_message_safe_to_inherit": "Fit shared printing into existing systems with FutureSmart firmware and Workpath extensibility.",
      "ultra_short": "Fleet-ready workflows",
      "ultra_short_safe_to_inherit": "Fleet-ready workflows"
    },
    "KSP4": {
      "headline": "Fewer paper interruptions\n\nOR\n\nCapacity for shared demand",
      "long_message_best_sku": "Reduce reloads and interruptions in busy shared environments. The HP LaserJet Enterprise 6501dn Printer includes 650-sheet standard input and expands to a 2,850-sheet maximum input with optional paper handling. Teams can support larger jobs and daily document demand with fewer stops.",
      "long_message_safe_to_inherit": "Reduce reloads and interruptions in busy shared environments. The HP LaserJet Enterprise 6501dn Printer includes standard input that expands with optional paper handling. Teams can support larger jobs and daily document demand with fewer stops across shared print areas.",
      "mid_length": "Reduce reloads and interruptions in busy shared environments. 650-sheet standard input expands to a 2,850-sheet maximum input with optional paper handling.",
      "mid_length_safe_to_inherit": "Reduce reloads and interruptions in busy shared environments. Standard input expands with optional paper handling to support shared document demand.",
      "short_message": "Reduce reloads with 650-sheet standard input that expands for shared demand needs.",
      "short_message_safe_to_inherit": "Reduce reloads with standard input that expands for shared document demand needs.",
      "ultra_short": "Fewer reloads",
      "ultra_short_safe_to_inherit": "Fewer reloads"
    },
    "ValueProposition": {
      "headline": "High-volume printing, easier fleet control",
      "long_message_best_sku": "The HP LaserJet Enterprise 6501dn Printer helps large shared print environments keep everyday documents moving while giving IT a stronger foundation for fleet control, endpoint protection, and long-term standardization across A4 mono devices. Built for high-volume output, it pairs automatic two-sided printing, a recommended monthly page volume of 3,750 to 18,750 pages, and a 650-sheet standard input that expands to a 2,850-sheet maximum input, so busy teams can produce document sets with fewer reloads and fewer interruptions. The 4.3-inch color touchscreen and walk-up USB simplify walk-up use, while FutureSmart firmware, HP Web Jetadmin, Workpath and OXPd extensibility, embedded Gigabit Ethernet, HP Sure Start, Memory Shield, Connection Inspector, TPM 2.0, storage encryption, and TLS 1.2/1.3 support consistent deployment, adaptable workflows, and stronger protection for a shared network print endpoint.",
      "long_message_safe_to_inherit": "The HP LaserJet Enterprise 6501dn Printer helps large shared print environments keep everyday documents moving while giving IT a stronger foundation for fleet control, endpoint protection, and long-term standardization across A4 mono devices. Built for high-volume output, it pairs automatic two-sided printing, a workload range designed for shared environments, and standard input that expands with optional paper handling, so busy teams can produce document sets with fewer reloads and fewer interruptions. The 4.3-inch color touchscreen and walk-up USB simplify walk-up use, while FutureSmart firmware, HP Web Jetadmin, Workpath and OXPd extensibility, embedded Gigabit Ethernet, HP Sure Start, Memory Shield, Connection Inspector, TPM 2.0, storage encryption, and TLS 1.2/1.3 support consistent deployment, adaptable workflows, and stronger protection for a shared network print endpoint.",
      "mid_length": "Keep shared A4 mono printing productive, manageable, and better protected with automatic two-sided output, fleet-ready firmware, embedded security, and expandable input.",
      "mid_length_safe_to_inherit": "Keep shared A4 mono printing productive, manageable, and better protected with automatic two-sided output, fleet-ready firmware, embedded security, and expandable input.",
      "short_message": "Productive A4 mono printing with fleet control, embedded security, and expandable input.",
      "ultra_short": "Print fleet control"
    },
    "_chatSession": {
      "responseId": "resp_0fe3880b841b2ab3006aa0470d4e488194b22e72a0778041f8",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging is coherent and office-oriented, with repeated cues around shared environments, busy teams, everyday documents, workflows, and reduced interruptions. Technical security, fleet, firmware, capacity, and product-specific claims were treated as nonvisual context rather than scene requirements.",
  "count_explanation": "Four numbered KSPs contain usable workplace or document-flow cues, but they all point to the same shared office document environment. One prompt combines the overlapping cues without adding unsupported separate scenarios.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "Keep shared print work moving with fewer bottlenecks."
        },
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "Busy teams can produce everyday documents with fewer interruptions."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Mapped to a shared office counter with everyday forms. Product-specific output, duplexing, A4, and volume claims were omitted as device and specification details."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "everyday work"
        },
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "documents, devices, and connections across shared network printing"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The everyday work and document cues support the office context. Endpoint protection, firmware integrity, and intrusion detection are abstract technical claims and were not visualized as guards, locks, or security props."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "systems your teams already use"
        },
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "shared print environments"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The team and shared-environment language reinforces a common workplace setting. Fleet consistency, firmware, extensibility, and management burden were not represented visually because they are system-level concepts."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "busy shared environments"
        },
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "Teams can support larger jobs and daily document demand with fewer stops."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Mapped to a compact stack of forms suggesting daily document demand. Paper capacity and reload claims were simplified to a small paper cue within the medium-view prop limit."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "large shared print environments keep everyday documents moving"
      },
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "busy teams can produce document sets with fewer reloads and fewer interruptions"
      }
    ],
    "prompt_ids": [
      "p1"
    ],
    "explanation": "Used to unify the scene as a shared office document area. Fleet control, endpoint protection, touchscreen, USB, Ethernet, encryption, and protocol details were omitted as nonvisual or product-specific."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Durable light laminate counter chosen as a plausible shared office surface.",
        "Single pen added as an ordinary low-profile work prop within the two-prop limit.",
        "Softly blurred corridor wall added as the one permitted background detail for local workplace context."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "No people or busy team activity required",
          "No room-wide print area or furniture collection",
          "Security, fleet management, firmware, and network claims omitted as abstract",
          "High-volume and paper-capacity claims reduced to a compact stack of forms",
          "No product names, device references, or device-dependent interaction included"
        ],
        "explanation": "The selected preset supports a local medium oblique setting with at most two nearby props and one subordinate background detail. The prompt retains the shared office document cue using forms and a pen while keeping the surrounding context modest."
      }
    ],
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "5bcffe0d851bc13aafd2ff396c0448715443bcba42a8ef14d6e62abcfa1b9a1b",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "a6750b3f3034a80926c0519f4651865f3c48c5544bb63e1a742aeb17f08ca9e1",
  "source_semantic_sha256": "324b14a617dfedbaa74ed0f14b93d038737a01c1fa6180a9af37de60905f53a9",
  "input_raw_sha256": "fa6a8903d7ef9eea25b37eb3305cadeb4cda27f2d92726f4e04db93bfd8096d4",
  "recorded_input_semantic_sha256": "9b63267e4b9ea06219a285c929135adaf8399c7100896e1d49b1e92102c0d853",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-EbvzcK45Dz8RCqESVLiaWFwcf9Tbo",
  "usage": {
    "completion_tokens": 2037,
    "prompt_tokens": 13004,
    "total_tokens": 15041,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1024,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 10,
      "engine_ttft_ms": 232,
      "engine_ttlt_ms": 19800,
      "pre_inference_ms": 145,
      "service_tbt_ms": 10,
      "service_ttft_ms": 670,
      "service_ttlt_ms": 20232,
      "user_visible_ttft_ms": 525
    }
  },
  "attempt": 1,
  "latency_seconds": 20.995,
  "started_at": "2026-10-22T22:56:08.462406+00:00",
  "completed_at": "2026-10-22T22:56:29.457689+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "21_actual_printer_magic_enterprise_front_right_medium",
  "source_id": "324b14a617dfedba",
  "product_name": "Magic",
  "camera_tag": "Printer_Front_Right_Medium",
  "purpose": "Previously uncovered actual enterprise-printer source under a medium oblique view.",
  "input_path": "inputs/21_actual_printer_magic_enterprise_front_right_medium.json",
  "input_raw_sha256": "fa6a8903d7ef9eea25b37eb3305cadeb4cda27f2d92726f4e04db93bfd8096d4",
  "input_semantic_sha256": "9b63267e4b9ea06219a285c929135adaf8399c7100896e1d49b1e92102c0d853",
  "source_kind": "actual",
  "source_semantic_sha256": "324b14a617dfedbaa74ed0f14b93d038737a01c1fa6180a9af37de60905f53a9",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/324b14a617dfedba.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK901460674462796743.zip",
      "member": "Source Messaging - 27735f23-c479-4d5b-8951-cdf900133f0b.json",
      "sha256": "8ba3311a2196b3f0059c6f703fc260dc14f0fce1889420fe80a99c4e4c0087f4"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "21_actual_printer_magic_enterprise_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/21_actual_printer_magic_enterprise_front_right_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 31,
      "environment": "Office"
    }
  ],
  "prompt_count": 1,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Magic",
    "resolved_product": "Magic_Printers-6500_dn_CMF-Atmosphere_Blues.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

## 22_actual_printer_messi_ink_tank_front_right_medium

Previously uncovered actual ink-tank all-in-one source under a medium oblique view.

- Requested product: `Messi`
- Requested camera: `Printer_Front_Right_Medium`
- Offline resolver agrees with output debug: **yes**

### Generated text prompts

**p1 · Office**

A shared office worktable with a clean laminate surface, a compact stack of forms, and a single pen. A softly blurred file tray sits in the background under even daylight.

**p2 · Education**

A school preparation table with lightly worn wood, the cropped edge of a worksheet, and a small stack of marked lesson pages. A simple chair back stays softly out of focus in daylight.

### Exact resolved profile limits

```json
{
  "requested_tag": "Printer_Front_Right_Medium",
  "resolved_tag": "Printer_Front_Right_Medium",
  "resolution": "exact",
  "requested_product": "Messi",
  "resolved_product": "Messi_Ceramic-White.printer.usdz",
  "product_resolution": "alias",
  "profile_version": "camera-v2-draft-2026-10-22",
  "registry_status": "draft_for_text_evaluation",
  "device_family": "printer",
  "source_camera_name": "Front_Right_Medium",
  "effective_profile": {
    "framing": "medium",
    "elevation": "oblique",
    "max_local_props": 2,
    "max_background_details": 1,
    "people_policy": "optional_partial_activity"
  },
  "applied_overrides": [],
  "restrictions_applied": [],
  "incompatible_reason": null,
  "used_minimal_fallback": false
}
```

### Matching offline camera reference

Exact local reference: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png`

SHA-256: `ac16182e6f9217ac2ca1e9de1ce6b7f99390c56d6c155b25e9a071bdf0ab49ca`

```json
{
  "available": true,
  "kind": "exact_zip_asset",
  "match_rule": "resolved full product name + source camera name + device family, all exact",
  "resolved_product": "Messi_Ceramic-White.printer.usdz",
  "source_camera_name": "Front_Right_Medium",
  "catalog": {
    "device_id": "camera_printer.locator_Messi_Ceramic-White.printer",
    "device_family": "printer",
    "device_asset_name_from_folder": "Messi_Ceramic-White.printer.usdz",
    "camera_name_exact": "Front_Right_Medium",
    "zip_filename": "Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png",
    "extracted_absolute_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png",
    "width_px": 1024,
    "height_px": 576,
    "image_format": "PNG",
    "bytes": 26168,
    "sha256": "ac16182e6f9217ac2ca1e9de1ce6b7f99390c56d6c155b25e9a071bdf0ab49ca",
    "zip_crc32": "cdb07c0e"
  },
  "local": {
    "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/HP_scenes/extracted/Shared/camera_printer.locator_Messi_Ceramic-White.printer/camera_printer.locator_Messi_Ceramic-White.printer_Front_Right_Medium.png",
    "bytes": 26168,
    "sha256": "ac16182e6f9217ac2ca1e9de1ce6b7f99390c56d6c155b25e9a071bdf0ab49ca",
    "mime_type": "image/png"
  }
}
```

<details><summary>Full input JSON</summary>

```json
{
  "source_messaging": {
    "KSP1": {
      "headline": "Print longer between refills\n\nOR\n\nMore ink from day one",
      "long_message_best_sku": "Print more of the documents you need with fewer ink interruptions. HP Smart Tank 7602 All-in-One includes Original HP Ink and a high-capacity refillable ink tank system, giving frequent printing a stronger supply foundation from the start. Keep forms, records, school materials, and color documents moving without making ink management the center of your day.",
      "long_message_safe_to_inherit": "Print more of the documents you need with fewer ink interruptions. HP Smart Tank all-in-one printers include Original HP Ink and a high-capacity refillable ink tank system, giving frequent printing a stronger supply foundation from the start. Keep forms, records, school materials, and color documents moving without making ink management the center of your day.",
      "mid_length": "Print more with fewer ink interruptions. Included Original HP Ink and a high-capacity refillable tank system help support regular document work from day one.",
      "mid_length_safe_to_inherit": "Print more with fewer ink interruptions. Included Original HP Ink and a high-capacity refillable tank system help support regular document work from day one.",
      "short_message": "Included Original HP Ink helps support regular printing with fewer refill interruptions.",
      "short_message_safe_to_inherit": "Included Original HP Ink helps support regular printing with fewer refill interruptions.",
      "ultra_short": "Ink that lasts",
      "ultra_short_safe_to_inherit": "Ink that lasts"
    },
    "KSP2": {
      "headline": "Keep paperwork moving\n\nOR\n\nLess manual document handling",
      "long_message_best_sku": "Move through everyday document work with less manual effort. A 35-page auto document feeder, automatic two-sided printing, and fax help HP Smart Tank 7602 All-in-One handle multi-page paperwork, copies, scans, and administrative tasks in one place. Spend less time feeding pages by hand and more time finishing the work that keeps your day organized.",
      "long_message_safe_to_inherit": "Move through everyday document work with less manual effort. An auto document feeder, automatic two-sided printing, and fax help HP Smart Tank all-in-one printers handle multi-page paperwork, copies, scans, and administrative tasks in one place. Spend less time feeding pages by hand and more time finishing the work that keeps your day organized.",
      "mid_length": "Move through everyday document work with less manual effort. An auto document feeder, automatic two-sided printing, and fax help streamline multi-page tasks.",
      "mid_length_safe_to_inherit": "Move through everyday document work with less manual effort. An auto document feeder, automatic two-sided printing, and fax help streamline multi-page tasks.",
      "short_message": "An auto document feeder, duplex printing, and fax help simplify recurring paperwork.",
      "short_message_safe_to_inherit": "An auto document feeder, duplex printing, and fax help simplify recurring paperwork.",
      "ultra_short": "Paperwork made easier",
      "ultra_short_safe_to_inherit": "Paperwork made easier"
    },
    "KSP3": {
      "headline": "One hub for documents\n\nOR\n\nPrint, scan, copy, fax",
      "long_message_best_sku": "Handle common document tasks from one compact device. HP Smart Tank 7602 All-in-One brings print, copy, scan, fax, ADF, and wireless capabilities together, with flatbed and ADF scanning for everyday paper handling. Create copies, digitize pages, send fax documents, and manage routine output without switching devices.",
      "long_message_safe_to_inherit": "Handle common document tasks from one compact device. HP Smart Tank all-in-one printers bring print, copy, scan, fax, ADF, and wireless capabilities together, with flexible scanning for everyday paper handling. Create copies, digitize pages, send fax documents, and manage routine output without switching devices.",
      "mid_length": "Handle common document tasks from one compact device. Print, copy, scan, fax, ADF, and wireless capabilities support everyday paper handling.",
      "mid_length_safe_to_inherit": "Handle common document tasks from one compact device. Print, copy, scan, fax, ADF, and wireless capabilities support everyday paper handling.",
      "short_message": "Print, copy, scan, fax, ADF, and wireless features support everyday document work.",
      "short_message_safe_to_inherit": "Print, copy, scan, fax, ADF, and wireless features support everyday document work.",
      "ultra_short": "One document hub",
      "ultra_short_safe_to_inherit": "One document hub"
    },
    "KSP4": {
      "headline": "Connect your way\n\nOR\n\nShared access, simplified",
      "long_message_best_sku": "Print from the devices your space already uses. Ethernet, USB, dual-band Wi-Fi, Wi-Fi Direct, the HP app, Apple AirPrint, and Android printing help HP Smart Tank 7602 All-in-One support laptops, phones, and shared workflows. Keep access flexible across wired, wireless, and mobile printing needs.",
      "long_message_safe_to_inherit": "Print from the devices your space already uses. Ethernet, USB, dual-band Wi-Fi, Wi-Fi Direct, the HP app, Apple AirPrint, and Android printing help HP Smart Tank all-in-one printers support laptops, phones, and shared workflows. Keep access flexible across wired, wireless, and mobile printing needs.",
      "mid_length": "Print from the devices your space already uses. Ethernet, dual-band Wi-Fi, Wi-Fi Direct, and mobile printing help keep access flexible.",
      "mid_length_safe_to_inherit": "Print from the devices your space already uses. Ethernet, dual-band Wi-Fi, Wi-Fi Direct, and mobile printing help keep access flexible.",
      "short_message": "Ethernet, dual-band Wi-Fi, Wi-Fi Direct, and mobile printing support shared access.",
      "short_message_safe_to_inherit": "Ethernet, dual-band Wi-Fi, Wi-Fi Direct, and mobile printing support shared access.",
      "ultra_short": "Flexible printing access",
      "ultra_short_safe_to_inherit": "Flexible printing access"
    },
    "ValueProposition": {
      "headline": "High-capacity productivity for everyday documents",
      "long_message_best_sku": "Print often, manage paperwork, and connect across shared devices with one practical ink tank all-in-one. HP Smart Tank 7602 All-in-One pairs included Original HP Ink and a high-capacity refillable ink system with the productivity tools needed for recurring document work, including a 35-page auto document feeder, automatic two-sided printing, fax, print, copy, scan, and wireless capabilities. Ethernet, dual-band Wi-Fi, Wi-Fi Direct, the HP app, Apple AirPrint, and Android printing help make access flexible from laptops and phones, so forms, records, school materials, scans, copies, and color documents keep moving from one compact hub.",
      "long_message_safe_to_inherit": "Print often, manage paperwork, and connect across shared devices with one practical ink tank all-in-one. HP Smart Tank all-in-one printers pair included Original HP Ink and a high-capacity refillable ink system with the productivity tools needed for recurring document work, including an auto document feeder, automatic two-sided printing, fax, print, copy, scan, and wireless capabilities. Ethernet, dual-band Wi-Fi, Wi-Fi Direct, the HP app, Apple AirPrint, and Android printing help make access flexible from laptops and phones, so forms, records, school materials, scans, copies, and color documents keep moving from one compact hub.",
      "mid_length": "Print often with fewer ink interruptions, document tools, all-in-one functions, and flexible wired, wireless, and mobile access from one HP Smart Tank printer.",
      "mid_length_safe_to_inherit": "Print often with fewer ink interruptions, document tools, all-in-one functions, and flexible wired, wireless, and mobile access from one HP Smart Tank printer.",
      "short_message": "Included ink, document tools, and flexible connections support everyday printing needs.",
      "ultra_short": "Ink tank productivity"
    },
    "_chatSession": {
      "responseId": "resp_0484532a5ea265d6006aa42fc9786c819695503fce300316d5",
      "model": "gpt-5.5",
      "systemInstructions": "You are an expert HP copywriter generating Source Messaging from a required Smart Brief.Generate Source Messaging only: one Value Proposition and KSP1 through KSP4.Do not generate eTail Messaging or any other deliverable type. eTail Messaging ishandled by a separate, downstream process once Source Messaging is approved.The Smart Brief, provided in the user message as JSON, is the required primarysource of truth. The user message also supplies the customer-facing product name,internal code name, and approved configuration scope for this run. Other inputs maybe used only when they are explicitly identified as approved inputs.INTERNAL WORK VS. OUTPUTSteps 1 through 6 are internal working steps. Perform them silently before returningthe JSON output.Do not output, anywhere in the response:- A prohibitions list- An audience profile- Product information as a separate section- Analysis or rationale- Verification notes- Quality-gate results- Word or character counts- The internal product code name- Any deliverable other than Source Messaging (Value Proposition + KSP1-4)- Any commentary, markdown, or text outside the required JSON objectIf no Smart Brief is provided, do not generate copy. Return an empty result andexplain nothing is available to act on.If the Smart Brief and other explicitly approved inputs do not contain enoughvalidated information to support the required Value Proposition and four KSPs, donot invent, infer, upgrade, combine, or assume information. Leave the affectedfield(s) empty rather than fabricate content.STEP 1: EXTRACT AND LOCK PROHIBITIONSRead the Smart Brief's CLAIMS DISCLAIMERS section and every item marked validationrequired, watchout, not validated, or equivalent. Apply the same review to anyother explicitly approved input. Build an internal prohibition list and obey itthroughout the copy.Universal prohibitions:- Never position the product as a gaming, creator, workstation, AI, or premium PC unless explicitly validated in an approved input.- Never reference an NPU, AI acceleration, or AI features unless explicitly validated.- Never reference enterprise security features unless explicitly validated.- Never use quiet operation, whisper-quiet, or any silence claim unless explicitly validated.- Never use unvalidated performance superlatives such as fast, instant,snappy, lightning, or blazing. Such language requires support from a named benchmark, certification, or other explicit validation in an approved input.- Never imply that every configuration includes dual SSD slots, a bundled keyboard and mouse, or any other configuration-dependent feature unless validated as universal.- Never use up to in any copy field.- Never use the internal product code name in any copy field.- Never write customer-facing copy in question format.- Never use an em dash in any copy field.- Never use demographic descriptors, including income brackets, age ranges, employment-status labels, or generational labels.Banned hedge language:- may be available with- may include- details may vary- signals- is part of the story too- Vague substitutes such as options or details when an approved input provides a concrete noun or factHANDLING VALIDATION-REQUIRED CLAIMSWhen a selected claim requires validation or qualification:1. State the fact plainly in the body copy with its approved footnote marker, such as EPEAT Gold certified*.2. Put the approved qualifier or disclaimer only in the field's disclaimer field.3. Reproduce the approved qualifier or disclaimer verbatim. Do not summarize,  rewrite, shorten, or reinterpret it.4. Do not soften, euphemize, genericize, or remove the selected claim.5. Do not carry a disclaimer-dependent claim unless its approved marker and  disclaimer treatment can be preserved.Preserve all qualifiers, trademark requirements, footnote markers, and approveddisclaimers. Reproduce disclaimers verbatim. Never apply a claim or disclaimerbeyond its approved series, platform, model, SKU, configuration, or market.STEP 2: BUILD THE AUDIENCE PROFILEFrom the Smart Brief's TARGET AUDIENCE section and any other explicitly approvedaudience input, identify internally:- Primary and secondary buyer segments- Ranked purchase drivers- Language the audience uses when discussing PCs- Relevant tasks, use cases, and pain points- The audience's don't-care itemsExclude every feature, theme, and proof point belonging to a don't-care category.Translate audience information into need-based, task-based, or use-case language.Do not use prohibited demographic or employment-status descriptors in the copy.Do not expand an approved audience, use case, or market beyond its documented scope.STEP 3: EXTRACT PRODUCT IDENTITYThe customer-facing product name, internal code name, and approved configurationscope (PCC) are provided directly in the user message — use those values asauthoritative. Extract any remaining identity details (brand and sub-brand, series,product category, launch cycle, market scope, trademark requirements) internallyfrom the Smart Brief's HANDOFF PACKAGE and CLAIMS DISCLAIMERS sections, if present.Use the internal code name only to confirm it is excluded from output — neverstate it in any field.Use only the customer-facing product identity in the copy. Reproduce product namesand required trademarks accurately. Never transfer a product name, claim,specification, qualifier, disclaimer, or proof point from one series, platform,model, SKU, configuration, or market to another. Never apply a claim outside theapproved configuration scope provided in the user message.STEP 4: MAP VERIFIED FACTS AND KSPsFrom the Smart Brief's PROOF POINTS and KSP HIERARCHY sections:- Map KSP1 through KSP4 to the actual ranked KSPs, preserving their approved order.- Assign no more than two audience-relevant, validated proof points to each KSP.- Exclude proof points belonging to a don't-care category.- If fewer than four KSPs are explicitly ranked, use only the next strongest supporting themes explicitly emphasized in an approved input.- Never invent a KSP, feature, benefit, proof point, certification, SEO claim, product capability, audience, use case, or practical outcome.- Never combine separate claims to create a broader or stronger claim.- Never upgrade qualified language into an absolute claim.- Never default KSP4, or any other slot, to sustainability or recycling.- Use sustainability as a KSP only if an approved input ranks or explicitly emphasizes it. Place it in whichever KSP position the approved hierarchy establishes.- Keep every claim, proof point, qualifier, and disclaimer within its approved product and market scope.Sustainability rule (only if sustainability appears as an approved KSP):- Use only certified, legally defensible claims.- Add the approved footnote markers to claims requiring registration, configuration, or validation qualifiers.- Reproduce the full approved qualifier or disclaimer verbatim in the corresponding disclaimer field.- Never soften an unsupported environmental claim into vague language.- Never broaden a sustainability claim beyond the approved series, platform, model, SKU, configuration, or market.STEP 5: APPLY VOICE AND MESSAGE DISCIPLINEWrite customer-facing messages using the structure: customer context or need ->benefit -> supporting feature or specification -> practical outcome. Lead with thebenefit and use technical information as proof. Translate jargon into customervalue while preserving technical accuracy. Do not force every field to contain allfour components when its length tier cannot support them.Tone: confident, plainspoken, benefit-led, specific, relevant to practical buyers,free of enthusiast language, benchmark jargon, and spec-heavy openings.Sentence discipline:- Every sentence must communicate a concrete fact, a meaningful benefit, or both.- Lead with the benefit and the point.- Use technical information as supporting proof.- Translate technical terminology into practical customer value without changing its technical meaning.- Do not use scene-setting openings such as In today's world.- Do not use filler closings such as for the tasks life asks of it.- Avoid abstract framing and empty lifestyle language.- Remove any phrase that adds neither a fact nor a benefit.Best SKU vs. Safe to Inherit:- Best SKU copy uses specific, permitted product facts and may name an approved processor family, port count, certification, material, feature, or other exact proof point, kept within its approved SKU/configuration/model/platform/market scope.- Safe-to-Inherit copy is a surgical derivative of its same-length Best SKU counterpart: same opening, message arc, structure, tone, main benefit, and practical outcome. It genericizes only configuration-variable specifications, stays concrete and meaningful, and must not become a vague rewrite or broaden scope beyond what Best SKU is approved for.Example: a configuration-specific processor model becomes a capable processor; a configuration-specific port count becomes front-access connections.Tier compression: create long, short, mid, and ultra-short versions throughsemantic compression. Cut words, not meaning. Preserve the same customer need,main benefit, strongest proof, and core practical outcome at every tier. Do notintroduce a new message, claim, benefit, feature, specification, use case, orproof point in a shorter tier, and do not expand a claim's scope while shorteningit. Ultra Short must be the distilled core of the corresponding Long Message BestSKU.STEP 6: GENERATE SOURCE MESSAGINGGenerate in this exact order: Value Proposition, KSP1, KSP2, KSP3, KSP4.Value Proposition rules:- Open with the audience outcome or need, never Introducing.- Synthesize all four approved KSP themes into one coherent message.- Use only approved facts.- Follow customer context/need -> benefit -> supporting proof -> practical outcome.- Provide exactly one headline. Do not provide alternative headlines.KSP1 through KSP3 rules:- The first sentence must be a pure benefit statement — no feature, specification, certification, or product name in the first sentence.- Use no more than two validated proof points.- Use technical information only as proof of the benefit.- End with a practical outcome when the length tier allows it.- Provide exactly two genuinely distinct headline options that differ in wording and structure, not merely synonym substitution. Join the two options in the headline field with the literal separator \n\nOR\n\n.KSP4 rules: same as KSP1-3, using the KSP4 length targets below.Length targets (word counts are targets, not hard limits, but must not beexceeded by more than one word):- Headline: maximum 8 words- VP Long Message Best SKU / Safe to Inherit: 140-170 words, max 2-3 sentences- VP Mid Length / Safe to Inherit: 20-30 words, max 1-2 sentences- VP Short Message / Safe to Inherit: 12-18 words, one sentence- VP Ultra Short: 2-4 words- KSP1-KSP3 Long Message Best SKU / Safe to Inherit: 45-80 words, max 2-3 sentences- KSP4 Long Message Best SKU / Safe to Inherit: 35-55 words, max 2-3 sentences- KSP Mid Length / Safe to Inherit (all KSPs): 20-30 words, max 1-2 sentences- KSP Short Message / Safe to Inherit (all KSPs): 12-18 words, one sentence- KSP Ultra Short (all KSPs): 2-4 wordsEach Safe-to-Inherit field must match its Best SKU counterpart's target range,structure, message progression, main benefit, and strongest applicable proof.STEP 7: RUN INTERNAL SELF-CHECKS BEFORE RETURNING OUTPUTScan for and correct every failure, then repeat the checks:- up to anywhere in output- the internal product code name anywhere in output- demographic or employment-status descriptors- banned hedge phrases- em dashes- question-format copy- unsupported superlatives- unvalidated AI, security, silence, configuration, performance, or sustainability claims- any Source Messaging field exceeding its word limit- any Safe-to-Inherit field that is not a surgical derivative of its Best SKU counterpart- any don't-care theme appearing anywhere- any claim inferred, invented, upgraded, or created by combining separate claims- any shorter tier that fails to retain the main benefit and strongest proof of its longer version, or that introduces new information- any qualifier, trademark, or footnote marker not preserved- any disclaimer not reproduced verbatim- any claim or disclaimer applied beyond its approved series, platform, model,SKU, configuration, or market- KSP order not matching the approved hierarchy- KSP4 defaulted to sustainability without approval- the two headline options for any KSP not being genuinely distinctOUTPUT FORMATReturn only a JSON object conforming exactly to the response schema configured forthis call. Do not include any text, markdown, labels, or commentary outside thatJSON object, and do not wrap it in a code block"
    }
  },
  "product_name": "Messi",
  "camera_tag": "Printer_Front_Right_Medium"
}
```

</details>

<details><summary>Complete output debug</summary>

```json
{
  "input_assessment": "The source messaging provides concrete document-work cues including forms, records, school materials, paperwork, scans, copies, and shared workflows. The selected product resolves by alias to a supported printer product, and the requested camera is a known medium oblique printer preset.",
  "count_explanation": "Four numbered KSPs contain usable scene cues, but most overlap around routine document handling. Two prompts cover the distinct source-supported contexts that fit the fixed view: a shared office paperwork setting and an education preparation setting.",
  "used_fallback": false,
  "ksp_mappings": [
    {
      "ksp_id": "KSP1",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP1.long_message_best_sku",
          "quote": "Keep forms, records, school materials, and color documents moving without making ink management the center of your day."
        }
      ],
      "prompt_ids": [
        "p1",
        "p2"
      ],
      "explanation": "Forms and records support the office prompt, while school materials support the education prompt. Ink capacity and refill messaging were omitted because they are product claims rather than visible environment details."
    },
    {
      "ksp_id": "KSP2",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP2.long_message_best_sku",
          "quote": "handle multi-page paperwork, copies, scans, and administrative tasks in one place"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The office forms and pen suggest recurring paperwork and administrative tasks. Specific functions and mechanisms were omitted to avoid describing the target device."
    },
    {
      "ksp_id": "KSP3",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP3.long_message_best_sku",
          "quote": "Create copies, digitize pages, send fax documents, and manage routine output without switching devices."
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "The prompt retains the routine document-work context through forms and a worktable. Copy, scan, fax, wireless, and compact-device claims were omitted from scene prose because they are product functionality."
    },
    {
      "ksp_id": "KSP4",
      "eligible_for_additional_prompt": true,
      "source_evidence": [
        {
          "path": "KSP4.long_message_best_sku",
          "quote": "support laptops, phones, and shared workflows"
        }
      ],
      "prompt_ids": [
        "p1"
      ],
      "explanation": "Shared workflows are reflected as a shared office worktable. Extra computing hardware and mobile devices were not added because the view allows only a limited local scene and the prompt must not introduce additional hardware."
    }
  ],
  "value_proposition": {
    "source_evidence": [
      {
        "path": "ValueProposition.long_message_best_sku",
        "quote": "forms, records, school materials, scans, copies, and color documents keep moving"
      }
    ],
    "prompt_ids": [
      "p1",
      "p2"
    ],
    "explanation": "The value proposition reinforces everyday document productivity across office and school-material contexts. The environment prompts preserve those use cases without restating product capabilities."
  },
  "creative_additions": [
    {
      "prompt_id": "p1",
      "details": [
        "Clean laminate surface, single pen, softly blurred file tray, and even daylight were added as ordinary office details within the medium oblique view limit."
      ]
    },
    {
      "prompt_id": "p2",
      "details": [
        "Lightly worn wood, marked lesson pages, chair back, and daylight were added as plausible education-preparation details within the same object and background limits."
      ]
    }
  ],
  "ignored_fields": [
    "_chatSession"
  ],
  "camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "adjustments": [
      {
        "prompt_id": "p1",
        "omitted_or_simplified": [
          "product functions",
          "ink-system claims",
          "extra shared devices",
          "people",
          "busy office layout"
        ],
        "explanation": "The medium oblique preset permits a local setting with at most two nearby props and one subordinate background detail, so the office paperwork cue was reduced to forms, a pen, and one soft background tray."
      },
      {
        "prompt_id": "p2",
        "omitted_or_simplified": [
          "full classroom",
          "teachers or students",
          "shelving and room fixtures",
          "multiple school supplies"
        ],
        "explanation": "The school-material cue was kept as a cropped worksheet and small lesson-page stack on a local table, avoiding broader classroom elements that would exceed the fixed view."
      }
    ],
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Model, request, and hash metadata</summary>

```json
{
  "request_key": "5839a2b14e8816b8b88f2e91d6a528483aff6e7c75b4504ea59a263da4ec0753",
  "system_prompt_sha256": "5e9996e88ab1bd6ef062c9eab9eec8a39bc45e5c918949a95b0455069500dc06",
  "input_schema_sha256": "bfea8b17cd3c9125a5781c002b3e66dbc66868d7a770c042cfcb73490d227af0",
  "output_schema_sha256": "6e16825466cb6f4971060183132a227d19b7c395e16830ced7a4fae9f6d4e7b0",
  "manifest_sha256": "a6750b3f3034a80926c0519f4651865f3c48c5544bb63e1a742aeb17f08ca9e1",
  "source_semantic_sha256": "943faef0af11484f5bee2a60f6bb25ac7d70ee4ab00c220b2ff1e599e2eb58cf",
  "input_raw_sha256": "e48ba726b349e11728def96930422dc0399d8ff8ebfe7fe984e6058cf423e246",
  "recorded_input_semantic_sha256": "58447acc50e22d9e333ccfafc018b6c134b0a9c1bf7db79fc448ed6d224be89b",
  "settings": {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000
  },
  "model": "gpt-5.5-2026-04-24",
  "response_id": "chatcmpl-Ebvzxl63NpHoO1WbgwRHmwwhTITWI",
  "usage": {
    "completion_tokens": 2548,
    "prompt_tokens": 12992,
    "total_tokens": 15540,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1510,
      "rejected_prediction_tokens": 0,
      "text_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cache_write_tokens": null,
      "cached_tokens": 6400,
      "image_tokens": null,
      "text_tokens": null
    },
    "latency_checkpoint": {
      "engine_tbt_ms": 9,
      "engine_ttft_ms": 326,
      "engine_ttlt_ms": 23670,
      "pre_inference_ms": 141,
      "service_tbt_ms": 9,
      "service_ttft_ms": 893,
      "service_ttlt_ms": 24233,
      "user_visible_ttft_ms": 752
    }
  },
  "attempt": 1,
  "latency_seconds": 24.737,
  "started_at": "2026-10-22T22:56:29.482563+00:00",
  "completed_at": "2026-10-22T22:56:54.219720+00:00",
  "schema_valid": true,
  "retry_events": []
}
```

</details>

<details><summary>Manifest case metadata</summary>

```json
{
  "case_id": "22_actual_printer_messi_ink_tank_front_right_medium",
  "source_id": "943faef0af11484f",
  "product_name": "Messi",
  "camera_tag": "Printer_Front_Right_Medium",
  "purpose": "Previously uncovered actual ink-tank all-in-one source under a medium oblique view.",
  "input_path": "inputs/22_actual_printer_messi_ink_tank_front_right_medium.json",
  "input_raw_sha256": "e48ba726b349e11728def96930422dc0399d8ff8ebfe7fe984e6058cf423e246",
  "input_semantic_sha256": "58447acc50e22d9e333ccfafc018b6c134b0a9c1bf7db79fc448ed6d224be89b",
  "source_kind": "actual",
  "source_semantic_sha256": "943faef0af11484f5bee2a60f6bb25ac7d70ee4ab00c220b2ff1e599e2eb58cf",
  "source_input_path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/data/source_json/943faef0af11484f.json",
  "source_origins": [
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/ATSK9166360275256369928.zip",
      "member": "Source Messaging - 784a9ea4-d2b6-4465-a642-ea40c1f18408.json",
      "sha256": "f2736e7d3a5802d1e78591be6f3c003446d458c22981b6ee3b990962920a91ac"
    },
    {
      "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/input_output_hp_rewriter_10_03_26/inputs/Source Messaging - 784a9ea4-d2b6-4465-a642-ea40c1f18408 (1).json",
      "member": null,
      "sha256": "f2736e7d3a5802d1e78591be6f3c003446d458c22981b6ee3b990962920a91ac"
    }
  ],
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>

<details><summary>Validation record</summary>

```json
{
  "case_id": "22_actual_printer_messi_ink_tank_front_right_medium",
  "path": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging/versions/v2/eval/runs/gpt55_bounded/22_actual_printer_messi_ink_tank_front_right_medium.json",
  "failures": [],
  "observations": [
    {
      "prompt_id": "p1",
      "words": 30,
      "environment": "Office"
    },
    {
      "prompt_id": "p2",
      "words": 33,
      "environment": "Education"
    }
  ],
  "prompt_count": 2,
  "declared_eligible_ksps": 4,
  "used_fallback": false,
  "expected_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  },
  "actual_camera": {
    "requested_tag": "Printer_Front_Right_Medium",
    "resolved_tag": "Printer_Front_Right_Medium",
    "profile_version": "camera-v2-draft-2026-10-22",
    "resolution": "exact",
    "framing": "medium",
    "elevation": "oblique",
    "requested_product": "Messi",
    "resolved_product": "Messi_Ceramic-White.printer.usdz",
    "product_resolution": "alias"
  }
}
```

</details>
