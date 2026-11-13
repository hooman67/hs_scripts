# Minimal Inference: Text to Video

## Prerequisites
* Please read the minimal inference README at [../README.md](../aidoc/index.md) and documentation on the [Wiki](https://wiki.corp.adobe.com/display/GenAI/Minimal+Inference) before continuing further
* Make sure that you have a working colligo setup by running 
    * `./m sys.check` - To check the installation
    * `source m` - To check if env loads
    * `./m deps.sync` - To update the environment with packages

## Text to Video Minimal Inference

### Single invocation / Adhoc run

* To run text to video minimal inference on a single or a handful of inputs, run the `minimal_t2v.py` script. An example script is provided below for guidance

```
python minimal_t2v.py \
--prompt "A person standing on the side of a busy road in Tokyo" \
--width_latent 80 \
--height_latent 44 \
--num_frames 20 \
--n_channels 12 \
--save_to "</path/to/video.mp4>"
```

### HTML Generation
<!-- * For HTML generation check [../html_generation](../html_generation/aidoc/index.md) README.md page -->

## Run & Debug
* Alternatively, you can run adhoc minimal inference (`minimal_t2v.py`) and HTML minimal inference (`minimal_inference_html.py`) by choosing the appropriate section in `colligo/.vscode/launch.json`
* You will find Minimal Inference HTML generation under "----- HTML Generation -----" and single execution minimal inference under "----- Minimal Inference -----"


Re-use the following `launch.json` snippet if needed. Change the `--task`, `--save_to` and `--prompt_file` parameters per your need
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
            "--prompt_file", "/sensei-fs/users/sannavajjala/filix2/colligo2html/t2v/prompts.txt", // Replace with your text prompts file
            "--save_to", "/sensei-fs/users/sannavajjala/minimal_inference/html_gen_t2v", // Replace with your location to store outputs
            "--task", "t2v",
            "--width_latent", "80",
            "--height_latent", "44",
            "--num_frames", "20", // Modify to change the duration of output video. Should be a multiple of 5
        ],
    },
```

## [Model Developers] Contributing T2V models to Colligo via Minimal Inference T2V

Follow the recommendations below to contribute your models to the Colligo pipeline via Minimal Inference

*Goal*: As a researcher, we'd like you to give us a working minimal inference script with your custom changes. That's it. Once you have a working minimal inference script with custom code, the integration team will use your changes (from your PR) to integrate models into the production pipeline

*Parity*: Minimal inference is a minimal version of the production pipeline. The results you are able to get using minimal inference will match the results in the production pipeline

### Contribution guidelines
- Minimal Inference has multiple moving parts. In the case of T2V these would be the text encoder, DiT model, decoder
- In the file `minimal_t2v_local.py` we provide a code example of adding a DiT model to minimal inference (while keeping other models unchanged)
    - Notice how only the DiT logic is changed while keeping the decoder unchanged (because the user's goal is to change the DiT model while reusing an existing decoder)
 