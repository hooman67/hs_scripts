# Mori

Mori is a PyTorch-based training framework that supports training large-scale foundation models efficiently and scalably. It provides the following features:
* MoriX accelerator that currently suppport FSDP and FSDP2.
* Optimized attention layers with FA2, FA3, Context Parallelism, and Distributed Attention.
* Essential tools for model development including S3 storage, data visualization, profiling, and more!

## More About Mori

Mori is a PyTorch native training framework that helps with training in-house foundation models. It is designed to be simple to use, yet powerful enough to handle complex training scenarios. The framework provides a set of abstractions and utilities that make it easy to define, train, and evaluate models.

Mori consists of the following components:

| Component |  Description  |
|-----------| ------------- |
| mori.training |  Core package for training.         |
| mori.training.morix | Lightweight training accelerator with a common interface between multiple training strategies. New training strategies can be included by implemening new `Plugin`.   |
| mori.training.tools | Common tools for training jobs including HTML creation and S3 storage.      |
| mori.models   | FireFly, Research, and common thirdparty models with configurable optimization.  |
| collections   | Project folders where training logics are implemented by using `mori.training`. Each project has a well-defined ownership to avoid blocking each other. Most experimental features will be tested under collections before upstreaming to `mori.training` or `mori.models`.   |



### Scripting Experience
The building blocks of Mori are not gigantic trainer classes. They are re-usable functional components. You can modify any PyTorch-101 training script with a few lines of codes and start using features including FSDP and S3 checkpointing. We plan to release a few tutorial projects under `collections`.

### Simple Extensions
GenAI is a fast-evolving field where things are changing everyday. To catch up with the trend at the scale of FireFly org, the framework needs to be able to absorb new training strategies and algorithms. The `Strategy Pattern` is adopted by MoriX (mori.training.morix) where new training strategies can easily fit into existing workflows by implementing a new `Plugin`.


## Start Development

Please refer to the [Documentation](https://docs.ai.corp.adobe.com/contrib/Mori/aidoc/overview.html).

## Quick Tips

- You may need to update Genie version if your project doesn't do so. [link](https://docs.genie.ai.corp.adobe.com/#install-genie-in-runai)

- If your code crashes, make sure to evict any process.
    ```
    killall -9 /opt/venv/bin/python
    ```
    If above is successful, you should see `nvidia-smi` show no to little memory usage in each GPU.
