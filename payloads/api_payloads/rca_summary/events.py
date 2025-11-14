import random

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class EventsAPI(BaseAPI):
    class PayloadTypes:
        """Payload type constants for EventsAPI"""
        DEFAULT = "default"
        COMBO_ID_ONLY = "combo_id_only"
        COMBO_ID_WITH_CURATED = "combo_id_with_curated"
        BUNDLE_ID_WITH_CURATED = "bundle_id_with_curated"

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/events"
        self.bundle_id = random.choice(json_payload.get_valid_bundle_ids())
        self.combo_id = random.choice(json_payload.get_valid_combo_ids())

    def get_api_method(self):
        return "GET"

    def generate_payload(self, payload_type: str = None):
        if payload_type is None:
            # Randomly select a payload type
            payload_types = [
                EventsAPI.PayloadTypes.DEFAULT,
                EventsAPI.PayloadTypes.COMBO_ID_ONLY,
                EventsAPI.PayloadTypes.COMBO_ID_WITH_CURATED,
                EventsAPI.PayloadTypes.BUNDLE_ID_WITH_CURATED,
            ]
            payload_type = random.choice(payload_types)
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case EventsAPI.PayloadTypes.DEFAULT:
                return {
                    "curated_event": None,
                    "bundle_id": self.bundle_id
                }
            case EventsAPI.PayloadTypes.COMBO_ID_ONLY:
                return {
                    "combo_id": self.combo_id,
                    "curated_event": None
                }
            case EventsAPI.PayloadTypes.COMBO_ID_WITH_CURATED:

                return {
                    "combo_id": self.combo_id,
                    "curated_event": True
                }
            case EventsAPI.PayloadTypes.BUNDLE_ID_WITH_CURATED:
                return {
                    "bundle_id": self.bundle_id,
                    "curated_event": True
                }

