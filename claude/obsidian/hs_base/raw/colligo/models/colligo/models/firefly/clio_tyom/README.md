# Firefly Custom Models (aka. Train Your Own Model)

This is the main code subtree for the Custom Models project.

### Inference Optimizations

#### FP8 quantization

FP8 quantization is based on the AOTI framework's (`frameworks.aoti` package) support for compiling the model with quantization and calibration.

##### Calibration

To make use of the FP8's range and precision as much as possible, we calibrate the weights using some scale values based on the inputs/outputs ranges determined from a set of representative inputs passed through the model's blocks.

Instructions for dumping model inputs for running the calibration:

1. Enable input dumping logic in the inference code

    e.g. For CM5, the dumping code resides in [t2x_inference.py](modules/inference/cm5/simple/t2x_inference.py) - set `DUMP_FP8_CALIBRATION_DATA` to `True` and set a proper dumping folder in the code where this constant is used (ensure that folder exists).

2. (optional) Upload the dumped inputs to an S3 bucket for persistence
    ```bash
    s5cmd cp --show-progress --concurrency=20 '/mnt/localssd/cm5/aot/calibration/*' s3://colligo-dev-artifacts/artifacts-v1/tyom/cm5/dit/calibration_inputs/ie_2026_06_02/
    ```

3. Run calibration using the AOTI export script

    e.g. for CM5, run the [aoti_export.py](modules/denoisers/gen45/export/aoti_export.py) script with `should_quantize = True` and `calib_data_base_path` set to the above dumping folder.

4. Check the produced calibration ranges using the visualization script: [calibration_visualisation.py](modules/denoisers/gen45/export/calibration_visualisation.py)

5. Upload the calibration ranges file (`calibration_ckpt.pt`) to the colligo artifacts S3 bucket and reference it in the `build.py` file:
    ```bash
    ./m deps.upload_artifact <path_to_the_compilation_folder>/calibration_ckpt.pt tyom/cm5/dit
    ```