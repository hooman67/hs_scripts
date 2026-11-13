## Generate HTMLs Command for Pipeline (Not Min Inference)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/scripts/generate_html_from_inputs.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/style_prompts_11-08-24_15 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/t2v_for_prompt_styles1.csv --width 1280 --height 720 --num_frames 128 --n_jobs 1
```

* [http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/style\_prompts\_11-08-24\_10/t2v\_intermediate\_2024\_11\_08\_17:06.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/style_prompts_11-08-24_10/t2v_intermediate_2024_11_08_17:06.html)
* [http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/style\_prompts\_11-08-24\_13/t2v\_final\_2024\_11\_10\_08:54.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/style_prompts_11-08-24_13/t2v_final_2024_11_10_08:54.html)
* [http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/style\_prompts\_11-08-24\_15/t2v\_final\_2024\_11\_10\_20:46.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/style_prompts_11-08-24_15/t2v_final_2024_11_10_20:46.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/scripts/generate_html_from_inputs.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/just_prompts_for_style_11-08-24_3 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/styles_just_prompts_rem1.csv --width 1280 --height 720 --num_frames 128 --n_jobs 1
```

* [http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/just\_prompts\_for\_style\_11-08-24/t2v\_intermediate\_2024\_11\_08\_15:01.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/just_prompts_for_style_11-08-24/t2v_intermediate_2024_11_08_15:01.html)
* Re-encoded of above: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_5d241967739b2800e8f5bd660ded390a.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_5d241967739b2800e8f5bd660ded390a.html)
* [http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/just\_prompts\_for\_style\_11-08-24\_2/t2v\_intermediate\_2024\_11\_08\_17:06.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/just_prompts_for_style_11-08-24_2/t2v_intermediate_2024_11_08_17:06.html)

This prompt gets rejected by prompty its detected as none english: `table fan and stand fan green screen animation ,,,,,,,,,,,2d,,1280,720,128,,`

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/scripts/generate_html_from_inputs.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/just_prompts_for_style_ref_decoder_v2_11-20-24_0 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/styles_just_prompts_rem1prompt.csv --width 1280 --height 720 --num_frames 128 --n_jobs 1
```

With the ref-decoder-v2: [http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/just\_prompts\_for\_style\_ref\_decoder\_v2\_11-20-24\_0/t2v\_intermediate\_2024\_11\_10\_09:23.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/just_prompts_for_style_ref_decoder_v2_11-20-24_0/t2v_intermediate_2024_11_10_09:23.html)

Combined style and no style: [http://clio.corp.adobe.com/files/merged\_content\_2024-11-11-19-08-18-adab43493f\_md5\_41c6dae85877c4af72d639ad7fb2da91.html](http://clio.corp.adobe.com/files/merged_content_2024-11-11-19-08-18-adab43493f_md5_41c6dae85877c4af72d639ad7fb2da91.html)

Original videos from ref-decoder-v2 on the style pompts (without style) Vs. same videos re-encoded with CRF at 23 compression: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/ref-decoder-v2-original\_vs\_crf-23\_compression\_md5\_d13af5b0b385391d0845256952b80cd6.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/ref-decoder-v2-original_vs_crf-23_compression_md5_d13af5b0b385391d0845256952b80cd6.html)

You can send debug parameters to the generate\_from\_inputs via command line this: `--debug_params '{"disable_nsfw": true}'`

Used this for 544p generation:

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/scripts/generate_html_from_inputs.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/544p_baseline_bite-reg_11-13-34_1 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/t2v_bytesize_regression.csv --width 1920 --height 1080 --num_frames 128 --n_jobs 4 --limit_prompts 10000
```

`--debug_params '{"disable_nsfw": true}'`

[http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/544p\_baseline\_bite-reg\_11-13-34\_1/t2v\_final\_2024\_11\_13\_15:46.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/544p_baseline_bite-reg_11-13-34_1/t2v_final_2024_11_13_15:46.html)

For camera controls 450:

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/camera_controls_450_11-19-24_1 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/t2v-cameracontrols-450.csv --width 1280 --height 720 --num_frames 128 --n_jobs 5 --limit_prompts 10000
```

For SSEval of GenExtend ref-decoder from main:

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --task "v2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/v2v_bitesized_main91139_11-19-24_2 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_bytesize_regression.csv --width 1280 --height 720 --num_frames 64 --n_jobs 5 --limit_prompts 10000 --debug_params "{'relax_fps': true}"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v2v\_bitesized\_main91139\_11-19-24\_2/v2v\_intermediate\_2024\_11\_19\_18:10.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v2v_bitesized_main91139_11-19-24_2/v2v_intermediate_2024_11_19_18:10.html)

1.  Why videos have other than 20fps. There are 30fps videos there. In prod these will get rejected
2.  Camera controls where wrong in the v2v eval with names that didn't match. And also this is bitesized not supposed to have camera.

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/sannavajjala/dump/v2v\_hshariati\_11202024/v2v\_final\_2024\_11\_20\_14:48.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/sannavajjala/dump/v2v_hshariati_11202024/v2v_final_2024_11_20_14:48.html)

### 540p Model Generation:

**T2V:**

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline540p_982k-ckpt_11-26-2024_2 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/t2v_bytesize_regression.csv --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18
```

* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/baseline540p\_982k-ckpt\_11-26-2024\_2/t2v\_intermediate\_2024\_11\_26\_19:42.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/baseline540p_982k-ckpt_11-26-2024_2/t2v_intermediate_2024_11_26_19:42.html)
* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/baseline540p\_982k-ckpt\_11-26-2024\_2/t2v\_final\_2024\_11\_26\_19:42.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/baseline540p_982k-ckpt_11-26-2024_2/t2v_final_2024_11_26_19:42.html)

**I2V:**

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint http://localhost:8000 --task "i2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/i2v_baseline540p_982k-ckpt_11-26-2024_4 --overwrite --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v/i2v_bytesize_regression.csv --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18
```

* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/i2v\_baseline540p\_982k-ckpt\_11-26-2024\_4/i2v\_intermediate\_2024\_11\_26\_19:48.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/i2v_baseline540p_982k-ckpt_11-26-2024_4/i2v_intermediate_2024_11_26_19:48.html)
* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/i2v\_baseline540p\_982k-ckpt\_11-26-2024\_4/i2v\_final\_2024\_11\_26\_19:48.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/i2v_baseline540p_982k-ckpt_11-26-2024_4/i2v_final_2024_11_26_19:48.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-4096 --overwrite --input_file /sensei-fs/users/mrizve/temp/prompts/morgan_t2v_21_subset.txt --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18 --negative_prompt "cartoon, vector art, & bad aesthetics & poor aesthetic"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-4096/t2v\_intermediate\_2024\_12\_10\_18:08.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-4096/t2v_intermediate_2024_12_10_18:08.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-4400--overwrite --input_file /sensei-fs/users/mrizve/temp/prompts/morgan_t2v_21_subset.txt --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18 --negative_prompt "cartoon, vector art, & bad aesthetics & poor aesthetic"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-4400--overwrite/t2v\_intermediate\_2024\_12\_10\_19:24.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-4400--overwrite/t2v_intermediate_2024_12_10_19:24.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-8160--overwrite --input_file /sensei-fs/users/mrizve/temp/prompts/morgan_t2v_21_subset.txt --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18 --negative_prompt "cartoon, vector art, & bad aesthetics & poor aesthetic"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-8160--overwrite/t2v\_intermediate\_2024\_12\_10\_19:44.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-8160--overwrite/t2v_intermediate_2024_12_10_19:44.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint http://localhost:8000 --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-3520--overwrite --input_file /sensei-fs/users/mrizve/temp/prompts/morgan_t2v_21_subset.txt --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18 --negative_prompt "cartoon, vector art, & bad aesthetics & poor aesthetic"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-3520--overwrite/t2v\_intermediate\_2024\_12\_10\_20:21.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-10-24-pix-cnt-3520--overwrite/t2v_intermediate_2024_12_10_20:21.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-t2v_1 --overwrite --input_file /sensei-fs/users/hshariati/del/clineto/data/clineto_team_test_sets/t2v/t2v_bytesize_regression.csv --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18 --debug_params "{'ssr_type':'ff_light', 'enable_pre_ssr_output':true}"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-t2v\_1/t2v\_intermediate\_2024\_12\_12\_19:13.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-t2v_1/t2v_intermediate_2024_12_12_19:13.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --task "i2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-i2v_1 --overwrite --input_file /sensei-fs/users/hshariati/del/clineto/data/clineto_team_test_sets/i2v/i2v_bytesize_regression.csv --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18 --debug_params "{'ssr_type':'ff_light', 'enable_pre_ssr_output':true}"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-i2v\_1/i2v\_intermediate\_2024\_12\_12\_19:13.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-i2v_1/i2v_intermediate_2024_12_12_19:13.html)

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --task "t2v" --seeds 24 --fix_seeds --save_to /sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-500htq-t2v --overwrite --input_file /sensei-fs/users/hshariati/del/clineto/data/clineto_team_test_sets/t2v/t2v_human_animals_500_1.2.csv --width 1920 --height 1080  --num_frames 128 --n_jobs 1 --limit_prompts 10000 --bit_rate_factor 18 --debug_params "{'ssr_type':'ff_light', 'enable_pre_ssr_output':true}"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-500htq-t2v/t2v\_intermediate\_2024\_12\_12\_19:13.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/12-12-24-988run2-540p-new-ff-ssr-500htq-t2v/t2v_intermediate_2024_12_12_19:13.html)

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/sannavajjala/shared/irina_borisova_king_prompts_formatted.csv --limit_prompts 10000 --task i2v_guided_transform --seeds 24 --negative_prompt "cartoon, vector art, & bad aesthetics & poor aesthetic" --width 1920 --height 1080 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/guided-transform-harmbias-12-13-2024_1" --overwrite --n_jobs 1
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/guided-transform-harmbias-12-13-2024\_1/i2v\_guided\_transform\_intermediate\_2024\_12\_13\_15:42.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/guided-transform-harmbias-12-13-2024_1/i2v_guided_transform_intermediate_2024_12_13_15:42.html)

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint  [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/t2v_bytesize_regression.csv --limit_prompts 10000 --task t2v --seeds 24 --negative_prompt "cartoon, vector art, & bad aesthetics & poor aesthetic" --width 1920 --height 1080 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25" --overwrite --n_jobs 2
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_t2v\_01-16-25/t2v\_final\_2025\_01\_16\_15:38.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25/t2v_final_2025_01_16_15:38.html)

```python
python models/colligo/models/common/asml_generation_utils/viq_scripts/combine_csvs.py --input_csvs "/sensei-fs/users/alse/shared/html/bitesize/2025-01-12/combined/combined.csv,/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25/t2v_final_2025_01_16_15:38.csv" --save_to /sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25/combined/ --caption_column "prompt" --input_video_column "https_video0_ssr" --output_video_columns "prompt1, prompt2, prompt3, prompt4"
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_t2v\_01-16-25/combined/combined\_csvs.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25/combined/combined_csvs.html)

```python
/mnt/localssd/hshariati/colligo/models/colligo/models/common/asml_generation_utils/viq_scripts/reencode_videos.py --input_csv "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25/combined/combined_hs.csv" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25/combined/reenc" --crf 46 --caption_column "prompt" --image_columns "image0,image1" --video_columns "ref-deccoder,fill-in-gap decoder torch,fill-in-gap decoder AOT (and no blending)"
```

**Guided Transform:**

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v_guided_transform/i2v_guidedtransform_bytesize.csv --limit_prompts 10000 --task i2v_guided_transform --seeds 24 --width 1920 --height 1080 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_01-16-25" --overwrite --n_jobs 1 --resume
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_guidedTrans\_01-16-25/i2v\_guided\_transform\_intermediate\_2025\_01\_17\_18:54.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_01-16-25/i2v_guided_transform_intermediate_2025_01_17_18:54.html)

**Horizantal I2V:**

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v/i2v_bytesize_regression.csv --limit_prompts 10000 --task i2v --seeds 24 --width 1920 --height 1080 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_i2v_horiz_01-16-25" --overwrite --n_jobs 1 --resume true
```

* [http://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_i2v\_horiz\_01-16-25/i2v\_intermediate\_2025\_01\_17\_17:46.html](http://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_i2v_horiz_01-16-25/i2v_intermediate_2025_01_17_17:46.html)
* [http://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_i2v\_horiz\_01-16-25/i2v\_intermediate\_2025\_01\_22\_14:09.html](http://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_i2v_horiz_01-16-25/i2v_intermediate_2025_01_22_14:09.html)

**Vertival I2V:**

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v/i2v_bytesize_regression.csv --limit_prompts 10000 --task i2v --seeds 24 --width 1080 --height 1920 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_i2v_vert_01-16-25" --overwrite --n_jobs 1 --resume true
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_i2v\_vert\_01-16-25/i2v\_intermediate\_2025\_01\_17\_17:49.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_i2v_vert_01-16-25/i2v_intermediate_2025_01_17_17:49.html)

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v_guided_transform/i2v_guidedtransform_bytesize.csv --limit_prompts 10000 --task i2v_guided_transform --seeds 24 --width 1920 --height 1080 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-delete" --overwrite --n_jobs 1
```

Cvide\[...\]5BFFP-23567%5Dt2v-baseline%2CFFP-24106-t2v-ref-decoder-v2

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint  [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/) --input_file /sensei-fs/users/lakshya/video_gen/vae_swap/contrib/Mori/collections/genai_foundation/test_data/text_prompts/eval_sentences_master.txt --limit_prompts 10000 --task t2v --seeds 24 --negative_prompt "cartoon, vector art, & bad aesthetics & poor aesthetic" --width 1920 --height 1080 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-26-25_onMasterPrompts" --overwrite --n_jobs 2
```

```python
python models/colligo/models/firefly/pipelines/clineto/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v/i2v_bytesize_regression.csv --limit_prompts 10000 --task i2v --seeds 24 --width 1080 --height 1920 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_i2v_vert_01-16-25" --overwrite --n_jobs 1 --resume true
```

**For v1.8:**

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint  http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/tvid_general_100.csv --limit_prompts 10000 --task t2v --seeds 24 --width 1920  --height 1080 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_dentro_post':false,'enable_dentro_pre': false}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/v1.8_t2v_general-100_01-29-25_2" --overwrite --n_jobs 1 --resume true
```

* [http://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_t2v\_general-100\_01-29-25/t2v\_intermediate\_2025\_01\_29\_18:19.html](http://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_t2v_general-100_01-29-25/t2v_intermediate_2025_01_29_18:19.html)
* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_t2v\_general-100\_01-29-25\_2/t2v\_final\_2025\_01\_29\_18:33.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_t2v_general-100_01-29-25_2/t2v_final_2025_01_29_18:33.html)
* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_t2v\_general-100\_01-29-25\_2/reencoded\_crf37/t2v\_final\_2025\_01\_29\_18:33.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_t2v_general-100_01-29-25_2/reencoded_crf37/t2v_final_2025_01_29_18:33.html)

**Guided transform on new test sets with the old model and fill-in-gap decoder:**

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v_guided_transform/i2v_guidedtrans_general_150-1.csv --limit_prompts 10000 --task i2v_guided_transform --seeds 24 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_general_150_vert-and-hor_01-30-25" --overwrite --n_jobs 1
```

`/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_general_150_vert-and-hor_01-30-25/i2v_guided_transform_final_2025_01_30_18:42.csv`

**Guided transfomr on 540 set:**

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/i2v_guided_transform/i2v_guidedtrans_vertical_540-1.csv --limit_prompts 10000 --task i2v_guided_transform --seeds 24 --num_frames 128 --bit_rate_factor 18 --debug_params "{'enable_pre_ssr_output': true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_general_540_vert_01-31-25" --overwrite --n_jobs 1
```

`/sensei-fs/users/sannavajjala/dump/sursinha-p5-all-i2v-eval/i2v_final_2025_01_29_15:18.csv`
`sensei_video0_ssr` and `image`

`/sensei-fs/users/sannavajjala/dump/p5-all/t2v_final_2025_01_29_14:25.csv`

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/sannavajjala/dump/sursinha-p5-all-t2v-stage/reencoded\_crf37/t2v\_final\_2025\_01\_29\_19:06.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/sannavajjala/dump/sursinha-p5-all-t2v-stage/reencoded_crf37/t2v_final_2025_01_29_19:06.html)

`/sensei-fs/users/sannavajjala/dump/sursinha-p5-all-t2v-stage/t2v_final_2025_01_29_19:06.csv`

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/sannavajjala/dump/sursinha-p5-all-i2v-stage/reencoded\_crf37/i2v\_final\_2025\_01\_30\_10:07.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/sannavajjala/dump/sursinha-p5-all-i2v-stage/reencoded_crf37/i2v_final_2025_01_30_10:07.html)

`/sensei-fs/users/sannavajjala/dump/sursinha-p5-all-i2v-stage/i2v_final_2025_01_30_10:07.csv`

`/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25/combined/combined_hs.csv`

`/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_t2v_01-16-25`

`/sensei-fs/users/hshariati/del/clineto/bhurat/v1-8_vs_prod.csv`

`/sensei-fs/users/hshariati/del/clineto/bhurat/v1-8_vs_prod.html`

`rans_general_540_vert_01-31-25/reencoded_crf37/i2v_guided_transform_final_2025_01_31_15:01.html` to `s3://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_general_540_vert_01-31-25/reencoded_crf37/i2v_guided_transform_final_2025_01_31_15:01.html` without using `--no-sign-request`.
INFO:root:HTML gen results: [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_guidedTrans\_general\_540\_vert\_01-31-25/reencoded\_crf37/i2v\_guided\_transform\_final\_2025\_01\_31\_15:01.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_general_540_vert_01-31-25/reencoded_crf37/i2v_guided_transform_final_2025_01_31_15:01.html)
INFO:root:Reencoded HTML link: [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder\_prod1\_540p-winattn-trt\_guidedTrans\_general\_540\_vert\_01-31-25/reencoded\_crf37/i2v\_guided\_transform\_final\_2025\_01\_31\_15:01.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_general_540_vert_01-31-25/reencoded_crf37/i2v_guided_transform_final_2025_01_31_15:01.html)
INFO:root:Reencoded HTML link saved to: `/sensei-fs/users/hshariati/del/clineto/html/fill-in-gap-decoder_prod1_540p-winattn-trt_guidedTrans_general_540_vert_01-31-25/reencoded_crf37/html.txt`

**Guided transform 540 again:** `--debug_params "{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true}"`

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v_guidedtrans_501_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_guidedtrans_501_03-20-25_5 --overwrite --task i2v_guided_transform --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 2 --debug_params "{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true,'enable_pre_ssr_output':true}"
```

**For Lior MAX model on gen3:**

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/contrib/Mori/collections/genai_foundation/test_data/text_prompts/eval_sentences_gen3.txt --limit_prompts 10000 --task t2v --seeds 24 --num_frames 128 --bit_rate_factor 18 --width 640 --height 360 --debug_params "{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true,'enable_pre_ssr_output':true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/max_release_gen3_data_t2v_06-02-25_3" --overwrite --n_jobs 1
```

```python
python /mnt/localssd/hshariati/colligo/models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file  /mnt/localssd/hshariati/colligo/contrib/Mori/collections/genai_foundation/test_data/text_prompts/eval_sentences_gen3.txt --limit_prompts 10000 --task t2v --seeds 24 --num_frames 128 --bit_rate_factor 18 --width 1280 --height 720 --debug_params "{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true,'enable_pre_ssr_output':true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/max_release_gen3_data_t2v_06-02-25_3" --overwrite --n_jobs 1
```

`/mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/colligo2html.py`

```python
python /mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/colligo2html.py --endpoint http://localhost:8000 --input_file  /mnt/localssd/hshariati/colligo/contrib/Mori/collections/genai_foundation/test_data/text_prompts/eval_sentences_gen3.txt --limit_prompts 10000 --task t2v --seeds 24 --num_frames 128 --bit_rate_factor 18 --width 1280 --height 720 --debug_params "{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true,'enable_pre_ssr_output':true}" --save_to "/sensei-fs/users/hshariati/del/clineto/html/max_release_gen3_data_t2v_06-02-25_5" --overwrite --n_jobs 1
```

**V2V 1.8 460 smoke test for DVA:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general460_v10-decoder_02-28-25_2 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 2 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "ssr_type": "ff_ssr_light_4k_aot", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8\_v2v\_general460\_v10-decoder\_02-28-25\_2/v2v\_intermediate\_2025\_02\_28\_18:39.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general460_v10-decoder_02-28-25_2/v2v_intermediate_2025_02_28_18:39.html)

upload: `../../../../sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general460_v10-decoder_02-28-25_2/reencoded_crf37/v2v_final_2025_02_28_18:39.html` to `s3://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general460_v10-decoder_02-28-25_2/reencoded_crf37/v2v_final_2025_02_28_18:39.html`
INFO:root:HTML gen results: [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8\_v2v\_general460\_v10-decoder\_02-28-25\_2/reencoded\_crf37/v2v\_final\_2025\_02\_28\_18:39.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general460_v10-decoder_02-28-25_2/reencoded_crf37/v2v_final_2025_02_28_18:39.html)
INFO:root:Reencoded HTML link: [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8\_v2v\_general460\_v10-decoder\_02-28-25\_2/reencoded\_crf37/v2v\_final\_2025\_02\_28\_18:39.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general460_v10-decoder_02-28-25_2/reencoded_crf37/v2v_final_2025_02_28_18:39.html)
INFO:root:Reencoded HTML link saved to: `/sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general460_v10-decoder_02-28-25_2/reencoded_crf37/html.txt`

**V2V 1.8 460 smoke test for DVA (01366000):**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_1366k-ckpt_general460_v10-decoder_03-02-25_1 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 2 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

**V2V 1.8 460 smoke test for DVA (01366000) with ref decoder:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_1366k-ckpt_ref-decoder_general460_v10-decoder_03-03-25_1 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_1366k-ckpt_ref-decoder_general460_v10-decoder_03-03-25_1 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

**V2V 1.8 old 100 bitesized:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genextend_general_100.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general100_v10-decoder_02-28-25_5 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 2 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

**V2V 1.8 old 100 bitesized (01366000):**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genextend_general_100.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_1366k-ckpt_general100_v10-decoder_03-02-25_1 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

**V2V 1.8 new 50 4k bitesized:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genextend_general_50_4k.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general50_4k_v10-decoder_02-28-25_2 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 2 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "ssr_type": "ff_ssr_light_4k_aot", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genextend_general_50_4k.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_general50_4k_v10-decoder_02-28-25_5 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 2 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false,"enable_pre_ssr_output":true}'
```

**V2V 1.8 new 50 4k bitesized new ckpt (01366000):**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genextend_general_50_4k.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_1366k-ckpt_general50_4k_v10-decoder_03-02-25_2 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

**V2V 1.8 new 50 4k bitesized new ckpt (01366000) ref decoder:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genextend_general_50_4k.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_1366k-ckpt_general50_4k_ref-decoder_03-02-25_1 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_v2v_1366k-ckpt_ref-decoder_general460_v10-decoder_03-03-25_1 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_v2v_prod1_8_540p_1", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

**T2V Tencent 420, 1080p:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/tencent_t2v-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_t2v_tencent420_v10-decoder_02-28-25_7 --overwrite --task t2v --seeds 24 --width 1920 --height 1080 --num_frames 121 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_t2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8\_t2v\_tencent420\_v10-decoder\_02-28-25\_7/t2v\_intermediate\_2025\_03\_01\_16:33.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8_t2v_tencent420_v10-decoder_02-28-25_7/t2v_intermediate_2025_03_01_16:33.html)

**T2V Tencent 420, UHD:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/t2v/tencent_t2v-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.8_t2v_tencent420_v10-decoder_UHD_02-28-25_3 --overwrite --task t2v --seeds 24 --width 3840 --height 2160 --num_frames 121 --num_jobs 1 --n_jobs 1 --debug_params '{"dit_model_name": "filix2_t2v_prod1_8_540p_1", "decoder_model_name": "dual_vae_pytorch", "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8\_t2v\_tencent420\_v10-decoder\_UHD\_02-28-25\_3/t2v\_intermediate\_2025\_03\_01\_16:57.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.8_t2v_tencent420_v10-decoder_UHD_02-28-25_3/t2v_intermediate_2025_03_01_16:57.html)

[http://s3://adobe-ai-platform-video-checkpoint/checkpoints/downlading0//sensei-fs/projects/firefly/clio/training/logs/zhiwenc/swap\_vae\_v17\_all\_v10\_c25\_genaiaes\_nogenaivid\_genextend\_prod\_variantb\_train/checkpoints/ckpt\_step01366000.pth](http://s3://adobe-ai-platform-video-checkpoint/checkpoints/downlading0//sensei-fs/projects/firefly/clio/training/logs/zhiwenc/swap_vae_v17_all_v10_c25_genaiaes_nogenaivid_genextend_prod_variantb_train/checkpoints/ckpt_step01366000.pth)

**V2V 1.5 460 smoke test for DVA:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_only1080p_for_v1.5.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.5_v2v_general460_v10-decoder_03-02-25_3 --overwrite --task v2v --seeds 24 --num_frames 64 --num_jobs 1 --n_jobs 2 --debug_params '{"relax_fps": true}' --resume true
```

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_only1080p_for_v1.5.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.5_v2v_general460_03-02-25_4 --overwrite --task v2v --seeds 24 --num_frames 64 --num_jobs 1 --n_jobs 1 --debug_params '{"relax_fps": true}'
```

**T2V V1.5 human\_animal\_500:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/users/hshariati/del/t2vid_human_animals_500-1.2_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/1.5_t2v_human-animal-500_03-05-25_1 --overwrite --task t2v --seeds 24 --width 1280 --height 720 --num_frames 128 --num_jobs 1 --n_jobs 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.5\_t2v\_human-animal-500\_03-05-25\_1/t2v\_intermediate\_2025\_03\_05\_20:17.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/1.5_t2v_human-animal-500_03-05-25_1/t2v_intermediate_2025_03_05_20:17.html)

**I2V V1.8 after fix Tencent:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/tencent_i2v-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-i2v_after-fix_03-07-25_1 --overwrite --task i2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_tencent-i2v\_after-fix\_03-07-25\_1/i2v\_intermediate\_2025\_03\_08\_00:11.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-i2v_after-fix_03-07-25_1/i2v_intermediate_2025_03_08_00:11.html)

**T2V V1.8 after fix Tencent:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/users/hshariati/eval_sets/tencent_t2v-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-t2v_after-fix_03-07-25_1 --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_tencent-t2v\_after-fix\_03-07-25\_1/t2v\_intermediate\_2025\_03\_07\_23:38.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-t2v_after-fix_03-07-25_1/t2v_intermediate_2025_03_07_23:38.html)

**V2V V1.8 after fix DVA:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /mnt/localssd/hshariati/colligo/data/test/clio_htmls/videos/clineto_team_test_sets/v2v/v2v_genExtend_general_460-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_dva-v2v_after-fix_03-07-25_1 --overwrite --task v2v --seeds 24 --num_frames 48 --num_jobs 1 --n_jobs 1 --debug_params '{ "relax_fps": true,"enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

**I2V V1.8 after fix Tencent 1376:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/projects/firefly/clineto/evaluation/tencent_i2v/tencent_i2v_horizontal.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-i2v-horizantal_1376ckpt_03-15-25_1 --overwrite --task i2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_tencent-i2v-horizantal\_1376ckpt\_03-15-25\_1/i2v\_intermediate\_2025\_03\_15\_10:07.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-i2v-horizantal_1376ckpt_03-15-25_1/i2v_intermediate_2025_03_15_10:07.html)

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/projects/firefly/clineto/evaluation/tencent_i2v/tencent_i2v_vertical.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-i2v-vertical_1376ckpt_03-15-25_2 --overwrite --task i2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1080 --height 1920 --n_jobs 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_tencent-i2v-vertical\_1376ckpt\_03-15-25\_2/i2v\_intermediate\_2025\_03\_15\_10:30.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_tencent-i2v-vertical_1376ckpt_03-15-25_2/i2v_intermediate_2025_03_15_10:30.html)

```python
python /sensei-fs/users/hshariati/hs_scripts/upload_to_eval_hub.py --csv_paths /sensei-fs/projects/firefly/clineto/autoX/data_log/siddhantg/kaizen-evals-1376k/tencent-t2v-1080p/output.csv --jira FFP-35676 --task t2v --eval_set tencent_t2v --eval_set_version 1.1
```

**H&B V1.8 ckpt1376 t2v\_child\_safety\_harm\_bite\_size\_eval\_set-1.0\_standard.csv:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/users/hshariati/eval_sets/t2v_child_safety_harm_bite_size_eval_set-1.0_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_child_safety_bite_size_1080p_03-18-25_2 --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_t2v\_child\_safety\_bite\_size\_03-18-25\_3/t2v\_intermediate\_2025\_03\_18\_18:22.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_child_safety_bite_size_03-18-25_3/t2v_intermediate_2025_03_18_18:22.html)
* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_t2v\_child\_safety\_bite\_size\_1080p\_03-18-25\_2/t2v\_intermediate\_2025\_03\_19\_16:57.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_child_safety_bite_size_1080p_03-18-25_2/t2v_intermediate_2025_03_19_16:57.html)
* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_t2v\_child\_safety\_bite\_size\_1080p\_03-18-25\_2/t2v\_final\_2025\_03\_19\_16:57.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_child_safety_bite_size_1080p_03-18-25_2/t2v_final_2025_03_19_16:57.html)

**H&B V1.8 ckpt1376 t2v\_human\_animal\_confusion\_harm\_bite\_size\_eval\_set-1.0\_standard.csv:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/users/hshariati/eval_sets/t2v_human_animal_confusion_harm_bite_size_eval_set-1.0_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_human_animal_bite_size_1080p_03-18-25_2 --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_t2v\_human\_animal\_bite\_size\_03-18-25\_1/t2v\_intermediate\_2025\_03\_18\_18:28.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_human_animal_bite_size_03-18-25_1/t2v_intermediate_2025_03_18_18:28.html)
* [https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_t2v\_human\_animal\_bite\_size\_1080p\_03-18-25\_2/t2v\_intermediate\_2025\_03\_19\_16:58.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_human_animal_bite_size_1080p_03-18-25_2/t2v_intermediate_2025_03_19_16:58.html)

**H&B V1.8 ckpt1376 i2v\_animal\_human\_confusion\_harm\_bite\_size\_eval\_set\_standard.csv:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/users/hshariati/eval_sets/i2v_animal_human_confusion_harm_bite_size_eval_set_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_i2v_human_animal_bite_size_03-18-25_5 --overwrite --task i2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_i2v\_human\_animal\_bite\_size\_03-18-25\_5/i2v\_intermediate\_2025\_03\_19\_15:57.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_i2v_human_animal_bite_size_03-18-25_5/i2v_intermediate_2025_03_19_15:57.html)

```python
s3_handle = S3Handle(
    aws_access_key_id="AKIASQRK44BROXTITHNO",
    aws_secret_access_key="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",
    aws_session_token=None,
    unsigned=False,
)
```

Above works for upload to eval hub.
For colligo2html use:

```bash
export AWS_ACCESS_KEY_ID=AKIASQRK44BROXTITHNO
export AWS_SECRET_ACCESS_KEY=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
aws s3 ls s3://clio-web-app/evaluation_service/eval_sets/i2v_animal_human_confusion_harm/data/part1/AdobeStock_583412451.jpeg
```

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v_animal_human_confusion_harm_bite_size_eval_set_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_i2v_human_animal_bite_size_03-18-25_5 --overwrite --task i2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}' --resume true
```

**H&B V1.8 ckpt1376 i2v\_child\_safety\_harm\_bite\_size\_eval\_set\_standard.csv:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net) --input_file /sensei-fs/users/hshariati/eval_sets/i2v_child_safety_harm_bite_size_eval_set_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_i2v_child_safety_bite_size_03-18-25_5 --overwrite --task i2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_i2v\_child\_safety\_bite\_size\_03-18-25\_5/i2v\_intermediate\_2025\_03\_19\_16:03.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_i2v_child_safety_bite_size_03-18-25_5/i2v_intermediate_2025_03_19_16:03.html)

**Guided Transform 501 for sci**

**Guided transform 540 again:**

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v_guidedtrans_501_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_guidedtrans_501_03-20-25_5 --overwrite --task i2v_guided_transform --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

`/sensei-fs/projects/firefly/clineto/autoX/data_log/sannavajjala/v1p8-ckpt-1344vs1368/ckpt_1368000/1080p_bytesize_vertical/job_0/video_eval_bytesized/03-03-2025_19-49-49/video_eval_bytesized.csv`

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v_guidedtrans_501_standard.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_guidedtrans_501_03-20-25_5 --overwrite --task i2v_guided_transform --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}' --resume --resume_from_csv /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_guidedtrans_501_03-20-25_5/
```

[https://clio.corp.adobe.com/model\_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8\_1376ckpt\_guidedtrans\_501\_03-20-25\_5/i2v\_guided\_transform\_intermediate\_2025\_03\_25\_15:35.html](https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_guidedtrans_501_03-20-25_5/i2v_guided_transform_intermediate_2025_03_25_15:35.html)

```python
python /sensei-fs/users/hshariati/hs_scripts/upload_to_eval_hub.py --task i2v --jira FFP-36891 --csv_paths /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_guidedtrans_501_03-20-25_5/i2v_guided_transform_final_2025_03_25_15:35.csv --eval_set i2v_guidedtrans_501 --eval_set_version 1.0 --link_to_eval true
```

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/morgan_prompts.txt --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_morgan_prompts_03-28-25_2 --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```


## I2V V1.8 ckpt 1376 one more time on tencent eval set but making sure we actually crop the heads with optimizations
```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/tencent_i2v-1.0_standardized.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_i2v_tencent_256_04-07-25_2 --overwrite --task i2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```
https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_i2v_tencent_256_04-07-25_2/i2v_intermediate_2025_04_07_18:18.html


## t2V V1.8 ckpt 1376 with optimizations on bitesize 100 1080p
```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/t2vid_general_100.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_bitesize_420_04-07-25_1 --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_bitesize_420_04-07-25_1/t2v_intermediate_2025_04_07_18:31.html


## t2V V1.8 ckpt 1376 with optimizations on bitesize 100 540p
```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/t2vid_general_100.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_bitesize_100_540p_04-08-25_1 --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 960 --height 540 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```


## t2V V1.8 ckpt 1376 with NO optimizations on bitesize 100 540p
```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/t2vid_general_100.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_t2v_bitesize_100_540p_noOpt_04-08-25_1 --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 960 --height 540 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

## tv structure match
```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/structure_match_tv/v2v_transformVideo_311.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_tv_bitesize_1080p_04-09-25_5 --overwrite --task structure_match --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'
```

# Generating assets from Fal ai
pip install fal-client
export FAL_KEY="530ec3e1-db84-4ff7-852c-09387cafae14:762468a73f52bc85c086b40483746537"
python /sensei-fs/users/hshariati/hs_scripts/fal_video_generator.py --input prompts.txt --output videos/ --api "fal-ai/kling-video/v1.5/pro/text-to-video"
Upload to eval hub using:
python fal_competitor_upload_to_eval_hub.py --task t2v --video_folder /sensei-fs/users/hshariati/del/clineto/fal_competitor_generations/veo2_physics_04-11-25 --prompt_file /sensei-fs/users/hshariati/eval_sets/t2v/physics_first_draft.txt --jira FFP-37517-veo2 --eval_set physics --eval_set_version 0.0 --link_to_eval false

## for veo2
python /sensei-fs/users/hshariati/hs_scripts/fal_video_generator.py --input /sensei-fs/users/hshariati/eval_sets/t2v/physics_first_draft.txt --output /sensei-fs/users/hshariati/del/clineto/fal_competitor_generations/veo2_physics_04-11-25 --api "fal-ai/veo2"

python /sensei-fs/users/hshariati/hs_scripts/fal_video_generator.py --input /sensei-fs/users/hshariati/eval_sets/t2v/motion_first_draft.txt --output /sensei-fs/users/hshariati/del/clineto/fal_competitor_generations/veo2_motion_04-11-25 --api "fal-ai/veo2"

python fal_competitor_upload_to_eval_hub.py --task t2v --video_folder /path/to/videos --prompt_file /path/to/prompts.txt --jira FFP-37517-veo2 --eval_set physics --eval_set_version 0.0 --link_to_eval false

## for wlan2.1
python /sensei-fs/users/hshariati/hs_scripts/fal_video_generator.py --input /sensei-fs/users/hshariati/eval_sets/t2v/physics_first_draft.txt --output /sensei-fs/users/hshariati/del/clineto/fal_competitor_generations/wan2.1_physics_04-11-25 --api "fal-ai/wan-t2v"

python /sensei-fs/users/hshariati/hs_scripts/fal_video_generator.py --input /sensei-fs/users/hshariati/eval_sets/t2v/motion_first_draft.txt --output /sensei-fs/users/hshariati/del/clineto/fal_competitor_generations/wan2.1_motion_04-11-25 --api "fal-ai/wan-t2v"

**T2V Physics First Draft:**

### This generation uses v1.8 model to evaluate physics prompts at 1080p resolution.

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/physics_first_draft.txt --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_prod_t2v_physics_1080p_04-25-24 --overwrite --width 1920 --height 1080 --n_jobs 1 --seeds 24 --limit_prompts 1000000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}"
```

**T2V Motion First Draft:**

### This generation uses v1.8 model to evaluate motion prompts at 1080p resolution.

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/motion_first_draft.txt --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_prod_t2v_motion_1080p_04-25-24 --overwrite --width 1920 --height 1080 --n_jobs 1 --seeds 24 --limit_prompts 1000000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}"
```


### This generation uses v1.9 model to evaluate physics prompts at 720p resolution.
From this ckpt: s3://adobe-ai-platform-video-checkpoint/training_logs//sensei-fs/projects/firefly/clio/training/logs/kpnvr/kpnvr-qt-v2/checkpoints/ckpt_step01392000.pth/

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/physics_first_draft.txt --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.9_1392ckpt_prod_t2v_physics_720p_04-25-24_1 --overwrite --width 1280 --height 720 --n_jobs 1 --seeds 24 --limit_prompts 1000000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}"
```

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.9_1392ckpt_prod_t2v_physics_720p_04-25-24_1/t2v_intermediate_2025_04_14_17:46.html

### This generation uses v1.9 model to evaluate motion prompts at 720p resolution.
From this ckpt: s3://adobe-ai-platform-video-checkpoint/training_logs//sensei-fs/projects/firefly/clio/training/logs/kpnvr/kpnvr-qt-v2/checkpoints/ckpt_step01392000.pth/

```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/motion_first_draft.txt --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.9_1392ckpt_prod_t2v_motion_720p_04-25-24_2 --overwrite --width 1280 --height 720 --n_jobs 1 --seeds 24 --limit_prompts 1000000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}"
```

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1.9_1392ckpt_prod_t2v_motion_720p_04-25-24_2/t2v_intermediate_2025_04_14_18:06.html


### V1.8 prod, tencent_i2v with the inifinite aspect ratio infinate dimensions fix
```python
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/tencent_i2v-1.0_standardized.csv --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_prodckpt_tencent_i2v_imageDimension_04-24-25_1 --overwrite --width 1920 --height 1080 --n_jobs 1 --seeds 24 --limit_prompts 1000000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --initiative "test_init" --experiment "test_exp" --ckpt "1376k"
```

### L2 Teacher V1.9 T2V on taxonomy
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/siddhantg/dumps/v1p9_evals_2025_apr/datasets/t2v_SFT_Taxonomy_Prompts_80_Horizontal_Only.csv --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_1389k_t2v_taxonomy_1080p_04-25-25_4 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 180 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-ckpt-compare --ckpt 1389k --commit-hash 3bc6e938a3b660128a1b72ed7a26edc349867552 --initiative clineto --num_frames 121

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_1389k_t2v_taxonomy_1080p_04-25-25_4/t2v_intermediate_2025_05_13_00:04.html

### L2 Teacher V1.9 I2V on taxonomy
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py \
  --endpoint http://localhost:8000 \
  --input_file /sensei-fs/users/siddhantg/dumps/v1p9_evals_2025_apr/datasets/i2v_SFT_ImagetoVideo_16_9_aspectRatio_66.csv \
  --task i2v \
  --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_1389k_i2v_16x9_1080p_04-25-25_4 \
  --overwrite \
  --n_jobs 1 \
  --seeds 24 \
  --limit_prompts 166 \
  --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-ckpt-compare --ckpt 1389k --commit-hash 3bc6e938a3b660128a1b72ed7a26edc349867552 --initiative clineto --num_frames 121


https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_1389k_i2v_16x9_1080p_04-25-25_4/i2v_intermediate_2025_05_13_00:05.html


### L1 Student V1.9 T2V on tencent 1080p
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/t2v/tencent_t2v-1.0_standardized.csv --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l1_student_1389k_t2v_tencent_1080p_05-13-25_2 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-ckpt-compare --ckpt 1389k_student --commit-hash 8142e9e18da3d173015bdb031f605d2574dc9f7c --initiative clineto --num_frames 121 --width 1920 --height 1080

### L1 Student V1.9 I2V on tencent 1080p
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/tencent_i2v-1.0_standardized.csv --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l1_student_1389k_i2v_tencent_1080p_05-13-25_3 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-ckpt-compare --ckpt 1389k_student --commit-hash 8142e9e18da3d173015bdb031f605d2574dc9f7c --initiative clineto --num_frames 121 --width 1920 --height 1080




### new L2 teacher on taxonomy t2v
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/siddhantg/dumps/v1p9_evals_2025_apr/datasets/t2v_SFT_Taxonomy_Prompts_80_Horizontal_Only.csv --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_teacher__139k_t2v_taxonomy_t2v_05-15-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-ckpt-compare --ckpt 1389k_student --commit-hash f216ee2a8f7ed78bed905ff9f83af4376fc8158d --initiative clineto --num_frames 121


### new L2 teacher on taxonomy i2v
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/siddhantg/dumps/v1p9_evals_2025_apr/datasets/i2v_SFT_ImagetoVideo_16_9_aspectRatio_66.csv --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_teacher__139k_t2v_taxonomy_i2v_05-15-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-ckpt-compare --ckpt 1389k_student --commit-hash f216ee2a8f7ed78bed905ff9f83af4376fc8158d --initiative clineto --num_frames 121



### testing slowing down fast motion videos
#### BAseline L2 student
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_ORIG_05-22-25_2 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_ORIG_05-22-25_2/i2v_intermediate_2025_05_22_17:53.html


#### L2 student Simple drop at 7
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_all_,keyFrames_dropAt7_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080



#### L2 student Forward noise added drop at 7
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_all_keyFrames_forwardNoiseSchedule_dropAt7_05-22-25_4 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080


#### L2 student Reverse noise added drop at 7
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_all_keyFrames_reverseNoiseSchedule_dropAt7_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080


#### L2 student SPG implementation spg_weight=0.3 with spg_blur_kernel=5
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp3_spg-bur5_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080


#### SPG implementation spg_weight=0.3 with spg_blur_kernel=3
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp3_spg-bur3_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

#### L2 student SPG implementation spg_weight=0.3 with spg_blur_kernel=7
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp3_spg-bur7_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080


#### L2 student SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule = lambda t: 0.5 * (1.0 - t)

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-schedule_spg-bur3_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080


#### L2 student SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule4 = lambda t: 0.3 * (1.0 - t)

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-scheduleAt3_spg-bur5_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-scheduleAt3_spg-bur5_05-22-25_1/i2v_intermediate_2025_05_30_21:26.html

#### L2 student SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule = lambda t: 0.5 * (t)

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-scheduleReverse_spg-bur3_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-scheduleReverse_spg-bur3_05-22-25_1/i2v_intermediate_2025_05_30_20:39.html


#### L2 student SPG implementation spg_weight=schdule with spg_blur_kernel=5 spg_schedule3 = lambda i: 0.5 if i <= 10 else 0.0 

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-first10Only_spg-bur5_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-first10Only_spg-bur5_05-22-25_1/i2v_intermediate_2025_05_30_20:51.html

#### L2 student SPG implementation spg_weight=schdule with spg_blur_kernel=5 spg_schedule4 = lambda i: 0.5 if i >= 15 else 0.0

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-last10OnlyAtP5_spg-bur5_05-22-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-last10OnlyAtP5_spg-bur5_05-22-25_1/i2v_intermediate_2025_05_30_21:28.html



#### L2 student SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule6 = lambda t, i: 0.5 * (1.0 - t) if i <= 10 else 0.0

###### ***Best for student so far it seems

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-scheduleAt5First10_spg-bur5_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_spg-wp-scheduleAt5First10_spg-bur5_05-30-25_1/i2v_intermediate_2025_05_30_22:02.html

#### L2 teacher baseline

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_teacher__1394k_i2v_fast_motion_ORIG_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_teacher__1394k_i2v_fast_motion_ORIG_05-30-25_1/i2v_intermediate_2025_05_30_21:03.html


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule = lambda t: 0.5 * (1.0 - t)

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-wp-scheduleAtP5_spg-bur5_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-wp-scheduleAtP5_spg-bur5_05-30-25_1/i2v_intermediate_2025_05_30_21:39.html


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule = lambda t: 0.5 * (1.0 - t) but with     spg_enhanced: bool = True,  spg_bad_model: bool = False, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP5_spg-bur5_spgEnhancedOn_spgBadModelOff_05-30-25_2 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP5_spg-bur5_spgEnhancedOn_spgBadModelOff_05-30-25_2/i2v_intermediate_2025_05_31_00:33.html


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule = lambda t: 0.5 * (1.0 - t) but with     spg_enhanced: bool = True,  spg_bad_model: bool = True, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP5_spg-bur5_spgEnhancedOn_spgBadModelOn_05-30-25_2 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP5_spg-bur5_spgEnhancedOn_spgBadModelOn_05-30-25_2/i2v_intermediate_2025_05_31_01:25.html

###### doesn't do anything


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule = lambda t: 0.8 * (1.0 - t) but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP8_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP8_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_05_30_23:33.html


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule7 = lambda t, i: 0.8 * (1.0 - t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP8OnlyFirst10_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP8OnlyFirst10_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_05_31_00:46.html


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_early_strong = lambda t: 1.2 if t > 0.7 else 0.3 * (1.0 - t)       but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1P2OnlyFirstP7_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_2 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1P2OnlyFirstP7_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_2/i2v_intermediate_2025_05_31_01:27.html

###### major artifacts. Too much


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=5    spg_schedule7 = lambda t, i: 1.2 * (1.0 - t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1P2OnlyFirst10_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1P2OnlyFirst10_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_05_31_01:59.html


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=11    spg_schedule7 = lambda t, i: 1.2 * (1.0 - t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1P2OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1P2OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_05_31_02:13.html


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=11    spg_schedule7 = lambda t, i: 3.2 * (1.0 - t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,

python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt3P2OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt3P2OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_05_31_02:43.html








#### Combined L2 student showing SPG, and other methods
https://clio.corp.adobe.com/files/7512ae68-5125-47b5-b98f-493892f1085d_md5_385ce977c1979d655ad86fe5e09f23a2.html


#### Combined L2 student showing different SPG experiments
https://clio.corp.adobe.com/files/36ef533e-8d38-4bf4-9378-d1b2593ff2db_md5_62cf4775d53ab015b99b423c063803b1.html

l2-student-baseline,spg-wp-scheduleAt5First10_spg-bur5,spg-wp3_spg-bur3,spg-wp3_spg-bur5,spg-wp3_spg-bur7,spg-wp-scheduleAt3_spg-bur5,spg-wp-scheduleAt5_spg-bur5,spg-wp-last10OnlyAtP5_spg-bur5,spg-wp-first10Only_spg-bur5,spg-wp-scheduleAt5Reverse_spg-bur5

Just showing the best results:
https://clio.corp.adobe.com/files/b4894200-7778-477b-adb9-ec7b947e8117_md5_385a69b419da55023b7eea1f59856b53.html


#### Combined L2 Teachers showing different SPG experiments
https://clio.corp.adobe.com/files/756acdde-225b-4c40-acdc-621ce72a2e66_md5_8fd9c35a8c187a143b8749a1d98e0913.html

l2_teacher_baseline,l2Teacher_spg-wp-scheduleAtP5_spg-bur5_spgEnhancedOff_spgBadModelOff,l2Teacher_spg-scheduleAtP5_spg-bur5_spgEnhancedOn_spgBadModelOff,l2Teacher_spg-scheduleAtP5_spg-bur5_spgEnhancedOn_spgBadModelOn,l2Teacher_spg-scheduleAt1P2OnlyFirstP7_spg-bur5_spgEnhancedOff_spgBadModelOff,l2Teacher_spg-scheduleAt1P2OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff,l2Teacher_spg-scheduleAtP8_spg-bur5_spgEnhancedOff_spgBadModelOff,l2Teacher_spg-scheduleAt1P2OnlyFirst10_spg-bur5_spgEnhancedOff_spgBadModelOff,l2Teacher_spg-scheduleAtP8OnlyFirst10_spg-bur5_spgEnhancedOff_spgBadModelOff,l2Teacher_spg-scheduleAt3P2OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff

Just showing the best results:
https://clio.corp.adobe.com/files/508a7ec5-03e9-4d20-b1b1-6ebf983232f9_md5_fab2038a77611ffac4251d4e297d46fe.html



#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=11    spg_schedule7 = lambda t, i: 10 * (1.0 - t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt10OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt10OnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_06_03_11:24.html

##### Still no differences


#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=11    spg_schedule9 = lambda t, i: 1.2 * (t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1p2ReverseOnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt1p2ReverseOnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_06_03_12:00.html

##### finally this shows some differences. However, there is an artifact. 




#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=11    0.5 * (t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt0p5ReverseOnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt0p5ReverseOnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_06_03_15:47.html



#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=11    0.8 * (t) if i <= 10 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt0p8ReverseOnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt0p8ReverseOnlyFirst10_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_06_03_17:11.html

#### L2 teacher SPG implementation spg_weight=schdule with spg_blur_kernel=11    0.8 * (t) if i <= 15 else 0.0      but with     spg_enhanced: bool = False,  spg_bad_model: bool = False, spg_skip_layers: bool = False,
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint http://localhost:8000 --input_file /sensei-fs/users/hshariati/eval_sets/i2v/too_fast_videos.txt --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt0p8ReverseOnlyFirst15_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1800 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-slow-down-videos --ckpt 13894k_student --commit-hash ab1e8d5f0524c67e351c64046003fa926c14cf0e --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAt0p8ReverseOnlyFirst15_spg-bur11_spgEnhancedOff_spgBadModelOff_05-30-25_1/i2v_intermediate_2025_06_03_17:12.html










### L2 Student (final deployed one) V1.9 I2V on taxonomy Final L2 review
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://load-test-video-v1-dev.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/siddhantg/dumps/v1p9_evals_2025_apr/datasets/i2v_SFT_ImagetoVideo_16_9_aspectRatio_66.csv --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_l2_approval_i2v_06-6-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-student-l2-approval --ckpt 1394k-2 --commit-hash d56f118baaf1c0fce1b68fe17e4cf394ae017aab --initiative clineto --num_frames 121

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_l2_approval_i2v_06-6-25_1/i2v_intermediate_2025_06_06_17:12.html

### L2 Student (final deployed one) V1.9 T2V on taxonomy Final L2 review
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://load-test-video-v1-dev.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/siddhantg/dumps/v1p9_evals_2025_apr/datasets/t2v_SFT_Taxonomy_Prompts_80_Horizontal_Only.csv --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_l2_approval_t2v_06-6-25_1 --overwrite --n_jobs 18 --seeds 24 --limit_prompts 1000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-student-l2-approval --ckpt 1394k-1 --commit-hash d56f118baaf1c0fce1b68fe17e4cf394ae017aab --initiative clineto --num_frames 121

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_l2_approval_t2v_06-6-25_1/t2v_intermediate_2025_06_06_17:19.html





### L2 Student (final deployed one) V1.9 I2V on tencent Final sseval (with opt)
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://load-test-video-v1-dev.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/hshariati/eval_sets/i2v/tencent_i2v-1.0_standardized.csv --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_tencent_i2v_06-6-25_1 --overwrite --n_jobs 1 --seeds 24 --limit_prompts 1000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-student-l2-approval --ckpt 1394k-2 --commit-hash d56f118baaf1c0fce1b68fe17e4cf394ae017aab --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_tencent_i2v_06-6-25_1/i2v_intermediate_2025_06_06_18:00.html


### L2 Student (final deployed one) V1.9 T2V on tencent Final sseval (with opt)
python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://load-test-video-v1-dev.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/hshariati/eval_sets/t2v/tencent_t2v-1.0_standardized.csv --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_tencent_t2v_06-6-25_1 --overwrite --n_jobs 18 --seeds 24 --limit_prompts 1000 --debug_params "{'enable_pre_ssr_output': false, 'enable_dentro_post': false, 'enable_video_nsfw_only': false, 'disable_nsfw': true, 'enable_dentro': false, 'enable_dentro_pre': false}" --experiment v1p9-student-l2-approval --ckpt 1394k-1 --commit-hash d56f118baaf1c0fce1b68fe17e4cf394ae017aab --initiative clineto --num_frames 121 --width 1920 --height 1080

https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_student_final_tencent_t2v_06-6-25_1/t2v_intermediate_2025_06_06_22:35.html


### Qwen 2.5 7b captions on audio data:
fe77157


python -m glimmer.inference --config /mnt/localssd/genie/glimmer/modules/qwen2dot5_structured_captions/video_config.yaml --gpus 2 --test-mode

glim create --table /mnt/localssd/genie/glimmer/modules/qwen2dot5_structured_captions/video_config.yaml --job-name hshariati-glim-video-captions-for-audio --row-group-size 256

glim stats --job-name hshariati-glim-video-captions-for-audio


