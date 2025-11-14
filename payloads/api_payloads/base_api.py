import json
from abc import ABC, abstractmethod

from config import config


class BaseAPI(ABC):
    def __init__(self):
        self.endpoint = ""

    def get_api_endpoint(self):
        return f"{config.DEFAULT_HOST}/{self.endpoint}"

    @abstractmethod
    def get_api_method(self):
        pass

    @abstractmethod
    def generate_payload(self):
        pass
