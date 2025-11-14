import random

from payloads.api_payloads.base_api import BaseAPI


class AskAIAPI(BaseAPI):
    def __init__(self, session_id: str = None):
        super().__init__(session_id=session_id)
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/ai/ask-ai/"
        # Sample messages for AI queries
        self.sample_messages = [
            "acropolis crashing in loop",
            "cassandra connection timeout",
            "zookeeper leader election failure",
            "stargate authentication error",
            "prism service unavailable",
            "genesis initialization failed",
            "cerebro memory leak detected",
            "curator backup failure",
            "chronos scheduling issue",
            "uhura communication error",
            "lazan data corruption",
            "minerva query timeout",
        ]

    def get_api_method(self):
        return "POST"

    def generate_payload(self, payload_type: str):
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case "default":
                # Use a random message from the sample list
                message = random.choice(self.sample_messages)
                return {
                    "messages": [message]
                }
            case "acropolis_crash":
                return {
                    "messages": ["acropolis crashing in loop"]
                }
            case "custom":
                # For custom messages, you can pass a message parameter
                # This is a placeholder - actual implementation would need message parameter
                return {
                    "messages": [random.choice(self.sample_messages)]
                }
            case _:
                # Default fallback
                return {
                    "messages": [random.choice(self.sample_messages)]
                }

