import random

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class EventsAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/events"
        self.bundle_id = random.choice(json_payload.get_valid_bundle_ids())
        self.combo_id = random.choice(json_payload.get_valid_combo_ids())

    def get_api_method(self):
        return "GET"

    def generate_payload(self, payload_type: str):
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case "default":
                return {
                    "curated_event": None,
                    "bundle_id": self.bundle_id
                }
            case "combo_id_only":
                return {
                    "combo_id": self.combo_id,
                    "curated_event": None
                }
            case "combo_id_with_curated":

                return {
                    "combo_id": self.combo_id,
                    "curated_event": True
                }
            case "bundle_id_with_curated":
                return {
                    "bundle_id": self.bundle_id,
                    "curated_event": True
                }

