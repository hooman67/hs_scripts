This guide describes the creation of the config files for the tileable workflow.

## Script support
`models/colligo/models/firefly/clio/scripts/create_seamless.py` can be used to create the seamless yaml, example:
```bash
python models/colligo/models/firefly/clio/scripts/create_seamless.py models/colligo/models/firefly/clio_common/configs/multidiffusion/clio3_pro5_24_moe_part1.yaml
```
## Manual changes
- Copy the existing config, for ex, copy `models/colligo/models/firefly/clio_common/configs/multidiffusion/clio3_pro5_24_moe_part1.yaml` to `models/colligo/models/firefly/clio_common/configs/multidiffusion/clio3_pro5_24_moe_part1_seamless.yaml`
- change the guidance type to seamless and add the following seamless parameters.

```yaml
guidance_type: seamless
seamless_image_parameters:
  inner_guidance_type: cfg-stdev-normalize
  roll_scale: [0.25, 0.25]
```

- add `sampling_parameters` with `logsnr`. (replicate the existing `sampling_parameter` for `uniform` and change `skip_type` to `logsnr`)

```yaml
sampling_parameters:
  - # Scheduling.
    beta_0: 0.00085
    beta_1: 0.012
    beta_schedule: linear
    max_beta: 0.999

    # Sampling.
    schedule_type: hybrid-ddim
    prediction_type: v_prediction
    dynamic_thresholding: null
    eps_tolerance: 0.01
    momentum_beta: 0.6
    solver_order: 2
    zero_terminal: true

    # Noise.
    base_eta: 1.0
    eta_schedule_type: constant

    # Hybrid specific.
    first_again_after_timestep: -1
    first_sampler: ddim
    hybrid_transition: 750
    second_sampler: dpmsolverpp

    # Skips.
    skip_type: uniform
    timesteps_start_ratio: 1.0
    timesteps_end_ratio: 0.45
    training_timesteps: 1000
  - # Scheduling.
    beta_0: 0.00085
    beta_1: 0.012
    beta_schedule: linear
    max_beta: 0.999

    # Sampling.
    schedule_type: hybrid-ddim
    prediction_type: v_prediction
    dynamic_thresholding: null
    eps_tolerance: 0.01
    momentum_beta: 0.6
    solver_order: 2
    zero_terminal: true

    # Noise.
    base_eta: 1.0
    eta_schedule_type: constant

    # Hybrid specific.
    first_again_after_timestep: -1
    first_sampler: ddim
    hybrid_transition: 750
    second_sampler: dpmsolverpp

    # Skips.
    skip_type: logsnr
    timesteps_start_ratio: 1.0
    timesteps_end_ratio: 0.45
    training_timesteps: 1000
```
