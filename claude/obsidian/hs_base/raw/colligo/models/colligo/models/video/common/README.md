## Common Video Modules

### Profiling - Custom Backends

Colligo allows for custom backends which are not listed above as well. As part of the video pipelines few custom backends were added which other teams can leverage as well. You can use these backends by following the steps below:

1. Add `colligo.models.video.common.profiling` as a dep in `colligo.yaml` for your pipeline
2. To your `colligo.dev.yaml`, add `custom_profiling_tools_callable: "colligo.models.video.common.profiling.handlers.CustomHandlerFactoriesCallable"`
3. Add the backends to your `annotate.zone` as shown below.
```py
from colligo.base.log_codes import LogCode
from colligo.base.profiling import annotate
from colligo.models.video.common.profiling.handlers import CustomHandlerType

with annotate.zone(
    zone="extract_frames",
    log_code=LogCode.PERF_ZONE,
    args={
        "torch_mem": False,
        "cprofile": False,
        "bg_monitor": True,
    },
    backends=[
        CustomHandlerType.TORCH_MEM,
        CustomHandlerType.YAPPI,
        CustomHandlerType.BG_MONITOR,
    ],
):
    ...
```

#### `TORCH_MEM`

This backend is a wrapper around the PyTorch tool to visualize the CUDA memory utilization. You can find more information [here](https://pytorch.org/docs/stable/torch_cuda_memory.html).

This backend generates a pickle file which can be visualized using [pytorch.org/memory_viz](https://pytorch.org/memory_viz) as shown below.

![Torch Memory Profiler](../../../../../docs/_assets/profiling/image-1.png)

#### `TORCH_TRACE`

This backend is a wrapper around the PyTorch profiler to generate traces of the all the functions within the annotated zone. You can find more information [here](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html#using-tracing-functionality).

This backend generates a json file which can be visualized using [chrome tracing](chrome://tracing) as shown below.

![Torch Profiler Trace](../../../../../docs/_assets/profiling/image-2.png)

#### `BG_MONITOR`

This backend is a background resource monitor to track the CPU, RAM, GPU, Network & Disk IO. This uses statistical profiling technique to run a thread in background and periodically take snapshots of the resource utilization. This is particularly useful to identify is there would be a memory issue on scaling, check the CPU/GPU util for the annotated zone etc.

`BG_MONITOR` outputs 3 png files for CPU/RAM, GPU, IO utilization and a json with all the raw datapoints. A sample output for the CPU/RAM util is shown below.

![BG Resource Monitor](../../../../../docs/_assets/profiling/image-3.png)


#### `YAPPI`

This backend is a wrapper around the [yappi](https://github.com/sumerc/yappi) library. This is similar to `cProfile` but works well in multi-threaded and asyncronous envs. This is a line profiler which is useful to quickly identify the bottlenecks for CPU workers.

`YAPPI` outputs a `prof` file which can be visualized using [snake_viz](https://github.com/jiffyclub/snakeviz) as shown below.

![YAPPI snakeviz profile](../../../../../docs/_assets/profiling/image-4.png)