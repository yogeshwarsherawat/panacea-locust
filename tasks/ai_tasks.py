"""
AI API Tasks for Panacea Locust Load Testing

This module contains AI-related API endpoint tasks.
"""

from locust import task

from config import config
from payloads import PayloadGenerator


class AITaskMixin:
    """Mixin class containing AI-related API endpoint tasks."""

    @task(config.TASK_WEIGHTS["ai_report_summary"])
    def test_ai_report_summary_endpoint(self):
        """Test GET /api/v1/ai/report_summary endpoint."""
        params = payload_generator.get_ai_report_summary_params(self.user_id)
        self._log_request_info("ai/report_summary", "ai_summary", params=params)
        self._make_request("GET", "ai/report_summary", params=params)

    @task(config.TASK_WEIGHTS["ai_ask"])
    def test_ai_ask_endpoint(self):
        """Test POST /api/v1/ai/ask-ai endpoint."""
        payload = payload_generator.generate_ai_ask_payload(self.user_id)
        message_count = len(payload.get("messages", []))
        self._log_request_info(
            "ai/ask-ai",
            "ai_ask",
            params={
                "messages": message_count,
                "sfdc_case": payload.get("sfdc_case_number"),
            },
        )
        self._make_request("POST", "ai/ask-ai", json_data=payload)

    @task(2)  # Medium weight for feedback endpoint
    def test_ai_report_summary_feedback_endpoint(self):
        """Test POST /api/v1/ai/report_summary/feedback endpoint."""
        payload = payload_generator.generate_ai_report_summary_feedback_payload(
            self.user_id
        )
        feedback_status = payload.get("ai_summary_feedback_status", "unknown")
        bundle_info = payload.get("bundle_id") or payload.get("combo_id")
        self._log_request_info(
            "ai/report_summary/feedback",
            "ai_feedback",
            params={
                "status": feedback_status,
                "bundle": bundle_info,
            },
        )
        self._make_request("POST", "ai/report_summary/feedback", json_data=payload)
