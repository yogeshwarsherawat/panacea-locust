import json
from abc import ABC, abstractmethod

from config import config


class BaseAPI(ABC):
    def __init__(self):
        self.endpoint = ""

    def get_api_endpoint(self):
        return f"{config.DEFAULT_HOST}/{self.endpoint}"

    def get_api_method(self):
        return "POST"

    def generate_headers(self):
        return {
            "X-Session-Id": self.session_id,
            "Content-Type": "application/json",
        }

    @abstractmethod
    def generate_payload(self):
        pass
