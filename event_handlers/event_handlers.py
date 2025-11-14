"""
Event Handlers for Panacea Locust Load Testing

This module contains event handlers for monitoring, logging, and managing
the lifecycle of Locust load tests.
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict

from locust import events

from config import config

# Configure logging
logger = logging.getLogger(__name__)


class TestMetrics:
    """Class to track and manage test metrics throughout the test lifecycle."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_users_registered = 0
        self.user_stats = {}
        self.test_config = {}

    def record_user_registration(self, user_id: str, user_stats: Dict[str, Any]):
        """Record user registration and stats."""
        self.total_users_registered += 1
        self.user_stats[user_id] = user_stats
        logger.debug(f"Recorded stats for user {user_id}")

    def get_summary(self) -> Dict[str, Any]:
        """Get test summary statistics."""
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()

        return {
            "test_duration_seconds": duration,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_users_registered": self.total_users_registered,
            "config": self.test_config,
            "user_distribution": self._get_user_distribution_stats(),
            "bundle_id_coverage": self._get_bundle_id_coverage(),
        }

    def _get_user_distribution_stats(self) -> Dict[str, Any]:
        """Get statistics about user distribution."""
        bundle_ranges = []
        combo_ranges = []

        for stats in self.user_stats.values():
            if "bundle_id_range" in stats:
                bundle_ranges.append(stats["bundle_id_range"])
            if "combo_id_range" in stats:
                combo_ranges.append(stats["combo_id_range"])

        return {
            "total_users": len(self.user_stats),
            "bundle_ranges_count": len(bundle_ranges),
            "combo_ranges_count": len(combo_ranges),
            "bundle_ranges": bundle_ranges[:10],  # First 10 for brevity
            "combo_ranges": combo_ranges[:10],  # First 10 for brevity
        }

    def _get_bundle_id_coverage(self) -> Dict[str, Any]:
        """Get statistics about bundle ID coverage across users."""
        return {}


# Global metrics instance
test_metrics = TestMetrics()


def on_test_start(environment, **kwargs):
    """
    Called when the test starts.

    Args:
        environment: Locust environment object
        **kwargs: Additional keyword arguments
    """
    logger.info("On test start")
    logger.info("Json Payload loading into memory")
    start_time = time.time()
    from payloads.json_payload import json_payload

    logger.info(
        f"Json Payload loaded into memory in {time.time() - start_time} seconds"
    )

    test_metrics.start_time = datetime.utcnow()

    # Record test configuration
    test_metrics.test_config = {
        "host": environment.host,
        "user_count": getattr(environment, "user_count", "unknown"),
        "spawn_rate": getattr(environment, "spawn_rate", "unknown"),
        "run_time": getattr(environment, "run_time", "unknown"),
        "session_id_length": config.SESSION_ID_LENGTH,
    }

    logger.info("=" * 60)
    logger.info("🚀 PANACEA API LOAD TEST STARTING")
    logger.info("=" * 60)
    logger.info(f"Target Host: {environment.host}")
    logger.info("=" * 60)


def on_test_stop(environment, **kwargs):
    """
    Called when the test stops.

    Args:
        environment: Locust environment object
        **kwargs: Additional keyword arguments
    """
    test_metrics.end_time = datetime.utcnow()

    logger.info("=" * 60)
    logger.info("🏁 PANACEA API LOAD TEST COMPLETED")
    logger.info("=" * 60)
    logger.info(f"Total Users Registered: {test_metrics.total_users_registered}")

    # Get test summary
    summary = test_metrics.get_summary()

    if summary["test_duration_seconds"]:
        logger.info(f"Test Duration: {summary['test_duration_seconds']:.2f} seconds")

    # Save test summary to file
    _save_test_summary(summary)

    logger.info("=" * 60)


def on_spawning_complete(*args, **kwargs):
    """
    Called when all users have been spawned.

    Args:
        *args: Positional arguments (may contain environment as first arg)
        **kwargs: Keyword arguments (may contain 'environment' as kwarg)
    """
    # Handle both cases: environment as positional arg or as keyword arg
    environment = None
    if args:
        environment = args[0]
    elif "environment" in kwargs:
        environment = kwargs["environment"]

    if environment is None:
        logger.warning("on_spawning_complete called without environment parameter")
        return

    user_count = getattr(environment, "user_count", 0)
    test_metrics.total_users_registered = user_count

    logger.info(f"👥 All {user_count} users have been spawned successfully")


def on_request(
    request_type,
    name,
    response_time,
    response_length,
    response=None,
    context=None,
    exception=None,
    **kwargs,
):
    """
    Called for every request (success or failure).

    Args:
        request_type: HTTP method (GET, POST, etc.)
        name: Request name
        response_time: Response time in milliseconds
        response_length: Response content length
        response: Response object (if successful)
        context: Request context
        exception: Exception that caused the failure (if failed)
        **kwargs: Additional keyword arguments
    """
    if exception:
        logger.warning(
            f"❌ {request_type} {name} - {response_time}ms - Error: {exception}"
        )
    else:
        logger.debug(
            f"✅ {request_type} {name} - {response_time}ms - {response_length} bytes"
        )


def _save_test_summary(summary: Dict[str, Any]):
    """
    Save test summary to a JSON file.

    Args:
        summary: Test summary dictionary
    """
    try:
        # Create results directory if it doesn't exist
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"test_summary_{timestamp}.json"
        filepath = os.path.join(results_dir, filename)

        # Save summary to file
        with open(filepath, "w") as f:
            json.dump(summary, f, indent=2, default=str)

        logger.info(f"📊 Test summary saved to: {filepath}")

    except Exception as e:
        logger.error(f"Failed to save test summary: {e}")


def setup_event_handlers():
    """
    Register all event handlers with Locust.
    Call this function to set up event monitoring.
    """
    events.test_start.add_listener(on_test_start)
    events.test_stop.add_listener(on_test_stop)
    events.spawning_complete.add_listener(on_spawning_complete)
    events.request.add_listener(on_request)

    logger.info("🔧 Event handlers registered successfully")
