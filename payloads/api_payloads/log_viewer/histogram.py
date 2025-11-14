import random

from payloads.api_payloads.log_viewer.log_viewer import LogViewerAPI


class LogsHistogramAPI(LogViewerAPI):
    class PayloadTypes:
        """Payload type constants for LogsHistogramAPI"""
        DEFAULT = "default"

    DEFAULT_PAGE_SIZE = 100

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/logs/histogram/"

    def get_api_method(self):
        return "POST"

    def generate_payload(self, payload_type: str = None):
        if payload_type is None:
            payload_type = LogsHistogramAPI.PayloadTypes.DEFAULT
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case LogsHistogramAPI.PayloadTypes.DEFAULT:
                start_time, end_time = self.get_start_and_end_time_for_payload()
                return {
                    "bundle_ids": [self.bundle_id],
                    "page_no": 1,
                    "page_size": LogsHistogramAPI.DEFAULT_PAGE_SIZE,
                    "filters": {
                        "source_log_filenames": self.get_source_log_filenames_for_payload(),
                        "components": self.get_components_for_payload(),
                        # disabling log levels for histogram, as UI only calls it one time and then does the filtering in memory
                        # "log_levels": self.get_log_levels_for_payload(),
                        "cvm_ips": self.get_cvm_ips_for_payload(),
                        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "search_log_string": self.get_search_log_string_for_payload(),
                        "is_curated": self.get_is_curated_for_payload()
                    }
                }

