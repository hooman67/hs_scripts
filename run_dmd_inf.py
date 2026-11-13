from inference.inference_app import Inference
from inference.inference_md_app import InferenceMD
from inference.inference_utils import yaml_utils
from pathlib import Path
from PIL import Image
import numpy as np
import torch

# load one model
config_first = yaml_utils.yaml_to_inference_config(
    Path("/sensei-fs/users/hshariati/experimental_configs/dmd_prod3_18_inference_config.yaml")
)
for model_loader in config_first.model_configs:
    if model_loader[1] is not None:
        model_loader[1].device = 0
app = Inference(config_first)

app.config.seeds = [0]

# no mc
from clio.typings.typings import AestheticInputs

x = 128
y = 128
edge = torch.zeros((1, 2, x * 8, y * 8))
entity = torch.zeros((1, 3, x * 8, y * 8))
depth = torch.zeros((1, 1, x * 8, y * 8))

result = app(
    text_prompt="some pig",
    edge=edge,
    aesthetic_inputs=AestheticInputs(positive_aesthetic_score=6.0),
    #  content_type="vector",
    depth=depth,
    entity=entity,
    control_modules=[],
).images

result.save("/mnt/localssd/hshariati/colligo/delete/dmd_inf.png")
