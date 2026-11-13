#!/usr/bin/env python3
"""Construct the real gateway OpenAI client without issuing a model request."""

from __future__ import annotations

import importlib.metadata as metadata

import foundry_aws_gateway.llm
import types_boto3_bedrock_runtime


def main() -> None:
    client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=540.0)
    if client.__class__.__name__ != "OpenAI":
        raise RuntimeError(f"unexpected provider client: {client.__class__.__name__}")
    if not types_boto3_bedrock_runtime.__file__:
        raise RuntimeError("types_boto3_bedrock_runtime has no import path")
    print(f"gateway_version={metadata.version('foundry-aws-gateway')}")
    print(f"bedrock_types_version={metadata.version('types-boto3-bedrock-runtime')}")
    print(f"provider_client={client.__class__.__name__}")
    print("model_request_made=false")


if __name__ == "__main__":
    main()
