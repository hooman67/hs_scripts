import argparse
import os
from pathlib import Path

from clio.prototyping_tools.aws_util import S3Handle
from clio.prototyping_tools.html.viz import HTML
from inference.inference_app import Inference
from inference.inference_utils import yaml_utils
from clio.typings.typings import AestheticInputs
import numpy as np
import torch
from PIL import Image


def save_images(imgs, save_to, rownum, colnum):
    if not isinstance(imgs, list):
        imgs = [imgs]
    return_imgs = []
    for img in imgs:
        curimg = Image.fromarray(np.array(img))
        return_imgs.append(curimg)
        colnum += 1
    return colnum, return_imgs


def upload_dir_to_s3(save_to, return_file_path, modelname=None):
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
    )
    html_title = save_to.split("/")[-1] if modelname is None else modelname
    html_url = (
        f"http://clio.corp.adobe.com/model_evaluation/{save_to}/{html_title}.html"
    )
    print(f"Results available at: {html_url}")
    if return_file_path is not None:
        with open(return_file_path, "w") as file:
            file.write(html_url)


def main(
    config_file,
    save_to,
    prompt_file,
):

    config_obj = yaml_utils.yaml_to_inference_config(Path(config_file))
    for model_loader in config_obj.model_configs:
        if model_loader[1] is not None:
            model_loader[1].device = 0
    app = Inference(config_obj)

    html = HTML(web_dir=save_to, title=save_to.split("/")[-1])
    html.add_table()

    with open(prompt_file) as f:
        sentences = f.readlines()
    sentences = [sentence.strip() for sentence in sentences]

    if not os.path.isdir(save_to):
        os.makedirs(save_to)
    cnt = 0

    edge = torch.zeros((1, 2, 128 * 8, 128 * 8))
    entity = torch.zeros((1, 3, 128 * 8, 128 * 8))
    depth = torch.zeros((1, 1, 128 * 8, 128 * 8))

    for sentence in sentences:
        _images = []
        _captions = []
        colnum = 0

        result = app(
            text_prompt=sentence,
            edge=edge,
            depth=depth,
            entity=entity,
            aesthetic_inputs=AestheticInputs(positive_aesthetic_score=6.0),
            control_modules=[],
        ).images

        colnum, return_imgs = save_images(result, save_to, cnt, colnum)
        _images += return_imgs
        _captions.append("dmd_1step_1000to0")

        html.add_images(
            _images,
            row_label=f"row: [{cnt}], Prompt:{sentence}",
            img_captions=_captions,
            width=min(_images[0].width, _images[0].height),
        )
        html.save()
        upload_dir_to_s3(save_to, return_file_path=None)
        cnt += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the inference script.")
    parser.add_argument(
        "--config", type=str, help="Path to the YAML configuration file",
        default="/sensei-fs/users/alse/dmd/dmd/implementations/models/dmd_prod3_18_inference_config.yaml"
    )
    parser.add_argument(
        "--save_to",
        type=str,
        default=None,
        help="Directory to save output images and HTML",
    )
    parser.add_argument(
        "--prompt_file", type=str, help="Path to the prompt file",
        default="/sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/new_eval_sentences_people.txt"
    )
    args = parser.parse_args()

    main(config_file=args.config, save_to=args.save_to, prompt_file=args.prompt_file)
