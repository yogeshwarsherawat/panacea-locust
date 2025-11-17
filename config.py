"""
Configuration module for Panacea Locust Load Testing

This module contains all configuration settings for the load testing framework.
Settings can be overridden via environment variables.
"""

import os

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

    # Wait Time Configuration (in seconds)
    STANDARD_USER_WAIT_MIN = float(os.getenv("STANDARD_WAIT_MIN", "1.0"))
    STANDARD_USER_WAIT_MAX = float(os.getenv("STANDARD_WAIT_MAX", "3.0"))

    # User Distribution Weights
    STANDARD_USER_WEIGHT = int(os.getenv("STANDARD_USER_WEIGHT", "5"))

    # Session Configuration
    SESSION_ID_LENGTH = int(os.getenv("SESSION_ID_LENGTH", "32"))
    SESSION_HEADER_NAME = "X-Session-Id"

    # ClickHouse Configuration
    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "9000"))
    CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "panacea")
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "panacea")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "panacea")

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
        "reports": 0,
        "list-combos": 1,
        "events": 1,
        "ask-ai": 1,
        "report-summary": 1,
        "logs-info": 1,
        "logs-filter-options": 1,
        "logs-search": 1,
        "logs-histogram": 1,
        "logs-heatmap": 1,
        "logs-severity-count": 1,
    }

    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration values."""
        try:
            assert cls.SESSION_ID_LENGTH > 0
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
print(payload_config.PAYLOAD_JSON_FILE_PATH)