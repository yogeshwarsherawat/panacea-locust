import json

from config import payload_config


class JsonPayload:
    def __init__(self, session_id: str):
        self.payload_data = json.load(open(payload_config.PAYLOAD_JSON_FILE_PATH))

    def get_valid_bundle_ids(self):
        return self.payload_data["bundle_ids"]

    def get_valid_combo_ids(self):
        return self.payload_data["combo_ids"]

    def get_valid_components(self):
        return self.payload_data["components"]

    def get_valid_log_level_types(self):
        return self.payload_data["log_level_types"]

    def get_valid_session_ids(self):
        return self.payload_data["session_ids"]

    def get_case_owner_emails(self):
        return self.payload_data["case_owner_emails"]

    def get_sfdc_case_numbers(self):
        return self.payload_data["sfdc_case_numbers"]

    def get_session_ids(self):
        return self.payload_data["session_ids"]

    def get_messages(self):
        return self.payload_data["messages"]

    def get_bundle_ids_for_log_viewer_apis(self):
        return list(self.payload_data["bundle_data"].keys())

    def get_bundle_data(self, bundle_id: int):
        return self.payload_data["bundle_data"][bundle_id]


json_payload = JsonPayload(session_id="")
