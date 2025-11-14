import random

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class ReportsAPI(BaseAPI):
    class PayloadTypes:
        """Payload type constants for ReportsAPI"""
        DEFAULT = "default"
        PAGE_2 = "page_2"
        CASE_OWNER_EMAIL = "case_owner_email"
        SFDC_CASE_NUMBER = "sfdc_case_number"
        CASE_OWNER_EMAIL_AND_SFDC_CASE_NUMBER = "case_owner_email_and_sfdc_case_number"

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/reports"

    def generate_payload(self, payload_type: str = None):
        if payload_type is None:
            # Randomly select a payload type
            payload_types = [
                ReportsAPI.PayloadTypes.DEFAULT,
                ReportsAPI.PayloadTypes.PAGE_2,
                ReportsAPI.PayloadTypes.CASE_OWNER_EMAIL,
                ReportsAPI.PayloadTypes.SFDC_CASE_NUMBER,
                ReportsAPI.PayloadTypes.CASE_OWNER_EMAIL_AND_SFDC_CASE_NUMBER,
            ]
            payload_type = random.choice(payload_types)
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case ReportsAPI.PayloadTypes.DEFAULT:
                return {
                    "page_size": 20,
                    "page_no": 1
                }
            case ReportsAPI.PayloadTypes.PAGE_2:
                return {
                    "page_size": 20,
                    "page_no": 2
                }
            case ReportsAPI.PayloadTypes.CASE_OWNER_EMAIL:
                case_owner_email = random.choice(json_payload.get_case_owner_emails())
                return {
                    "page_size": 20,
                    "page_no": 1,
                    "case_owner_email": case_owner_email
                }
            case ReportsAPI.PayloadTypes.SFDC_CASE_NUMBER:
                sfdc_case_number = random.choice(json_payload.get_sfdc_case_numbers())
                return {
                    "page_size": 20,
                    "page_no": 1,
                    "sfdc_case_number": sfdc_case_number
                }
            case ReportsAPI.PayloadTypes.CASE_OWNER_EMAIL_AND_SFDC_CASE_NUMBER:
                case_owner_email = random.choice(json_payload.get_case_owner_emails())
                sfdc_case_number = random.choice(json_payload.get_sfdc_case_numbers())
                return {
                    "page_size": 20,
                    "page_no": 1,
                    "case_owner_email": case_owner_email,
                    "sfdc_case_number": sfdc_case_number
                }
