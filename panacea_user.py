"""
Base User Module for Panacea Locust Load Testing

This module contains the base PanaceaAPIUser class with core functionality
for session management, request handling, and user initialization.
"""

import logging
import random
import time
from typing import Any, Dict

from locust import HttpUser, between, task

from config import config
from payloads.json_payload import json_payload

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PanaceaAPIUser(HttpUser):
    """
    Base virtual user for testing Panacea API endpoints.
    Each user has unique session ID and user-specific payload generation.

    This class provides:
    - User initialization and data pool registration
    - Session management with X-Session-Id headers
    - Common HTTP request handling with error management
    - Base configuration for wait times and weights
    """

    wait_time = between(config.STANDARD_USER_WAIT_MIN, config.STANDARD_USER_WAIT_MAX)
    weight = config.STANDARD_USER_WEIGHT

    def __init__(self, *args, **kwargs):
        """Initialize the user class, ensuring parent classes are properly initialized."""
        super().__init__(*args, **kwargs)

    def on_start(self):
        """Initialize user-specific data when the user starts."""
        # Generate unique user identifier
        self.session_id = "cf811e567c5d42e9bd61a3562ecdd29f"

        # Set up session headers
        self._setup_session()

        logger.info(f"User started with session {self.session_id}")

    def _setup_session(self):
        """Set up session headers and authentication."""
        self.client.headers.update(
            {
                config.SESSION_HEADER_NAME: self.session_id,
                "Content-Type": "application/json",
                "User-Agent": f"PanaceaLocust/1.0",
            }
        )

        logger.info(f"Client headers: {self.client.headers}")

        logger.info(f"Session headers set with session_id: {self.session_id}")

    def make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
        name: str = None,
    ):
        """
        Make an HTTP request with optional name for Locust statistics grouping.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: JSON payload for POST requests
            params: Query parameters for GET requests
            name: Optional name to group requests in Locust statistics (defaults to endpoint)
        """
        if name is None:
            # Use endpoint as default name, removing query params for grouping
            name = endpoint.split("?")[0] if "?" in endpoint else endpoint

        if method == "POST":
            self.client.post(endpoint, json=json_data, params=params, name=name)
        elif method == "GET":
            self.client.get(endpoint, params=params, name=name)
        else:
            raise ValueError(f"Invalid method: {method}")

    @task(config.TASK_WEIGHTS["reports"])
    def test_reports_endpoint(self):
        from payloads.api_payloads.reports_api import ReportsAPI

        logger.info(f"Session ID: {self.session_id}")
        api = ReportsAPI()
        payload = api.generate_payload("default")
        # Randomly select a payload type
        payload_types = [
            "default",
            "page_2",
            "case_owner_email",
            "sfdc_case_number",
            "case_owner_email_and_sfdc_case_number",
        ]
        payload_type = random.choice(payload_types)
        # Generate payload
        payload = api.generate_payload(payload_type)

        logger.info(
            f"Sending request to {api.get_api_endpoint()} with payload {payload}"
        )
        self.make_request(
            api.get_api_method(), api.get_api_endpoint(), json_data=payload
        )

    @task(config.TASK_WEIGHTS["reports"])
    def test_list_combos_endpoint(self):
        from payloads.api_payloads.list_combos import ListCombosAPI

        logger.info(f"Session ID: {self.session_id}")
        api = ListCombosAPI()
        payload = api.generate_payload("default")
        # Randomly select a payload type
        payload_types = [
            "default",
            "page_2",
            "case_owner_email",
            "sfdc_case_number",
            "case_owner_email_and_sfdc_case_number",
        ]
        payload_type = random.choice(payload_types)
        # Generate payload
        payload = api.generate_payload(payload_type)

        logger.info(
            f"Sending request to {api.get_api_endpoint()} with payload {payload}"
        )
        self.make_request(
            api.get_api_method(), api.get_api_endpoint(), json_data=payload
        )

    @task(config.TASK_WEIGHTS["events"])
    def test_events_endpoint(self):
        from payloads.api_payloads.events import EventsAPI

        logger.info(f"Session ID: {self.session_id}")
        api = EventsAPI()
        # Randomly select a payload type
        payload_types = [
            "default",
            "combo_id_only",
            "combo_id_with_curated",
            "bundle_id_with_curated",
        ]
        payload_type = random.choice(payload_types)
        # Generate payload (query parameters for GET request)
        payload = api.generate_payload(payload_type)

        logger.info(
            f"Sending request to {api.get_api_endpoint()} with params {payload}"
        )
        # For GET requests, pass payload as params instead of json_data
        # Use a consistent name to group all events requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            params=payload,
            name="/api/v1/insights/events",
        )
