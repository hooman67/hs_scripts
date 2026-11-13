# Minimal Inference HTML Generator

- Use this module to get HTMLs from any minimal inference pipeline. 
- Currently supoorted pipelines are
    - [x] Text to Video
    - [x] Video to Video
    - [x] Image to Video
- RefSSR and SSR are not supported in html generation yet. They will be soon.

## Running minimal inference html generator

```
python minimal_inference_html.py \
--task <task> # t2v, v2v, i2v \
--prompt_file <path_to_input.txt> \
--save_to <unique_folder_path> \
--width_latent 80 \ 
--height_latent 44 \
--num_frames 128 \
--n_channels 12 \

```

or Add the following to your `launch.json`

```
    {
        "name": "---------[Minimal Inference HTML Generator]--------- "
    },
    {
        "name": "Minimal Inference HTML",
        "type": "debugpy",
        "request": "launch",
        "module": "minimal_inference_html",
        "console": "integratedTerminal",

        "cwd": "${workspaceFolder}/models/colligo/models/firefly/minimal_inference/html_generation/",
        "args": [
            "--prompt_file", "/sensei-fs/users/sannavajjala/filix2/i2v/eval_sentences_i2v.txt", // Replace with your text prompts file
            "--save_to", "/sensei-fs/users/sannavajjala/minimal_inference/html_gen_i2v", // Replace with your location to store outputs
            "--task", "i2v",
            "--width_latent", "80",
            "--height_latent", "44",
            "--num_frames", "20", // Modify to change the duration of output video. Should be a multiple of 5
        ],
    },
```