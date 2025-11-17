import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from payloads.api_payloads.base_api import BaseAPI
from payloads.json_payload import json_payload


class LogViewerAPI(BaseAPI):
    class PayloadTypes:
        """Payload type constants for LogsSearchAPI"""
        DEFAULT = "default"

    DEFAULT_PAGE_SIZE = 20

    def __init__(self):
        super().__init__()
        # do not use '/' at the beginning of the endpoint
        self.endpoint = "api/v1/insights/logs/viewer/"
        self.bundle_id = random.choice(json_payload.get_bundle_ids_for_log_viewer_apis())
        self.bundle_data = json_payload.get_bundle_data(self.bundle_id)
        self.components = self.bundle_data["components"]
        self.source_log_filenames = self.bundle_data["source_log_filenames"]
        self.log_levels = json_payload.get_valid_log_level_types()
        self.start_time = self.bundle_data["start_time"]
        self.end_time = self.bundle_data["end_time"]

    @abstractmethod
    def get_api_method(self):
        pass

    @abstractmethod
    def generate_payload(self, payload_type: str = None):
        pass
    
    def get_components_for_payload(self):
        components = []
        use_components = random.choice([True, False, False, False, False])
        if use_components:
            components_count_to_use = min(random.randint(1, 3), len(self.components))
            components_to_use = random.sample(self.components, components_count_to_use)
            components.extend(components_to_use)
        return components

    def get_source_log_filenames_for_payload(self):
        source_log_filenames = []
        use_source_log_filenames = random.choice([True, False, False, False, False])
        if use_source_log_filenames:
            source_log_filenames_count_to_use = min(random.randint(1, 3), len(self.source_log_filenames))
            source_log_filenames_to_use = random.sample(self.source_log_filenames, source_log_filenames_count_to_use)
            source_log_filenames.extend(source_log_filenames_to_use)
        return source_log_filenames
    
    def get_log_levels_for_payload(self):
        log_levels = []
        use_log_levels = random.choice([True, False, False, False, False])
        if use_log_levels:
            log_levels_count_to_use = min(random.randint(1, 3), len(self.log_levels))
            log_levels_to_use = random.sample(self.log_levels, log_levels_count_to_use)
            log_levels.extend(log_levels_to_use)
        return log_levels
    
    def get_start_and_end_time_for_payload(self):
        start_dt = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
        if start_dt >= end_dt:
            # fallback in case data is nonsense
            start_time = start_dt
            end_time = start_dt + timedelta(hours=random.randint(0, 240))
        else:
            total_seconds = int((end_dt - start_dt).total_seconds())
            rand_offset = random.randint(0, total_seconds)
            start_time = start_dt + timedelta(seconds=rand_offset)
            end_time = start_time + timedelta(hours=random.randint(0, 24))
        return start_time, end_time

    def get_is_curated_for_payload(self):
        return random.choice([True, None, None, None, None])

    def get_search_log_string_for_payload(self):
        search_log_string_sample = ["", "", "", "", "", "", random.choice(json_payload.get_messages())]
        return random.choice(search_log_string_sample)

    def get_cvm_ips_for_payload(self):
        cvm_ips = []
        return cvm_ips


