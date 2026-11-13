# Benchmark Scenarios

This directory contains YAML scenario files for benchmarking the CM Analyze pipelines (V3 vs V1).

## Files

- **`benchmark_scenarios.yaml`**: Full benchmark scenarios with multiple test cases
- **`benchmark_test_scenario.yaml`**: Lightweight test scenarios for quick validation

## Scenario Format

Scenarios are defined in YAML with the following structure:

```yaml
- base_recipe:
    modelUrn: "urn:..."
    debug:
      bg_monitor: true
      
  warmup:
    # Optional warmup configuration
    
  recipe_variations:
    - id: "scenario_name"
      recipe:
        # Recipe overrides for this specific scenario
```

## Usage

Pass scenario files to the benchmark CLI:

```bash
python -m colligo.models.firefly.clio_tyom.benchmark run \
  --scenarios ./models/colligo/models/firefly/clio_tyom/benchmark/scenarios/benchmark_scenarios.yaml \
  --colligo-app firefly_tyom_v2_training
```

## Creating New Scenarios

1. Copy an existing scenario file
2. Modify the `base_recipe` for common configuration
3. Add variations under `recipe_variations` with unique IDs
4. Test with a single scenario first before running full suite
