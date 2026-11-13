#!/usr/bin/env python3
"""
Simple script to test VLLM requests with minimal dependencies.
"""

import requests
import json

def test_vllm():
    url = "https://pluto-prod-hshariati-colligo-vllm-7yr2d4-1-0-8000.colligo.dev/v1/vllm_serve/OpenGVLab/InternVL3-38B"
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Python-requests/2.31.0'
    }
    
    data = {
        "samplingParams": {
            "n": 1,
            "temperature": 0.1,
            "maxTokens": 2048,
            "seed": 42
        },
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the current date?"}
        ]
    }
    
    print("Making request to VLLM server...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=2)}")
            except:
                print("Response is not valid JSON")
        else:
            print(f"Request failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_vllm()
