# Bazel 101

Bazel is a build system from Google (think of Make on steroids). When set up correctly, it offers several key advantages that we are interested in:

- **Fast**: Only runs actions that actually need to run. If nothing has changed, nothing gets rebuilt.
- **Hermetic**: Provides consistent, reproducible builds by minimizing external effects like environment variables and developer-specific configurations.
- **Simple onboarding**: Developers just run a single build command, and Bazel handles all the dependencies and setup automatically.

If you you are contributing to the inference platform, and not have used Bazel before, I highly recommend to spend a day or two to get familiar with.

## Fundamentals

[🌱 First Build Tutorial](https://bazel.build/start/cpp) |  [🌱 Fundamental concepts](https://bazel.build/concepts/build-ref)

I first recommend to follow the links above to get a hang of most important concepts.

## Bazel Modules

[🌱 External Dependencies](https://bazel.build/external/overview)

Modern Bazel (recent few years) has switched to the concept of Bazel Modules for linking different projects that use Bazel. This is related to the file `MODULE.bazel`, and the `bazel_dep(...)` command. Read the sections above under `External Dependencies` to learn this concept. 

## Bazel Query

[🌱 Bazel Query](https://bazel.build/query/quickstart)

Bazel has commands to explore contents of BUILD files without opening them. Read section above to learn more. This helps you navigate the services ecosystem and well as any other Bazel MODULE, find where build artifacts go, ... .

## Writing rules and macros

[🌱 Extending, Concepts](https://bazel.build/extending/concepts) | [🌱 Extending, Tutorial](https://bazel.build/rules/rules-tutorial) 


Bazel at core is a graph execution engine. Most of the other functionalities are built on top of that through its extension API (i.e. defining `rules`, `macros`, and `aspects`). We even use them within the inference platform. Read the sections above to learn more.

## Build file generation with Gazelle

[🦌 Gazelle Overview](https://github.com/bazel-contrib/bazel-gazelle#gazelle-build-file-generator) | [🐍 Gazelle for Python Overview](https://github.com/bazel-contrib/rules_python/tree/main/gazelle#python-gazelle-plugin) | [🐍 Gazelle for Python Example](https://github.com/bazel-contrib/rules_python/tree/main/examples/build_file_generation)

We don't want the developers to need to deal with the BUILD files constantly, and auto-manage them as much as possible. This is done via the `Gazelle` tool. Read through the links above to learn more.

I highly recommend to follow the example and get your hands dirty with it. One caveat it has is that it uses the old `WORKSPACE` instead of modern `MODULE.bazel`. You can probably ask cursor or ChatGPT to convert that to `MODULE.bazel` for you.


## Shayan's playground

[🌱 Link](https://github.com/hoshyari_adobe/bazel-playground)

As I was following the tutorials and learning more, I made up these basic examples to get my hands dirty. I think it is valuable for you to also try to setup dummy cases, similar to above, on your own, play with changing things and see how they take effect. What I provide does not have a lot of docs, mainly to showcase how you can setup small independent examples to learn.

## Important Links and Future Reading

- [bazel.build](https://bazel.build/): The reference manual for Bazel. You can pretty much find everything here.
- [registry.bazel.build](https://registry.bazel.build/): Bazel's build registry. Contains list of all available Bazel external modules.

