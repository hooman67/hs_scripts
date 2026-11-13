#!/usr/bin/env python3
"""
Script to test VLLM server requests and debug issues.
This script replicates the curl command and provides detailed debugging information.
"""

import requests
import json
import time
from typing import Dict, Any, Optional
import sys

def make_vllm_request(
    url: str,
    messages: list,
    sampling_params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Make a request to the VLLM server with detailed logging.
    
    Args:
        url: The VLLM server endpoint URL
        messages: List of message objects with role and content
        sampling_params: Optional sampling parameters
        headers: Optional custom headers
        timeout: Request timeout in seconds
        verbose: Whether to print detailed information
    
    Returns:
        Dictionary containing response data and metadata
    """
    
    # Default sampling parameters (from your curl command)
    default_sampling_params = {
        "n": 1,
        "presencePenalty": 0,
        "frequencyPenalty": 0,
        "repetitionPenalty": 1,
        "temperature": 0.1,
        "topP": 1,
        "topK": -1,
        "minP": 0,
        "seed": 42,
        "includeStopStrInOutput": False,
        "ignoreEos": False,
        "maxTokens": 2048,
        "minTokens": 0,
        "detokenize": True,
        "skipSpecialTokens": True,
        "spacesBetweenSpecialTokens": True
    }
    
    # Default headers (from your curl command)
    default_headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://pluto-prod-hshariati-colligo-vllm-7yr2d4-1-0-8000.colligo.dev',
        'Referer': 'https://pluto-prod-hshariati-colligo-vllm-7yr2d4-1-0-8000.colligo.dev/debug/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'x-request-id': f'python-{int(time.time())}'
    }
    
    # Merge with provided headers
    if headers:
        default_headers.update(headers)
    
    # Merge with provided sampling params
    if sampling_params:
        default_sampling_params.update(sampling_params)
    
    # Prepare the request payload
    payload = {
        "samplingParams": default_sampling_params,
        "messages": messages
    }
    
    if verbose:
        print("=" * 60)
        print("VLLM REQUEST DEBUG INFO")
        print("=" * 60)
        print(f"URL: {url}")
        print(f"Method: POST")
        print(f"Timeout: {timeout}s")
        print("\nHeaders:")
        for key, value in default_headers.items():
            print(f"  {key}: {value}")
        
        print("\nPayload:")
        print(json.dumps(payload, indent=2))
        print("\n" + "=" * 60)
    
    try:
        # Make the request
        start_time = time.time()
        response = requests.post(
            url,
            headers=default_headers,
            json=payload,
            timeout=timeout
        )
        end_time = time.time()
        
        if verbose:
            print(f"Response Status: {response.status_code}")
            print(f"Response Time: {end_time - start_time:.2f}s")
            print(f"Response Headers:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")
        
        # Try to parse JSON response
        try:
            response_json = response.json()
            if verbose:
                print(f"\nResponse Body (JSON):")
                print(json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            if verbose:
                print(f"\nResponse Body (Raw):")
                print(response.text)
            response_json = {"raw_response": response.text}
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response_time": end_time - start_time,
            "headers": dict(response.headers),
            "data": response_json,
            "raw_text": response.text
        }
        
    except requests.exceptions.Timeout:
        error_msg = f"Request timed out after {timeout} seconds"
        if verbose:
            print(f"ERROR: {error_msg}")
        return {"success": False, "error": error_msg}
    
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection error: {str(e)}"
        if verbose:
            print(f"ERROR: {error_msg}")
        return {"success": False, "error": error_msg}
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        if verbose:
            print(f"ERROR: {error_msg}")
        return {"success": False, "error": error_msg}

def test_connection(url: str) -> bool:
    """Test basic connectivity to the URL."""
    try:
        response = requests.get(url, timeout=10)
        return True
    except:
        return False

def main():
    """Main function to test the VLLM request."""
    
    # Your original request details
    url = "https://pluto-prod-hshariati-colligo-vllm-7yr2d4-1-0-8000.colligo.dev/v1/vllm_serve/OpenGVLab/InternVL3-38B"
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "date?"}
    ]
    
    print("Testing VLLM Server Request")
    print("=" * 60)
    
    # Test 1: Basic connectivity
    print("1. Testing basic connectivity...")
    if test_connection(url):
        print("✓ Server is reachable")
    else:
        print("✗ Server is not reachable")
        print("This might be a network issue or the server is down.")
        return
    
    # Test 2: Original request
    print("\n2. Making original request...")
    result = make_vllm_request(url, messages, verbose=True)
    
    if result["success"]:
        print("\n✓ Request successful!")
        if "data" in result and "raw_response" not in result["data"]:
            # Try to extract the actual response content
            response_data = result["data"]
            if "choices" in response_data:
                for i, choice in enumerate(response_data["choices"]):
                    if "message" in choice and "content" in choice["message"]:
                        print(f"Response {i+1}: {choice['message']['content']}")
            elif "output" in response_data:
                print(f"Response: {response_data['output']}")
            else:
                print("Response structure:", json.dumps(response_data, indent=2))
    else:
        print(f"\n✗ Request failed: {result.get('error', 'Unknown error')}")
        
        # Test 3: Try with minimal headers
        print("\n3. Trying with minimal headers...")
        minimal_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Python-requests/2.31.0'
        }
        result2 = make_vllm_request(url, messages, headers=minimal_headers, verbose=True)
        
        if result2["success"]:
            print("✓ Request with minimal headers successful!")
        else:
            print(f"✗ Request with minimal headers also failed: {result2.get('error', 'Unknown error')}")
            
            # Test 4: Try GET request to see if endpoint exists
            print("\n4. Testing GET request to endpoint...")
            try:
                get_response = requests.get(url, timeout=10)
                print(f"GET response status: {get_response.status_code}")
                print(f"GET response: {get_response.text[:200]}...")
            except Exception as e:
                print(f"GET request failed: {e}")

if __name__ == "__main__":
    main()
