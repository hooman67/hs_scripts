# MFM Masking Pipelines

This directory contains the Masking Foundation Model based pipeline. for the DI Imaging project.

## Structure
    .
    ├── adapters                # API Class to Pipeline Class Adapters
    ├── components              # Entrypoint of different components in the pipeline
    ├── pipelines               # Pipeline classes
    ├── test                    # Unit tests for components and pipelines
    ├── types                   # Class definitions
    ├── build.py                # Build pipeline and API
    └── colligo.yaml            # Dependencies and public interfaces

## Steps to add new head

* Add model worker outside of `mfm_masking` directory
* Update component in `/components` to invoke the model worker
* Add pipeline in `/pipelines` to orchestrate the components
* Add build step in `build.py` to build the pipeline
* Add tests in `/test` to test the pipeline and component
* Add type definitions in `/types` for classes and interfaces
* Add adapter in `/adapters` to trasform API request to pipeline request, also response
