import random

from payloads.api_payloads.log_viewer.log_viewer import LogViewerAPI


class LogsHeatmapAPI(LogViewerAPI):
    class PayloadTypes:
        """Payload type constants for LogsHeatmapAPI"""
        DEFAULT = "default"

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/logs/heatmap/"

    def get_api_method(self):
        return "POST"

    def generate_payload(self, payload_type: str = None):
        if payload_type is None:
            payload_type = LogsHeatmapAPI.PayloadTypes.DEFAULT
        return self.get_payload(payload_type)

    def get_payload(self, payload_type: str):
        match payload_type:
            case LogsHeatmapAPI.PayloadTypes.DEFAULT:
                start_time, end_time = self.get_start_and_end_time_for_payload()
                return {
                    "bundle_ids": [self.bundle_id],
                    "filters": {
                        "components": self.get_components_for_payload(),
                        "log_levels": self.get_log_levels_for_payload(),
                        "cvm_ips": self.get_cvm_ips_for_payload(),
                        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    }
                }

