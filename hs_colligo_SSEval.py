import requests
import json
import uuid
import csv
import os
import time
from typing import Any
from typing import Union, List
from io import BytesIO

from loguru import logger
from PIL import Image
from sseval.SelfServeEval import SelfServeEval
from joblib import Parallel, delayed
from tqdm import tqdm
from datetime import datetime


def download_image(url: str) -> Image:
    """
    Parameters
    :url: Image URL
    Return
    :PIL image object or None if error happens
    Download the image from the specified URL.
    """
    pil_image = None
    try:
        response = requests.get(url)
        content_type = response.headers["Content-Type"]
        if content_type.startswith("image/"):
            pil_image = Image.open(BytesIO(response.content))
        else:
            logger.error(f"Not valid image [{content_type}]")
    except Exception as e:
        logger.exception(e)
        logger.error(f"Failed to download image from {url}")

    return pil_image


def pil_to_id(pil_image):
    image_byte_array = BytesIO()
    pil_image.save(image_byte_array, format=pil_image.format)
    image_byte_array = image_byte_array.getvalue()

    response_image = requests.post(storage_url, headers=headers_storage, data=image_byte_array)
    return response_image.json()["images"][0]["id"]


# switch case to handle request
def update_request_for_evalset(eval_set, model_input, seed_list):

    # if "structurematch" in eval_set:
    #     request = {
    #         "prompt": model_input["prompt"],
    #         "n": len(seed_list),
    #         "seeds": seed_list,
    #         "ContentClass": "auto",
    #     }

    #     if "no_reference" not in eval_set:
    #         request["controlData"] = {
    #             "depthData": {"referenceImage": {"presignedUrl": model_input["reference_image_uri"]}},
    #             "cannyData": {"referenceImage": {"presignedUrl": model_input["reference_image_uri"]}},
    #             "adherenceThreshold": model_input["strength"],
    #         }
    # elif "human_diversity" in eval_set:
    #     request = {
    #         "prompt": model_input["prompt"],
    #         "n": len(seed_list),
    #         "seeds": seed_list,
    #         "contentClass": "photo",
    #     }

    # elif "text_rendering_eval_set" in eval_set:
    #     request = {
    #         "prompt": model_input["prompt"],
    #     }

    # else:
    #     print(f"{eval_set} request is not include yet!! Sample model input below")
    #     print(model_input)
    #     request = None

    request = {
        "prompt": model_input["prompt"],
        "n": len(seed_list),
        "seeds": seed_list,
    }

    return request


# Modify these API endpoint URLs and parameters
url = "http://localhost:8000/v2/images/generate"
storage_url = "https://cliofast-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/v2/storage/image"
ldap_parameter = "hshariati"

headers_storage = {
    "x-api-key": "ASMLSenseiTest",
    "authorization": f"Bearer eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktYXQtMS5jZXIiLCJraWQiOiJpbXNfbmExLXN0ZzEta2V5LWF0LTEiLCJpdHQiOiJhdCJ9.eyJpZCI6IjE3MTQ1OTk5OTM0ODVfZmVkN2QyMDktYjJmYS00OGY2LTk0YTgtNjI1NzNmMTFiYzM2X3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJjb2xsaWdvX3Rlc3RpbmciLCJ1c2VyX2lkIjoiMDJCQTREQkE2NTMwODFDNDBBNDk0MTNEQGM2MmYyNGNjNWI1YjdlMGUwYTQ5NDAwNCIsImFzIjoiaW1zLW5hMS1zdGcxIiwiYWFfaWQiOiIwMkJBNERCQTY1MzA4MUM0MEE0OTQxM0RAYzYyZjI0Y2M1YjViN2UwZTBhNDk0MDA0IiwiY3RwIjowLCJmZyI6IllORkhVRE9FN1o2N0E0RFozR1pNQTJJQUtNPT09PT09Iiwic2lkIjoiMTcxNDE3MTg5MTgzNl85NTkyZTUzZS0xNjQ0LTQyNzAtODJiMy1jYmQ0NmNlM2E5OWNfdWUxIiwibW9pIjoiNzA1ZDlmZmYiLCJwYmEiOiJNZWRTZWNOb0VWLExvd1NlYyIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsImNyZWF0ZWRfYXQiOiIxNzE0NTk5OTkzNDg1Iiwic2NvcGUiOiJBZG9iZUlELGZpcmVmbHlfYXBpLG9wZW5pZCJ9.VSPpdh_iC9EQLj8l-BbRi4eoqj-iGYt93Y5z3SzH6MNBQBLSBqI3boh0Pzr_kPAShq0m4p89j4t58KQS_Zlo4UK-7prODg4Ut8IbRcAzUVjpOb1Z_oWzxq8WVreisUR6eD8NvzsMrl3Gg8DUqQLkIukvCyG7Tab66_WWMtE8B5Dn88XpS31p03bZh5JXScfmKALhagRcY1pD02Pe92OwbFPbHWYid-sC5ppiWddi3kU4V-YANGZW80WA1dAtI8TQgJhtgZo6pU55_G3jli44uMcTUNPK7ZNgA57ohGhCnuOWUunNP8SjjiPZfsUBVIWM__o4cDvuCrhfdh2yoJnhIA",
    "Content-Type": "image/png",
    "x-request-id": "454545454545454545",
}

# API headers
headers = {
    "x-request-id": str(uuid.uuid4()),
    "Authorization": f"Bearer eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktYXQtMS5jZXIiLCJraWQiOiJpbXNfbmExLXN0ZzEta2V5LWF0LTEiLCJpdHQiOiJhdCJ9.eyJpZCI6IjE3MTQ1OTk5OTM0ODVfZmVkN2QyMDktYjJmYS00OGY2LTk0YTgtNjI1NzNmMTFiYzM2X3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJjb2xsaWdvX3Rlc3RpbmciLCJ1c2VyX2lkIjoiMDJCQTREQkE2NTMwODFDNDBBNDk0MTNEQGM2MmYyNGNjNWI1YjdlMGUwYTQ5NDAwNCIsImFzIjoiaW1zLW5hMS1zdGcxIiwiYWFfaWQiOiIwMkJBNERCQTY1MzA4MUM0MEE0OTQxM0RAYzYyZjI0Y2M1YjViN2UwZTBhNDk0MDA0IiwiY3RwIjowLCJmZyI6IllORkhVRE9FN1o2N0E0RFozR1pNQTJJQUtNPT09PT09Iiwic2lkIjoiMTcxNDE3MTg5MTgzNl85NTkyZTUzZS0xNjQ0LTQyNzAtODJiMy1jYmQ0NmNlM2E5OWNfdWUxIiwibW9pIjoiNzA1ZDlmZmYiLCJwYmEiOiJNZWRTZWNOb0VWLExvd1NlYyIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsImNyZWF0ZWRfYXQiOiIxNzE0NTk5OTkzNDg1Iiwic2NvcGUiOiJBZG9iZUlELGZpcmVmbHlfYXBpLG9wZW5pZCJ9.VSPpdh_iC9EQLj8l-BbRi4eoqj-iGYt93Y5z3SzH6MNBQBLSBqI3boh0Pzr_kPAShq0m4p89j4t58KQS_Zlo4UK-7prODg4Ut8IbRcAzUVjpOb1Z_oWzxq8WVreisUR6eD8NvzsMrl3Gg8DUqQLkIukvCyG7Tab66_WWMtE8B5Dn88XpS31p03bZh5JXScfmKALhagRcY1pD02Pe92OwbFPbHWYid-sC5ppiWddi3kU4V-YANGZW80WA1dAtI8TQgJhtgZo6pU55_G3jli44uMcTUNPK7ZNgA57ohGhCnuOWUunNP8SjjiPZfsUBVIWM__o4cDvuCrhfdh2yoJnhIA",
    "x-api-key": "ASMLSenseiTest",
    "Content-Type": "application/json",
    "accept": "*/*",
}

eval_set_dictonary = {
    "prompts_general_subset_500_tq": "1.0",
    "prompts_human_subset_500_htq": "1.0",
    "prompts_human_subset_500_bias": "1.0",
    "prompts_general_subset_500_coherence": "1.0",
}


def structure_parallel(eval_set, version):
    # parameter
    save_to = "/sensei-fs/users/hshariati/eval/clio3_dmd_guide8_mp_v4_2024_02_28-2024-03-07T11-20-43/dmd_30k_05-01-24_SSEval_tq_htq_bias_coherence/"
    save_to = os.path.join(save_to, eval_set)
    os.makedirs(save_to, exist_ok=True)
    error_logs = []
    now = datetime.now().strftime("%Y%m%d%H%M")

    sseval = SelfServeEval(
        ldap=ldap_parameter,
        evaluation_set=f"{eval_set}",
        evaluation_set_version=f"{version}",
        run_id=f"{ldap_parameter}_{now}_{eval_set}",
    )

    total_prompts = sseval.get_eval_set_length()
    count = 0

    # progress bar to make it more visulaly appealing
    with tqdm(total=total_prompts, desc=f"Processing {eval_set}") as pbar:
        # Loop over the model inputs: here, we're just looping over the first 3 prompts
        for model_input_id, model_input, seed_list in sseval.get_model_input_it():

            count += 1

            request = update_request_for_evalset(eval_set, model_input, seed_list)

            if request is None:
                break

            data = json.dumps(request)

            # image generation
            start_time = time.time()
            response = requests.post(url, data=data, headers=headers)

            inference_time = time.time() - start_time

            if response.status_code == 200:
                json_response = response.json()
                for output in json_response["outputs"]:
                    img_seed = output["seed"]
                    img_url = output["image"]["presignedUrl"]
                    pil_img = download_image(img_url)

                    sseval_image_name = f"{model_input_id}_{img_seed}.png"
                    temp_path = os.path.join(save_to, sseval_image_name)
                    pil_img.save(temp_path)

                    sseval.add_record(
                        generated_asset=temp_path,
                        model_input_id=model_input_id,
                        inference_time_s=inference_time / len(seed_list),
                        seed=img_seed,
                    )

            else:
                print("Error:", response.status_code)
                print(response.text)
                error_logs.append([model_input_id, response.status_code, response.text])
            pbar.update(1)

    # Save: create a manifest, upload images + manifests to s3
    s3_url_json, run_id = sseval.save()

    # Requests that did not go through because they were unsafe / harmful etc..

    # Specify the file path
    csv_file_path = os.path.join(save_to, "error_logs.csv")

    # Open the file in write mode with newline='' to prevent extra line breaks
    with open(csv_file_path, "w", newline="") as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write each row of the data to the CSV file
        for row in error_logs:
            csv_writer.writerow(row)

    print("Error logs has been dumped into", csv_file_path)


results = Parallel(n_jobs=-1)(
    delayed(structure_parallel)(eval_set, version) for eval_set, version in eval_set_dictonary.items()
)
