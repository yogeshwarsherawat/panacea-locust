"""
Configuration module for Panacea Locust Load Testing

This module contains all configuration settings for the load testing framework.
Settings can be overridden via environment variables.
"""

import os
from typing import Any, Dict, List

# Try to load .env file if available
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass


class Config:
    """Configuration class for Panacea Locust load testing."""

    # API Configuration
    DEFAULT_HOST = os.getenv("PANACEA_HOST", "http://10.113.24.33:9898")
    API_VERSION = "v1"
    BASE_PATH = f"/api/{API_VERSION}"

    # User Configuration
    MIN_USERS = int(os.getenv("LOCUST_MIN_USERS", "1"))
    MAX_USERS = int(os.getenv("LOCUST_MAX_USERS", "100"))
    SPAWN_RATE = float(os.getenv("LOCUST_SPAWN_RATE", "2"))

    # Wait Time Configuration (in seconds)
    STANDARD_USER_WAIT_MIN = float(os.getenv("STANDARD_WAIT_MIN", "1.0"))
    STANDARD_USER_WAIT_MAX = float(os.getenv("STANDARD_WAIT_MAX", "3.0"))

    # User Distribution Weights
    STANDARD_USER_WEIGHT = int(os.getenv("STANDARD_USER_WEIGHT", "5"))

    # Bundle ID Configuration
    BUNDLE_ID_MIN = int(os.getenv("BUNDLE_ID_MIN", "800"))
    BUNDLE_ID_MAX = int(os.getenv("BUNDLE_ID_MAX", "1000"))
    BUNDLE_ID_RANGE_PER_USER = int(os.getenv("BUNDLE_ID_RANGE_PER_USER", "50"))
    BUNDLE_ID_OVERLAP_PERCENTAGE = float(
        os.getenv("BUNDLE_ID_OVERLAP_PERCENTAGE", "0.3")
    )

    # Combo ID Configuration
    COMBO_ID_MIN = int(os.getenv("COMBO_ID_MIN", "1"))
    COMBO_ID_MAX = int(os.getenv("COMBO_ID_MAX", "100"))
    COMBO_ID_RANGE_PER_USER = int(os.getenv("COMBO_ID_RANGE_PER_USER", "20"))

    # SFDC Case Configuration
    SFDC_CASE_MIN = int(os.getenv("SFDC_CASE_MIN", "10000000"))
    SFDC_CASE_MAX = int(os.getenv("SFDC_CASE_MAX", "99999999"))

    # User Pool Configuration
    USER_POOL_SIZE = int(os.getenv("USER_POOL_SIZE", "1000"))
    USER_ID_PREFIX = os.getenv("USER_ID_PREFIX", "loadtest_user")

    # Session Configuration
    SESSION_ID_LENGTH = int(os.getenv("SESSION_ID_LENGTH", "32"))
    SESSION_HEADER_NAME = "X-Session-Id"

    # ClickHouse Configuration
    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "panacea-clickhouse.cpaasonprem.com")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "9000"))
    CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "panacea")
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "panacea_user")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "qwerty")

    # Database Integration Settings
    USE_DATABASE_DATA = os.getenv("USE_DATABASE_DATA", "false").lower() == "true"
    DB_USERS_LIMIT = int(os.getenv("DB_USERS_LIMIT", "1000"))
    DB_BUNDLE_IDS_LIMIT = int(os.getenv("DB_BUNDLE_IDS_LIMIT", "500"))
    DB_COMBO_IDS_LIMIT = int(os.getenv("DB_COMBO_IDS_LIMIT", "100"))
    DB_SFDC_CASES_LIMIT = int(os.getenv("DB_SFDC_CASES_LIMIT", "200"))

    # Request Configuration
    REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "30.0"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

    # Payload Configuration
    MAX_BUNDLE_IDS_PER_REQUEST = int(os.getenv("MAX_BUNDLE_IDS_PER_REQUEST", "5"))
    MAX_LOG_MESSAGES_PER_REQUEST = int(os.getenv("MAX_LOG_MESSAGES_PER_REQUEST", "10"))

    # Time Range Configuration (in hours)
    DEFAULT_TIME_RANGE_HOURS = int(os.getenv("DEFAULT_TIME_RANGE_HOURS", "24"))
    MAX_TIME_RANGE_HOURS = int(os.getenv("MAX_TIME_RANGE_HOURS", "168"))  # 1 week

    # Pagination Configuration
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
    MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))
    MAX_PAGE_NUMBER = int(os.getenv("MAX_PAGE_NUMBER", "10"))

    # Task Weight Configuration
    TASK_WEIGHTS = {
        "reports": 1,
        "list-combos": 1,
        "events": 1,
        "ask-ai": 1,
        "report-summary": 1,
        "logs-info": 1,
        "logs-filter-options": 1,
    }

    PROD_TASK_WEIGHTS = {
        "reports": 5,
        "list-combos": 3,
        "events": 1,
        "ask-ai": 1,
        "report-summary": 1,
        "logs-info": 1,
        "logs-filter-options": 1,
    }

    # Network Configuration
    IP_RANGES = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]

    @classmethod
    def get_api_endpoint(cls, endpoint: str) -> str:
        """Get full API endpoint URL."""
        return f"{cls.BASE_PATH}/{endpoint.lstrip('/')}"

    @classmethod
    def get_bundle_id_range(cls, user_index: int) -> tuple:
        """Get bundle ID range for a specific user."""
        start = cls.BUNDLE_ID_MIN + (user_index * cls.BUNDLE_ID_RANGE_PER_USER)
        end = min(start + cls.BUNDLE_ID_RANGE_PER_USER, cls.BUNDLE_ID_MAX)

        # Add overlap with other users
        overlap_size = int(
            cls.BUNDLE_ID_RANGE_PER_USER * cls.BUNDLE_ID_OVERLAP_PERCENTAGE
        )
        start = max(cls.BUNDLE_ID_MIN, start - overlap_size)
        end = min(cls.BUNDLE_ID_MAX, end + overlap_size)

        return (start, end)

    @classmethod
    def get_combo_id_range(cls, user_index: int) -> tuple:
        """Get combo ID range for a specific user."""
        start = cls.COMBO_ID_MIN + (user_index * cls.COMBO_ID_RANGE_PER_USER)
        end = min(start + cls.COMBO_ID_RANGE_PER_USER, cls.COMBO_ID_MAX)
        return (start, end)

    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration values."""
        try:
            assert cls.BUNDLE_ID_MIN < cls.BUNDLE_ID_MAX
            assert cls.COMBO_ID_MIN < cls.COMBO_ID_MAX
            assert cls.SFDC_CASE_MIN < cls.SFDC_CASE_MAX
            assert 0 <= cls.BUNDLE_ID_OVERLAP_PERCENTAGE <= 1
            assert cls.SESSION_ID_LENGTH > 0
            assert cls.USER_POOL_SIZE > 0
            return True
        except AssertionError:
            return False


# Global configuration instance
config = Config()

# Validate configuration on import
if not config.validate_config():
    raise ValueError(
        "Invalid configuration detected. Please check environment variables."
    )


class PayloadConfig:
    PAYLOAD_JSON_FILE_PATH = os.getenv(
        "PAYLOAD_JSON_FILE_PATH",
        os.path.join(os.path.dirname(__file__), "payload.json"),
    )
    NO_OF_CASE_OWNER_EMAILS_REQUIRED = 10
    NO_OF_SFDC_CASE_NUMBERS_REQUIRED = 10


payload_config = PayloadConfig()
