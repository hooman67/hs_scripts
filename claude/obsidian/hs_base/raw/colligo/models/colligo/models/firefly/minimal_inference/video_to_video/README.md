# Minimal Inference: Video to Video

## Prerequisites
* Please read the minimal inference README at [../README.md](../aidoc/index.md) and documentation on the [Wiki](https://wiki.corp.adobe.com/display/GenAI/Minimal+Inference) before continuing further
* Make sure that you have a working colligo setup by running 
    * `./m sys.check` - To check the installation
    * `source m` - To check if env loads
    * `./m deps.sync` - To update the environment with packages

## Video to Video Minimal Inference

### Single invocation / Adhoc run

* To run video to video minimal inference on a single or a handful of inputs, run the `minimal_v2v.py` script. An example script is provided below for guidance

```
python minimal_v2v.py \
--video_path "/sensei-fs/users/sannavajjala/minimal_inference/row_2_col_0.mp4" \
--width_latent 80 \
--height_latent 44 \
--num_frames 20 \
--n_channels 12 \
--save_to "</path/to/video.mp4>"
```

### HTML Generation
<!-- * For HTML generation check [../html_generation](../html_generation/aidoc/index.md) README.md page -->




## Run & Debug

* Alternatively, you can run adhoc minimal inference (`minimal_v2v.py`) and HTML minimal inference (`minimal_inference_html.py`) by choosing the appropriate section in `colligo/.vscode/launch.json`

* Re-use the following `launch.json` snippet if needed. Change the `--task`, `--save_to` and `--prompt_file` parameters per your need
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

