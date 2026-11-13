import argparse
import json
import os
import subprocess
import time
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
from PIL import Image
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm
import imageio.v3 as iio

from clio.prototyping_tools.aws_util import S3Handle
from clio.prototyping_tools.html.viz import HTML

import sys

sys.path.append(os.path.join(sys.path[0], "scripts/clineto"))
print(sys.path)

# sys.exit()


def check_s3_access(bucket_name):
    s3_handle = S3Handle(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", None),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", None),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN", None),
    )
    return s3_handle.has_access_to_bucket(bucket_name=bucket_name)


def upload_dir_to_s3(save_to, return_file_path, modelname=None, overwrite=False):
    BUCKET_NAME = "clio.corp.adobe.com"
    upload_dir_path = Path(save_to)

    s3_handle = S3Handle(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", None),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", None),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN", None),
    )
    if not s3_handle.has_access_to_bucket(bucket_name=BUCKET_NAME):
        print("No access to s3 to upload")
        return

    s3_handle.upload_dir(
        dir_path=upload_dir_path,
        bucket=BUCKET_NAME,
        s3_key_prefix="model_evaluation",
        overwrite=overwrite,
    )
    html_title = save_to.split("/")[-1] if modelname is None else modelname
    html_url = f"http://clio.corp.adobe.com/model_evaluation/{save_to}/{html_title}.html"
    print(f"Results available at: {html_url}")
    if return_file_path is not None:
        with open(return_file_path, "w") as file:
            file.write(html_url)


def get_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[404, 429, 500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def read_inputs(prompt_input_path: Path, limit_prompts: int) -> tuple[list[str], list[str | None]]:
    prompt_attributes: list[str | None] = []
    input_prompts = []

    if not os.path.exists(prompt_input_path):
        err_str = f"{prompt_input_path} is not a valid input file path."
        raise RuntimeError(err_str)

    with open(prompt_input_path) as f:
        prompts = f.readlines()[:limit_prompts]

    for prompt in prompts:
        if "|" in prompt:
            prompt, attrs = prompt.split("|")
            if "ctype" in attrs:
                content_class = attrs.split(":")[1].strip()
                # NOTE the ctype `illustration -> art`` and `vector` -> None transformation should be done within the given input prompt file
                prompt_attributes.append(content_class)
            elif "exif" in attrs:
                photo_settings = attrs.split(":")[1].strip()
                prompt_attributes.append(
                    photo_settings
                )  # TODO fix this - this actually does not work in the current script...
            else:
                content_class = attrs.strip()
                # NOTE the ctype `illustration -> art`` and `vector` -> None transformation should be done within the given input prompt file
                prompt_attributes.append(content_class)
        else:
            prompt_attributes.append(None)

        input_prompts.append(prompt.strip())
    return input_prompts, prompt_attributes


def list_of_ints(string: str) -> list[int]:
    try:
        return [int(x.strip()) for x in string.split(",")]
    except ValueError:
        exception_str = f"Invalid list of integers: {string}"
        raise argparse.ArgumentTypeError(exception_str)


def parse_arguments() -> argparse.Namespace:
    # Parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--endpoint",
        type=str,
        default="http://localhost:8000/v2/images/generate",
        help="Colligo endpoint URL",
    )

    parser.add_argument(
        "--seeds",
        type=list_of_ints,
        default="333",
        help="Seeds to pass in Colligo request",
    )

    parser.add_argument(
        "--save_to",
        type=str,
        required=True,
        help="save to location",
    )

    parser.add_argument(
        "--return_file_path",
        type=str,
        default=None,
        help="save to location for s3 html url",
    )

    parser.add_argument(
        "--text_prompt_file",
        type=str,
        default=None,
        help="Text prompt file for generations",
    )

    parser.add_argument(
        "--limit_prompts",
        type=int,
        default=None,
        help="Limit to the first N prompts of the text file",
    )

    parser.add_argument(
        "--avoid_prompt",
        type=str,
        default="art, illustration, vector, bad quality, low quality, dull, ugly, cartoon, icon, logo, cover, disfigured, deformed, worst quality, lowres, ",
        help="The avoid prompt being used",
    )

    parser.add_argument(
        "--width",
        type=int,
        required=True,
        help="The output width",
    )
    parser.add_argument(
        "--height",
        type=int,
        required=True,
        help="The output height",
    )
    parser.add_argument(
        "--num_frames",
        type=int,
        required=True,
        help="The number of output frames",
    )
    parser.add_argument(
        "--save_fps",
        type=int,
        default=12,
        help="The number of output frames",
    )

    return parser.parse_known_args()[0]


def create_text_to_video_payloads_for_colligo(
    prompt_file_path: str,
    avoid_prompt: str,  # NOTE currently the avoid prompt will be fixed - we can update this in the future
    limit_prompts: int,
    seeds: list[int],
    width: int,
    height: int,
    num_frames: int,
    prompt_debiasing: bool = False,
    prompt_expansion: bool = False,
    locale: str = "en-US",
) -> list[dict[str, Any]]:
    prompts, _ = read_inputs(Path(prompt_file_path), limit_prompts)

    inputs = []
    for prompt in prompts:
        prompt_input = []
        for seed in seeds:

            payload = {
                "seeds": [seed],
                "size": {"width": width, "height": height, "num_frames": num_frames},
                "outputMode": "full",
            }

            payload["prompt"] = prompt
            payload["negativePrompt"] = avoid_prompt
            payload["locale"] = locale

            prompt_input.append(payload)

        # inputs.append(payload)
        inputs.append(prompt_input)

    return inputs


def async_handling(command):
    response = subprocess.check_output(command, shell=True, text=True)
    print("async response:", response)
    return response


def extract_frames():
    # frame = Image.open(bytesio_gif)
    # nframes = 0
    # images = []
    # while frame:
    #     images.append(frame.copy())
    #     nframes += 1
    #     try:
    #         frame.seek(nframes)
    #     except EOFError:
    #         break
    frames = iio.imread(
        "/mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/tmp/bytesio.mp4", plugin="pyav"
    )
    images = [Image.fromarray(f) for f in frames]
    return images


def call_text_to_video_colligo_endpoint(
    endpoint: str,
    payload: dict[str, Any],
) -> list[Image.Image]:
    headers = {"Content-Type": "application/json"}
    session = get_session()
    response = session.post(endpoint, json=payload, headers=headers, timeout=120)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # TODO add in logic to allow for

    images = []
    colligo_json = json.loads(response.text)

    # with open("/mnt/localssd/siddhantg/colligo/contrib/AdobeDiffusion/scripts/clineto/handle_async.txt") as f:
    with open("/mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/handle_async.txt") as f:
        ping_command = f.read()
        full_path = colligo_json["links"]["result"]["href"]
        full_command = ping_command.replace("<path>", full_path)

    print("full_command")
    print(full_command)
    print()

    while "outputs" not in colligo_json:
        time.sleep(30)
        new_response = async_handling(full_command)
        colligo_json = json.loads(new_response)

    url = colligo_json["outputs"]["presignedUrl"]
    bytesio = BytesIO(requests.get(url).content)

    with open("/mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/tmp/bytesio.mp4", "wb") as f:
        f.write(bytesio.read())
        print("saved to /mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/scripts/clineto/tmp/bytesio.mp4")

    images = extract_frames()
    # images.append(Image.open(bytesio))

    print("images:", len(images))

    # if "outputs" in colligo_json:
    #     for output in colligo_json["outputs"]:
    #         bytesio = BytesIO(requests.get(output["presignedUrl"]).content)
    #         images.append(Image.open(bytesio))

    # return [images]  # TODO: Make this work for larger batch size
    return images


def generate_html_text_to_video_colligo_endpoint(
    text_prompt_file: str,
    limit_prompts: int,
    avoid_prompt: str,
    seeds: list[int],
    width: int,
    height: int,
    num_frames: int,
    endpoint: str,
    save_fps: int,
    save_to: str,
    return_file_path: str,
) -> None:
    upload_bucket = "clio.corp.adobe.com"
    assert check_s3_access(upload_bucket), f"Environment doesn't have access to s3://{upload_bucket}"

    html = HTML(web_dir=save_to, title=save_to.split("/")[-1])
    html.add_table()

    payloads = create_text_to_video_payloads_for_colligo(
        prompt_file_path=text_prompt_file,
        avoid_prompt=avoid_prompt,
        limit_prompts=limit_prompts,
        seeds=seeds,
        width=width,
        height=height,
        num_frames=num_frames,
    )

    for idx, prompt_payload in tqdm(enumerate(payloads)):
        _images = []
        for payload in prompt_payload:
            output_images = call_text_to_video_colligo_endpoint(endpoint=endpoint, payload=payload)
            _images.append(output_images)

        prompt = payload["prompt"]
        avoid_prompt = payload["negativePrompt"]
        # add to HTML
        html.add_images(
            _images,
            row_label=f"[{idx+1} \n\n Colligo e2e \n\n [TextPrompt]:{prompt} \n\n [AvoidPrompt]:{avoid_prompt}",
            width=_images[0][0].size[0],  # TODO make width the width which we have of our video, maybe?
            format="mp4",
            fps=save_fps,
        )
        html.save()
        upload_dir_to_s3(save_to, return_file_path, overwrite=True)


if __name__ == "__main__":
    # Parse command-line arguments
    opt = parse_arguments()
    generate_html_text_to_video_colligo_endpoint(
        text_prompt_file=opt.text_prompt_file,
        limit_prompts=opt.limit_prompts,
        avoid_prompt=opt.avoid_prompt,
        seeds=opt.seeds,
        width=opt.width,
        height=opt.height,
        num_frames=opt.num_frames,
        endpoint=opt.endpoint,
        save_fps=opt.save_fps,
        save_to=opt.save_to,
        return_file_path=opt.return_file_path,
    )
"""
# Run colligo v2 for video generation

python scripts/clio3/text_to_video_html_colligo_endpoint.py \
    --endpoint http://localhost:8000/v2/video/generate \
    --token "<token>" \
    --save_to /sensei-fs/users/siddhantg/colligo_2024_05_10/auto-inference/sample_results/dit_fps_12_105k \
    --return_file_path /sensei-fs/users/siddhantg/colligo_2024_05_10/auto-inference/sample_results/dit_fps_12_105k/output_dit_fps_12_105k.txt \
    --text_prompt /sensei-fs/users/siddhantg/colligo_2024_04_30/colligo/contrib/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/kineto_eval_sentences/sora_prompts.txt \
    --limit_prompts 2 \
    --seeds "333,334" \
    --aesthetic_score 6.0 \
    --height 22 \
    --width 40 \
    --num_frames 15 \
    --save_fps 12

"""
