# Benchmark Scenarios

This directory contains YAML scenario files for benchmarking Colligo pipeline endpoints.

## Directory Structure

```
scenarios/
├── cm_analyze/              # CM Analyze specific scenarios
│   ├── benchmark_scenarios.yaml
│   ├── benchmark_test_scenario.yaml
├── README.md                # This file
└── example_scenario.yaml    # Template for creating new scenarios
```

## Creating New Scenarios

1. Copy `example_scenario.yaml` as a starting point
2. Modify the `base_recipe` for your endpoint's common configuration
3. Add variations under `recipe_variations` with unique IDs
4. Create a subdirectory for your use case if you have multiple scenario files

## Scenario File Format

Scenarios are defined in YAML with the following structure:

```yaml
# Each scenario group has an id, base recipe, optional warmup, and variations
- id: my_scenario_group
  base_recipe:
    # Common fields applied to all variations in this group
    field1: value1
    debug:
      setting1: true
    # Optional: serialized as JSON into the `x-colligo-debug-input` HTTP header
    debug_headers:
      someDebugHeaderFlag: true

  warmup:
    # Optional warmup configuration (runs before actual scenarios)
    field1: warmup_value

  recipe_variations:
    - id: variation_1
      recipe:
        # Fields specific to this variation (merged with base_recipe)
        field2: value2

    - id: variation_2
      recipe:
        field2: value3
```

### Key Fields

- **id**: Unique identifier for the scenario group
- **base_recipe**: Common configuration applied to all variations
- **warmup**: Optional warmup request to prime the system
- **recipe_variations**: List of specific test cases
  - Each variation has an `id` and a `recipe` that overrides/extends `base_recipe`

### `debug_headers` (optional)

A `debug_headers` dict may appear inside `base_recipe`, `warmup`, or any variation's `recipe` (next to `debug`). The loader deep-merges it across layers and the benchmark serialises the result as JSON into the `x-colligo-debug-input` HTTP header when calling the endpoint. Use this to toggle any debug switch the target endpoint recognises on that header — the benchmark does not interpret the contents.

## Using Scenarios

Pass scenario files to the benchmark CLI:

```bash
python -m colligo.models.firefly.clio_tyom.benchmark run-distributed \
  --branch main \
  --colligo-app your_app \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/your_scenarios.yaml \
  --endpoints "v3:/v2/images/your_endpoint_v3" "v1:/v2/images/your_endpoint" \
  --sensei-output /sensei-fs/users/$USER/benchmark
```
