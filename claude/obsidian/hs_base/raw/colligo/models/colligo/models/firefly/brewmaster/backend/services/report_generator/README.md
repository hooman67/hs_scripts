# Report Generator

This module contains all logic for building comparison reports from Master JSON data in the Brewmaster evaluation system.

## Architecture

All report handling has been moved from frontend (JavaScript/React) to backend (Python) for:
- **Performance**: NumPy/SciPy are significantly faster than JavaScript for statistical computations
- **Smaller payloads**: Send histogram bins instead of raw per-sample data
- **Simpler frontend**: Frontend is now purely presentational
- **Consistency**: All calculations use the same Python libraries
- **Caching potential**: Backend can cache computed reports in the future

## Modules

### `builder.py` - ComparisonReportBuilder

Main class for building comparison reports from Master JSON data.

**Key responsibilities:**
- Aggregates metrics across models, datasets, and samples
- Extracts per-sample data from Master JSON
- Coordinates with statistics module to enrich data
- Returns complete comparison report with pre-computed histograms and statistics

**Usage:**
```python
from colligo.models.firefly.brewmaster.backend.services.report_generator import ComparisonReportBuilder

builder = ComparisonReportBuilder(master_json_manager)
report = builder.build_comparison_report(
    job_id=job_id,
    job_name=job_name,
    task_type="t2v",
    model_ids=["model-1", "model-2"],
    dataset_ids=["dataset-1"],
    metric_ids=["metric-1", "metric-2"],
    model_names={"model-1": "Firefly v2.1"},
    dataset_info={"dataset-1": {"name": "t2v_demo", "version": "v1.1", "dataset_key": "t2v_t2v_demo_v1.1"}},
    metric_names={"metric-1": "temporal_ssim"},
)
```

### `statistics.py` - Statistical Computations

Functions for computing statistics, confidence intervals, and histograms.

**Key functions:**

#### `create_histogram_bins(data: list[float], num_bins: int = 30)`
Creates histogram bins from data values.

**Returns:**
```python
[
    {"binStart": 0.80, "binEnd": 0.85, "count": 12, "binLabel": "0.800"},
    {"binStart": 0.85, "binEnd": 0.90, "count": 25, "binLabel": "0.850"},
    ...
]
```

#### `calculate_95_ci(values: list[float])`
Calculates 95% confidence interval using scipy.stats.

**Returns:**
```python
{"lb": 0.932, "ub": 0.968}  # Lower and upper bounds
```

#### `average_per_sample_values(per_sample: dict[str, list[float]])`
Averages per-frame values to get one value per sample.

**Input format:**
```python
{
    "0": [0.95, 0.94, 0.96],  # Frame-level scores for sample 0
    "1": [0.93, 0.92, 0.94],  # Frame-level scores for sample 1
}
```

**Returns:**
```python
[0.95, 0.93]  # One averaged value per sample
```

#### `compute_metric_statistics(per_sample: dict, num_bins: int = 30)`
Comprehensive statistics computation for a single metric.

**Returns:**
```python
{
    "mean": 0.95,
    "std": 0.03,
    "min": 0.89,
    "max": 0.99,
    "ci_95": {"lb": 0.93, "ub": 0.97},
    "histogram": [...],  # Histogram bins
    "sample_count": 100,
    "per_sample": {...}  # Original per-sample data preserved
}
```

#### `enrich_comparison_data_with_statistics(comparison_data: dict, num_bins: int = 30)`
Enriches an entire comparison report with statistics for all metrics.

**Input:** Comparison report from ComparisonReportBuilder
**Output:** Same report with added histogram, CI, and sample_count fields

## Data Flow

```
1. API receives request for job results
   ↓
2. ComparisonReportBuilder extracts data from Master JSON
   ↓
3. statistics.py computes histograms, CI, and aggregates
   ↓
4. API returns enriched report to frontend
   ↓
5. Frontend renders charts using pre-computed data
```

## Frontend Integration

The frontend (`JobResultsVisualization.tsx`) expects this data structure:

```typescript
interface ComparisonData {
  comparisons: Array<{
    metrics: Record<string, {
      mean: number
      std: number
      min: number
      max: number
      ci_95: { lb: number; ub: number }
      histogram: Array<{ binStart: number; binEnd: number; count: number; binLabel: string }>
      sample_count: number
      per_sample?: Record<string, number | number[]>  // Optional, for drill-down
    }>
  }>
}
```

The frontend **only** renders this data—it performs **no** statistical calculations.

## Performance Considerations

- NumPy operations are vectorized and highly optimized
- scipy.stats uses optimized C implementations
- Histogram binning is O(n) with NumPy
- CI calculation with scipy is more accurate than JavaScript approximations
- Frontend receives ~30 bins instead of 1000s of raw data points

## Testing

Test the statistics module:
```bash
pytest tests/test_statistics.py
```

Test the full report builder:
```bash
pytest tests/test_report_builder.py
```

