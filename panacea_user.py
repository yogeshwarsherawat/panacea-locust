"""
Base User Module for Panacea Locust Load Testing

This module contains the base PanaceaAPIUser class with core functionality
for session management, request handling, and user initialization.
"""

import json
import logging
import random
from typing import Any, Dict

from locust import HttpUser, between, task
from payloads.json_payload import json_payload

from config import config

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
        self.session_id = random.choice(json_payload.get_session_ids())
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

    def _log_curl_command(
        self,
        method: str,
        endpoint: str,
        json_data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ):
        """
        Log curl command randomly (10% chance) for debugging purposes.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: JSON payload for POST requests
            params: Query parameters for GET requests
        """
        # Log curl command 10% of the time
        if random.random() < 0.1:
            curl_parts = [f"curl -X {method} '{endpoint}'"]
            curl_parts.append(f"-H '{config.SESSION_HEADER_NAME}: {self.session_id}'")
            curl_parts.append("-H 'Content-Type: application/json'")

            if method == "POST" and json_data:
                curl_parts.append(f"-d '{json.dumps(json_data)}'")
            elif method == "GET" and params:
                # Build query string for GET requests
                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                # Append query string to URL
                separator = "&" if "?" in endpoint else "?"
                curl_parts[0] = (
                    f"curl -X {method} '{endpoint}{separator}{query_string}'"
                )

            curl_command = " \\\n  ".join(curl_parts)
            logger.info(f"CURL command:\n{curl_command}")

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

        # Log curl command randomly (10% chance)
        self._log_curl_command(method, endpoint, json_data, params)

        if method == "POST":
            self.client.post(endpoint, json=json_data, params=params, name=name)
        elif method == "GET":
            self.client.get(endpoint, params=params, name=name)
        else:
            raise ValueError(f"Invalid method: {method}")

    @task(config.TASK_WEIGHTS["reports"])
    def test_reports_endpoint(self):
        from payloads.api_payloads.reports.reports_api import ReportsAPI

        logger.info(f"Session ID: {self.session_id}")
        api = ReportsAPI()
        # Generate payload with random selection handled by the API
        payload = api.generate_payload()

        self.make_request(
            api.get_api_method(), api.get_api_endpoint(), json_data=payload
        )

    @task(config.TASK_WEIGHTS["list-combos"])
    def test_list_combos_endpoint(self):
        from payloads.api_payloads.reports.list_combos import ListCombosAPI

        logger.info(f"Session ID: {self.session_id}")
        api = ListCombosAPI()
        # Generate payload with random selection handled by the API
        payload = api.generate_payload()

        self.make_request(
            api.get_api_method(), api.get_api_endpoint(), json_data=payload
        )

    @task(config.TASK_WEIGHTS["events"])
    def test_events_endpoint(self):
        from payloads.api_payloads.rca_summary.events import EventsAPI

        logger.info(f"Session ID: {self.session_id}")
        api = EventsAPI()
        # Generate payload with random selection handled by the API (query parameters for GET request)
        payload = api.generate_payload()

        # For GET requests, pass payload as params instead of json_data
        # Use a consistent name to group all events requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            params=payload,
            name="/api/v1/insights/events",
        )

    @task(config.TASK_WEIGHTS["ask-ai"])
    def test_ask_ai_endpoint(self):
        from payloads.api_payloads.rca_summary.ask_ai import AskAIAPI

        logger.info(f"Session ID: {self.session_id}")
        api = AskAIAPI()
        # Generate payload with random selection handled by the API
        payload = api.generate_payload()

        self.make_request(
            api.get_api_method(), api.get_api_endpoint(), json_data=payload
        )

    @task(config.TASK_WEIGHTS["report-summary"])
    def test_report_summary_endpoint(self):
        from payloads.api_payloads.rca_summary.ai_summary import AISummaryAPI

        logger.info(f"Session ID: {self.session_id}")
        api = AISummaryAPI()
        # Generate payload with random selection handled by the API (query parameters for GET request)
        payload = api.generate_payload()

        # For GET requests, pass payload as params instead of json_data
        # Use a consistent name to group all report_summary requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            params=payload,
            name="/api/v1/insights/ai/report_summary",
        )

    @task(config.TASK_WEIGHTS["logs-info"])
    def test_logs_info_endpoint(self):
        from payloads.api_payloads.rca_summary.logs_info import LogsInfoAPI

        logger.info(f"Session ID: {self.session_id}")
        api = LogsInfoAPI()
        # Generate payload with random selection handled by the API (query parameters for GET request)
        payload = api.generate_payload()

        # For GET requests, pass payload as params instead of json_data
        # Use a consistent name to group all logs_info requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            params=payload,
            name="/api/v1/insights/logs/info",
        )

    @task(config.TASK_WEIGHTS["logs-filter-options"])
    def test_logs_filter_options_endpoint(self):
        from payloads.api_payloads.log_viewer.filter_options import LogsFilterOptionsAPI

        logger.info(f"Session ID: {self.session_id}")
        api = LogsFilterOptionsAPI()
        # Generate payload with random selection handled by the API (query parameters for GET request)
        payload = api.generate_payload()

        # For GET requests, pass payload as params instead of json_data
        # Use a consistent name to group all logs_filter_options requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            params=payload,
            name="/api/v1/insights/logs/filter-options",
        )

    @task(config.TASK_WEIGHTS["logs-search"])
    def test_logs_search_endpoint(self):
        from payloads.api_payloads.log_viewer.search import LogsSearchAPI

        logger.info(f"Session ID: {self.session_id}")
        api = LogsSearchAPI()
        # Generate payload with random selection handled by the API
        payload = api.generate_payload()

        # For POST requests, pass payload as json_data
        # Use a consistent name to group all logs_search requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            json_data=payload,
            name="/api/v1/insights/logs/search/",
        )

    @task(config.TASK_WEIGHTS["logs-histogram"])
    def test_logs_histogram_endpoint(self):
        from payloads.api_payloads.log_viewer.histogram import LogsHistogramAPI

        logger.info(f"Session ID: {self.session_id}")
        api = LogsHistogramAPI()
        # Generate payload with random selection handled by the API
        payload = api.generate_payload()

        # For POST requests, pass payload as json_data
        # Use a consistent name to group all logs_histogram requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            json_data=payload,
            name="/api/v1/insights/logs/histogram/",
        )

    @task(config.TASK_WEIGHTS["logs-heatmap"])
    def test_logs_heatmap_endpoint(self):
        from payloads.api_payloads.log_viewer.heatmap import LogsHeatmapAPI

        logger.info(f"Session ID: {self.session_id}")
        api = LogsHeatmapAPI()
        # Generate payload with random selection handled by the API
        payload = api.generate_payload()

        # For POST requests, pass payload as json_data
        # Use a consistent name to group all logs_heatmap requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            json_data=payload,
            name="/api/v1/insights/logs/heatmap/",
        )

    @task(config.TASK_WEIGHTS["logs-severity-count"])
    def test_logs_severity_count_endpoint(self):
        from payloads.api_payloads.log_viewer.severity_count import LogsSeverityCountAPI

        logger.info(f"Session ID: {self.session_id}")
        api = LogsSeverityCountAPI()
        # Generate payload with random selection handled by the API
        payload = api.generate_payload()

        # For POST requests, pass payload as json_data
        # Use a consistent name to group all logs_severity_count requests together in Locust stats
        self.make_request(
            api.get_api_method(),
            api.get_api_endpoint(),
            json_data=payload,
            name="/api/v1/insights/logs/severity-count/",
        )
