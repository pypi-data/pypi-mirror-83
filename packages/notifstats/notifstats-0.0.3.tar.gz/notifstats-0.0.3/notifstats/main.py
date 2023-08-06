from typing import Any, Dict
from datetime import datetime

from google.cloud import bigquery


class NotificationStatistic:
    def __init__(self, project_id: str, bq_client: Any) -> None:
        self.project_id = project_id
        self.bq_client = bq_client

    def capture(self, data: Dict[str, Any]):
        """Capture event

        Capture event and transport to BigQuery.

        Args:
            data: a dict consists of:
                    - notification_id
                    - event_type
                    - object_id
                    - taxonomy_id
                    - created_at
                    - notification_type

        Returns:
            BigQuery error message or None
        """

        available_events = [
            "sent_to_slackbot",
            "history_written",
            "notification_requested",
        ]

        if data["event_type"] not in available_events:
            raise ValueError("Event type is not supported")

        table_id = f"{self.project_id}.notification_platform.statistics"

        return self.bq_client.insert_rows_json(table_id, [data])


def capture_event(data: Dict[str, Any], is_production: bool = False):
    """Capture event

    Capture event and transport to BigQuery.

    Args:
        data: a dict consists of:
                - notification_id
                - event_type
                - object_id
                - taxonomy_id
                - created_at
                - notification_type
        is_production: A flag to select the bigquery dataset.

    Returns:
        BigQuery error message or None
    """

    project_id = "kumparan-data" if is_production else "kumparan-data-staging"

    ns = NotificationStatistic(project_id=project_id, bq_client=bigquery.Client())

    return ns.capture(data)