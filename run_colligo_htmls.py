import argparse
import json
import os
from io import BytesIO

import requests
import tqdm
from PIL import Image
from requests.adapters import HTTPAdapter, Retry
from util import check_s3_access, upload_dir_to_s3

from clio.prototyping_tools.html.viz import HTML


def get_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[404, 429, 500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def _read_inputs(prompt_input, limit_prompts):
    if prompt_input:
        if os.path.exists(prompt_input):
            with open(prompt_input) as f:
                prompts = f.readlines()[:limit_prompts]
            return [x.strip() for x in prompts]
        else:
            return [prompt_input]
    else:
        return [None]


def create_pil_image_from_presigned_url(url):
    response = get_session().get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    image = Image.open(BytesIO(response.content))
    return image


def get_output_images(colligo_response):
    images = []
    colligo_json = json.loads(colligo_response.text)
    if "outputs" in colligo_json:
        for output in colligo_json["outputs"]:
            if "image" in output and "presignedUrl" in output["image"]:
                image_url = output["image"]["presignedUrl"]
                image = create_pil_image_from_presigned_url(image_url)
                if image:
                    images.append(image)
    return images


def generate_html(opt):
    upload_bucket = "clio.corp.adobe.com"
    assert check_s3_access(upload_bucket), f"Environment doesn't have access to s3://{upload_bucket}"

    headers = {"Authorization": f"Bearer {opt.token}", "Content-Type": "application/json"}
    colligo_sess = get_session()

    save_to = opt.save_to
    html = HTML(web_dir=save_to, title=save_to.split("/")[-1])
    html.add_table()
    prompts = _read_inputs(opt.text_prompt, opt.limit_prompts)

    for idx, prompt in tqdm.tqdm(enumerate(prompts)):
        payload = {
            "n": 4,
            "seeds": [333, 334, 335, 336],
            "size": {"width": 1024, "height": 1024},
            "prompt": f"{prompt}",
            "locale": "en-US",
            "outputMode": "full",
        }
        try:
            response = colligo_sess.post(opt.endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            _images = get_output_images(response)
            html.add_images(_images, row_label=f"[{idx+1} \n\n Colligo e2e \n\n TextPrompt:{prompt}")
        except Exception as e:
            print(f"HTTP Error: {e}")

    html.save()
    upload_dir_to_s3(opt.save_to, opt.return_file_path, overwrite=True)


def parse_arguments():
    # Parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--endpoint",
        type=str,
        default="http://localhost:8000/v3/images/generate",
        help="Colligo endpoint URL",
    )

    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="Colligo Auth Token",
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
        "--text_prompt",
        type=str,
        required=True,
        help="Text prompt file for generations",
    )

    parser.add_argument(
        "--limit_prompts",
        type=int,
        default=None,
        help="Limit to the first N prompts of the text file",
    )

    return parser.parse_known_args()[0]


if __name__ == "__main__":
    # Parse command-line arguments
    opt = parse_arguments()
    generate_html(opt)
