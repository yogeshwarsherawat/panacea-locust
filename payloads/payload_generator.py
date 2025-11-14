import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import payload_config
from database.clickhouse_dao import ClickHouseDAO


class PayloadGenerator:
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = "cf811e567c5d42e9bd61a3562ecdd29f"
        self.clickhouse_dao = ClickHouseDAO()

    def get_headers(self):
        return {"Content-Type": "application/json", "X-Session-Id": self.session_id}

    def generate_payload(self):
        case_owner_emails, sfdc_case_numbers = (
            self.get_case_owner_emails_and_sfdc_case_numbers()
        )
        session_ids = list(self.clickhouse_dao.get_users_and_sessions().values())
        log_level_types = [
            "debug",
            "info",
            "warn",
            "error",
            "fatal",
            "critical",
            "trace",
            "unknown",
        ]
        bundle_ids = list(self.clickhouse_dao.get_valid_log_bundle_ids())
        combo_ids = list(self.clickhouse_dao.get_valid_combo_ids())

        data = {
            "case_owner_emails": case_owner_emails,
            "sfdc_case_numbers": sfdc_case_numbers,
            "session_ids": session_ids,
            "log_level_types": log_level_types,
            "bundle_ids": bundle_ids,
            "combo_ids": combo_ids,
            "messages": self.clickhouse_dao.get_messages_from_db(),
            "bundle_data": self.clickhouse_dao.get_bundle_data(bundle_ids)
        }

        with open(payload_config.PAYLOAD_JSON_FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)

    def get_case_owner_emails_and_sfdc_case_numbers(
        self,
    ) -> Tuple[List[str], List[str]]:

        url = "http://10.113.24.33:9898/api/v1/insights/reports"

        payload = json.dumps({"page_size": 20, "page_no": 1})
        headers = self.get_headers()
        response = requests.request("POST", url, headers=headers, data=payload)

        reponse = response.json()
        api_status = reponse["api_status"]
        report_details = reponse["report_details"]

        if not api_status == "success":
            raise Exception(
                f"error in get_case_owner_emails_and_sfdc_case_numbers : Failed to get case owner emails and sfdc case numbers"
            )

        case_owner_emails = []
        sfdc_case_numbers = []

        for report in report_details:
            if len(case_owner_emails) < payload_config.NO_OF_CASE_OWNER_EMAILS_REQUIRED:
                case_owner_emails.append(report["case_owner_email"])
            if len(sfdc_case_numbers) < payload_config.NO_OF_SFDC_CASE_NUMBERS_REQUIRED:
                sfdc_case_numbers.append(report["sfdc_case_no"])

        return case_owner_emails, sfdc_case_numbers


payload_generator = PayloadGenerator()
payload_generator.generate_payload()
