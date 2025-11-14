import random

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class AskAIAPI(BaseAPI):
    class PayloadTypes:
        """Payload type constants for AskAIAPI"""
        DEFAULT = "default"

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/ai/ask-ai/"
        # Sample messages for AI queries
        self.messages = json_payload.get_messages()

    def get_api_method(self):
        return "POST"

    def generate_payload(self, payload_type: str = None):
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        if payload_type is None:
            payload_type = AskAIAPI.PayloadTypes.DEFAULT
        message = random.choice(self.messages)
        return {"messages": [message] }

