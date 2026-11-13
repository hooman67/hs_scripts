# Minimal Inference: SSR

<strong><span style="color:red;">WARNING: </span></strong> Minimal Inference SSR only works with torch-2.1.0 for now

## Prerequisites
* Please read the minimal inference README at [../README.md](../aidoc/index.md) and documentation on the [Wiki](https://wiki.corp.adobe.com/display/GenAI/Minimal+Inference) before continuing further
* Make sure that you have a working colligo setup by running 
    * `./m sys.check` - To check the installation
    * `source m` - To check if env loads
    * `./m deps.sync` - To update the environment with packages

IMPORTANT NOTE: Minimal Inference SSR only works with torch=2.1.0 at the moment (we're working on fixing it to support 2.3.1)

## SSR Minimal Inference

### Single invocation / Adhoc run

1. Activate the torch-2.1.0 environment by running `source .venvs/torch-2.1.0/bin/activate`
2. Run minimal inference by running `python minimal_ssr.py --input_video </path/to/input/lowres/video.mp4> --output_path </path/to/output/highres/video.mp4>`

### HTML Generation

* To create an html with video to video results, use the script `minimal_ssr.py` - It uses `minimal_ssr_html.py` for single generations. Run the following command

```
python minimal_ssr_html.py \
--input_file "</path/to/ref/ssr/prompts.txt>"  \
--save_to "</path/to/save/output/folder/>" \
--html_filename "<name_of_html.html>"
```

## Run & Debug

* Alternatively, you can run adhoc minimal inference (`minimal_ssr.py`) and HTML minimal inference (`minimal_ssr_html.py`) by choosing the appropriate section in `colligo/.vscode/launch.json`
* You will find Minimal Inference HTML generation under "----- HTML Generation -----" and single execution minimal inference under "----- Minimal Inference -----"

