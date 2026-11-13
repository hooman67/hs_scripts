# Dataloading for Training and Inference

This readme will describe the dataloading for training and inference in the Conversational Interface.


## Training dataloading

For the conversational interface, all dataloading (image, video, audio, etc.) is done in the `src/foundation_exploration/data/inference_data.py`. In the data config, the only required field in the config is `assets` which contains a list[list[asset dictionary]] where the asset dictionary contains all relevant information to construct the asset. To validate the inputs, we use `AssetData` pydantic models.


## Inference dataloading

In the conversational interface, we support any Dataset class which follows the protocol `ConversationalInferenceDataset` defined in `src/foundation_exploration/common/types_gr6.py`. For quick iteration/exploration, feel free to create your own dataset class.

In production, we use the `X2XDataset` class in `conversational_inference_dataset.py`. This is the most generic conversational dataloader for inference, and it supports any arbitrary tasks. To utilize the dataloader, it requires a `prompt_path` which contains a path to your inference dataset in `json` format. This dataset should be structured as follows:

```
[
    {
        "task": str,  # Required. This task string corresponds to the system prompt key in you VLM model config
        "prompt": str,  # Optional. The user prompt or caption.
        "negative_prompt": str,  # Optional. The prompt/caption used for the uncondition generation in CFG
        "media": list[str],  # Optional. An list of media assets. The order of these is the order which they are used/placed in the conversation.
        "eval_set_item_id": str,  # Optional. The eval item id used by EvalHub for evaluations
        "output_media": str, # Optional. Path to a media asset which is an expected "ground-truth". Not currently used.
        "aspect_ratio": str,  # Optional. Defaults to 1:1. Area-preserving aspect ratio which scales the given base height/width.
        "width": int,  # Optional. The target width in pixels. Error thrown if aspect ratio is also given.
        "height": int,  # Optional. The target height in pixels. Error thrown if aspect ratio is also given.
        "num_frames": int,  # Optional. The target number of frames for video generation.
    },
]
```

To validate that an inference dataset is of the correct format as well as visualize the given dataset, you can call the script `python scripts/data/visualize_test_dataset.py -d <path-to-json> -n 16`. If the dataset is of the correct format, it will generate an HTML with `-n` samples of the dataset.

Note: This format may change once we officially support interleaving of data.
