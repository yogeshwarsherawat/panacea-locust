"""
Database package for Panacea Locust Load Testing
"""

from .clickhouse_dao import ClickHouseDAO

# Create a global instance
clickhouse_dao = ClickHouseDAO()

__all__ = ["ClickHouseDAO", "clickhouse_dao"]
