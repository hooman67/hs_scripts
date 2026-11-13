This description demonstrates how you can run your workers and web apps in cloud while leveraging the distributed computing nature.

1. You would need a Redis cluster. We recommend a managed solution, like `Amazon MemoryDB`, but for a quick solution
you can have a pod that simply runs the following as entry point.
    ```sh
    python -m frameworks.inference dev redis-cluster
    ```
1. You would need a config file (often created via a config map) in each pod that contains the configuration for inference frameworks and any library that integrates with its `default_config` mechanism.
1. You would need an http server to serve your web app endpoints. You need a service (pods) that run
    ```sh
    # if there are more web apps to include, separate by ","
    python -m frameworks.inference webapps ai.sample_a.webapp.hammering_app --config <path to config>
    ```
1. You would need pods that serve your workers.
    ```
    python -m frameworks.inference workers ai.sample_a.compute_worker.steve_v1 --config <path to config>
    python -m frameworks.inference workers ai.sample_a.pipeline_worker.emanuel_v1 --config <path to config>
    ```
1. Make an ingress that can send traffic to the http server pod (item 3), and you have a bare minimum app served in cloud.
