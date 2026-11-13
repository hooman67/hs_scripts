## Class to handle get and post requests to evalhub
# Description: This file provides a generic request-response utility for API interactions

import logging
import time
import argparse
import sys
from typing import Any, Dict, Optional, List, NoReturn

import requests
from requests.adapters import (
    HTTPAdapter,
    Retry,
)


class EvalHubRequestResponse:
    def __init__(
        self, base_url: str | None = None, headers: Dict[str, str] | None = None
    ) -> None:
        """EvalHubRequestResponse constructor

        Args:
            base_url (str): Base URL for API requests
            headers (Dict[str, str]): Headers dictionary
        """
        self.session = EvalHubRequestResponse.get_session()

        if base_url is None:
            self.base_url = "https://evaluation-service.adobe.io"
        if headers is None:
            self.headers = {
                "accept": "application/json",
                "x-api-key": "EvalServiceTest",
            }

    @staticmethod
    def get_session(
        num_retries: int = 5,
        backoff: int = 1,
        status_forcelist: list[int] | None = None,
    ) -> requests.Session:
        """Returns a session object with retries included

        Args:
            num_retries (int, optional): # of retries to perform. Defaults to 5.
            backoff (int, optional): Backoff factor. Defaults to 1.
            status_forcelist (list, optional): Status forcelist. Defaults to [404, 429, 500, 502, 503, 504].

        Returns:
            requests.Session: Session with retry configuration
        """
        if status_forcelist is None:
            status_forcelist = [404, 429, 500, 502, 503, 504]
        session = requests.Session()
        retries = Retry(
            total=num_retries, backoff_factor=backoff, status_forcelist=status_forcelist
        )
        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def get(
        self,
        method_path: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """Send a GET request to the specified method path

        Args:
            method_path (str): API method path to append to base URL
            params (Dict[str, Any], optional): Query parameters. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 30.

        Returns:
            Dict[str, Any]: Response data
        """
        url = f"{self.base_url}/{method_path}"
        logging.info(f"GET request to: {url} with params: {params}")

        try:
            response = self.session.get(
                url, params=params, headers=self.headers, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_response = {"error": True, "error_msg": str(e)}
            if hasattr(e, "response") and e.response is not None:
                error_response["status_code"] = e.response.status_code
                try:
                    error_data = e.response.json()
                    if "message" in error_data:
                        error_response["error_msg"] = error_data["message"]
                except Exception:
                    logging.error(f"GET request failed: {error_response}")
                    return error_response
            return error_response

    def post(
        self, method_path: str, payload: Dict[str, Any], timeout: int = 30
    ) -> Dict[str, Any]:
        """Send a POST request to the specified method path

        Args:
            method_path (str): API method path to append to base URL
            payload (Dict[str, Any]): Data to send in the request body
            timeout (int, optional): Request timeout in seconds. Defaults to 30.

        Returns:
            Dict[str, Any]: Response data
        """
        url = f"{self.base_url}/{method_path}"
        logging.info(f"POST request to: {url} with payload: {payload}")

        try:
            response = self.session.post(
                url, json=payload, headers=self.headers, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_response = {"error": True, "error_msg": str(e)}
            if hasattr(e, "response") and e.response is not None:
                error_response["status_code"] = e.response.status_code
                try:
                    error_data = e.response.json()
                    if "message" in error_data:
                        error_response["error_msg"] = error_data["message"]
                except Exception:
                    logging.error(f"POST request failed: {error_response}")
                    return error_response
            logging.error(f"POST request failed: {error_response}")
            return error_response


def get_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Launch evaluation studies")
    parser.add_argument(
        "--run-ids",
        nargs="+",
        required=True,
        help="List of run IDs to launch studies on",
    )
    parser.add_argument(
        "--study-templates",
        nargs="+",
        required=True,
        help="List of study template IDs to use: video-tech-qual, video-motion-quality, video-prompt-coherence, video-temporal-consistency, video-human-tech-qual",
    )
    parser.add_argument(
        "--skip-verification", action="store_true", help="Skip cost verification step"
    )
    return parser.parse_args()


def get_user_confirmation(
    preview_result: Dict[str, Any], run_id: str, template_id: str
) -> bool:
    """Get user confirmation for study launch"""
    print(f"\nPreview for run ID: {run_id} with template: {template_id}")
    print(f"Estimated cost: ${preview_result.get('estimated_cost', 'N/A')}")
    print(
        f"Estimated completion time: {preview_result.get('estimated_completion_time', 'N/A')} hours"
    )

    while True:
        response = (
            input("\nDo you want to proceed with this study? (yes/no): ")
            .lower()
            .strip()
        )
        if response == "yes":
            return True
        elif response == "no":
            return False
        else:
            print("Please enter 'yes' or 'no'")


def main() -> NoReturn:
    """Main function to handle study creation and publishing workflow"""
    args = get_args()
    eval_hub_client = EvalHubRequestResponse()

    # Base payload template
    base_payload = {
        "num_votes_per_asset": 9,
        "num_assets_per_participant": 20,
        "asset_shuffle_seed": int(time.time()),
        "created_by": "hshariati",
        "platform": "prolific",
        "participant_group": "default",
        "shuffle_assets_on_page": True,
    }

    # Store approved combinations for later processing
    approved_studies: List[tuple[str, str]] = []

    # Preview phase
    for run_id in args.run_ids:
        for template_id in args.study_templates:
            preview_payload = base_payload.copy()
            preview_payload.update(
                {
                    "run_ids": [run_id],
                    "study_template_id": template_id,
                }
            )

            # Get preview
            preview_response = eval_hub_client.post(
                method_path="/studies/preview",
                payload=preview_payload,
            )

            if "error" in preview_response and preview_response["error"]:
                print(
                    f"Error getting preview for run ID {run_id}, template {template_id}: {preview_response['error_msg']}"
                )
                continue

            if not args.skip_verification:
                if get_user_confirmation(preview_response, run_id, template_id):
                    approved_studies.append((run_id, template_id))
                else:
                    print(f"Skipping study for run ID {run_id}, template {template_id}")
            else:
                approved_studies.append((run_id, template_id))

    if not approved_studies:
        print("No studies were approved for launch. Exiting.")
        sys.exit(0)

    # Launch phase
    for run_id, template_id in approved_studies:
        # Create study
        create_payload = base_payload.copy()
        create_payload.update(
            {
                "run_ids": [run_id],
                "study_template_id": template_id,
            }
        )

        create_response = eval_hub_client.post(
            method_path="studies",
            payload=create_payload,
        )

        if "error" in create_response and create_response["error"]:
            print(
                f"Error creating study for run ID {run_id}, template {template_id}: {create_response['error_msg']}"
            )
            continue

        study_id = create_response["_id"]
        print(f"Created study with ID: {study_id}")

        # Publish study
        publish_response = eval_hub_client.post(
            method_path=f"/studies/{study_id}/publish",
            payload={},
        )

        if "error" in publish_response and publish_response["error"]:
            print(f"Error publishing study {study_id}: {publish_response['error_msg']}")
        else:
            print(f"Successfully published study {study_id}")


if __name__ == "__main__":
    main()
