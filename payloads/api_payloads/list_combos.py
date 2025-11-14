import random

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class ListCombosAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/list-combos"

    def generate_payload(self, payload_type: str):
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case "default":
                return {
                    "page_size": 20,
                    "page_no": 1
                }
            case "page_2":
                return {
                    "page_size": 20,
                    "page_no": 2
                }
            case "case_owner_email":
                case_owner_email = random.choice(json_payload.get_case_owner_emails())
                return {
                    "page_size": 20,
                    "page_no": 1,
                    "case_owner_email": case_owner_email
                }
            case "sfdc_case_number":
                sfdc_case_number = random.choice(json_payload.get_sfdc_case_numbers())
                return {
                    "page_size": 20,
                    "page_no": 1,
                    "sfdc_case_number": sfdc_case_number
                }
            case "case_owner_email_and_sfdc_case_number":
                case_owner_email = random.choice(json_payload.get_case_owner_emails())
                sfdc_case_number = random.choice(json_payload.get_sfdc_case_numbers())
                return {
                    "page_size": 20,
                    "page_no": 1,
                    "case_owner_email": case_owner_email,
                    "sfdc_case_number": sfdc_case_number
                }
