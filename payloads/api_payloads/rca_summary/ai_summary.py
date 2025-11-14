import random

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class AISummaryAPI(BaseAPI):
    class PayloadTypes:
        """Payload type constants for AISummaryAPI"""
        COMBO_ID_ONLY = "combo_id_only"
        BUNDLE_ID_ONLY = "bundle_id_only"

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/ai/report_summary"
        self.bundle_id = random.choice(json_payload.get_valid_bundle_ids())
        self.combo_id = random.choice(json_payload.get_valid_combo_ids())

    def get_api_method(self):
        return "GET"

    def generate_payload(self, payload_type: str = None):
        if payload_type is None:
            # Randomly select a payload type
            payload_types = [
                AISummaryAPI.PayloadTypes.COMBO_ID_ONLY,
                AISummaryAPI.PayloadTypes.BUNDLE_ID_ONLY,
            ]
            payload_type = random.choice(payload_types)
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case AISummaryAPI.PayloadTypes.COMBO_ID_ONLY:
                return {
                    "combo_id": self.combo_id
                }
            case AISummaryAPI.PayloadTypes.BUNDLE_ID_ONLY:
                return {
                    "bundle_id": self.bundle_id
                }

