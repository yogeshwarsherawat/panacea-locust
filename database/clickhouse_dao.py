"""
ClickHouse DAO for Panacea Locust Load Testing

This module provides database access for fetching real user and session data
from ClickHouse to make load testing more realistic.
"""

import logging
import os
from typing import Dict, List, Optional, Tuple

from clickhouse_driver import Client

# Configure logging
logger = logging.getLogger(__name__)


class ClickHouseDAO:
    """
    ClickHouse Data Access Object for fetching user and session data.

    This class provides methods to fetch real user IDs and session IDs
    from the ClickHouse database to make load testing more realistic.
    """

    def __init__(self):
        """Initialize ClickHouse connection."""
        self.host = os.getenv("CLICKHOUSE_HOST", "localhost")
        self.port = int(os.getenv("CLICKHOUSE_PORT", "9000"))
        self.database = os.getenv("CLICKHOUSE_DATABASE", "panacea_system")
        self.user = os.getenv("CLICKHOUSE_USER", "default")
        self.password = os.getenv("CLICKHOUSE_PASSWORD", "")

        # Connection settings
        self.settings = {
            "use_numpy": False,
            "max_execution_time": 30,
            "send_receive_timeout": 30,
        }

        self._client = None

        logger.info(
            f"ClickHouse DAO initialized for {self.host}:{self.port}/{self.database}"
        )

    def _get_client(self) -> Client:
        """
        Get or create ClickHouse client connection.

        Returns:
            ClickHouse client instance
        """
        if self._client is None:
            try:
                self._client = Client(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    settings=self.settings,
                )

                # Test connection
                self._client.execute("SELECT 1")
                logger.info("ClickHouse connection established successfully")

            except Exception as e:
                logger.error(f"Failed to connect to ClickHouse: {str(e)}")
                raise

        return self._client

    def get_users_and_sessions(self, limit: int = 1000) -> Dict[str, str]:
        """
        Fetch active user IDs and their session IDs from ClickHouse.

        This method queries the database to get real user and session data
        that can be used for realistic load testing.

        Args:
            limit: Maximum number of user-session pairs to fetch

        Returns:
            Dictionary mapping user_id to session_id: {'user_id': 'session_id'}

        Raises:
            Exception: If database query fails
        """

        client = self._get_client()

        # Query to get active users and their sessions
        # This is a sample query - adjust based on your actual schema
        query = """
                     SELECT
                            u.id AS user_id,
                            s.session_id
                        FROM panacea.nu_users AS u
                        INNER JOIN panacea.nu_sessions AS s
                            ON u.id = s.user_id
                        WHERE s.expires_at > now();

            """

        logger.info(f"Fetching users and sessions with limit: {limit}")

        # Execute query
        result = client.execute(query, {"limit": limit})

        user_id_to_session_id = {result[0]: result[1] for result in result}

        return user_id_to_session_id

    def get_valid_log_bundle_ids(self, limit: int = 20) -> List[int]:
        client = self._get_client()
        query = f"select id from panacea.nu_metadata where is_deleted=0 order by rand() limit {limit}"
        result = client.execute(query, {"limit": limit})
        return [result[0] for result in result]

    def get_valid_combo_ids(self, limit: int = 20) -> List[int]:
        client = self._get_client()
        query = f"select multi_bundle_id from panacea.nu_multi_bundle order by rand() limit {limit}"
        result = client.execute(query, {"limit": limit})
        return [result[0] for result in result]
    
    def get_messages_from_db(self, limit: int = 20) -> List[str]:
        client = self._get_client()
        query = f"""
                    SELECT DISTINCT message
                    FROM nu_logs_local
                    WHERE length(message) < 100
                    LIMIT {limit};
                """
        result = client.execute(query, {"limit": limit})
        return [result[0] for result in result]


