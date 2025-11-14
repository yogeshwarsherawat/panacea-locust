import random

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class LogsFilterOptionsAPI(BaseAPI):
    class PayloadTypes:
        """Payload type constants for LogsFilterOptionsAPI"""
        BUNDLE_IDS_ONLY = "bundle_ids_only"
    
    MAX_BUNDLE_IDS_PER_REQUEST = 3

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/logs/filter-options"
        n_bundle_ids = random.randint(1, LogsFilterOptionsAPI.MAX_BUNDLE_IDS_PER_REQUEST)
        self.bundle_ids = random.sample(json_payload.get_valid_bundle_ids(), n_bundle_ids)

    def get_api_method(self):
        return "GET"

    def generate_payload(self, payload_type: str = None):
        if payload_type is None:
            payload_type = LogsFilterOptionsAPI.PayloadTypes.BUNDLE_IDS_ONLY
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case LogsFilterOptionsAPI.PayloadTypes.BUNDLE_IDS_ONLY:
                return {
                    "bundle_ids": ",".join(map(str, self.bundle_ids))
                }

