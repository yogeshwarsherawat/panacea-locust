"""
Panacea API Locust Load Testing Framework

python : /Users/yogeshwar.sherawat/nutanix/panacea/panacea-api/venv/bin/python
which python : python 3.11
"""

import logging
import os

# Import configuration
from config import config

# Import event handlers and set them up
from event_handlers import setup_event_handlers
from panacea_user import PanaceaAPIUser



# Configure logging
log_level = os.getenv("LOCUST_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Setup event handlers for monitoring and metrics
setup_event_handlers()

# Log framework initialization
logger.info("🚀 Panacea Locust Framework Initialized")

# Export user classes for Locust to discover
# Locust will automatically find these classes and use their weights
__all__ = [
    "PanaceaAPIUser",
]
