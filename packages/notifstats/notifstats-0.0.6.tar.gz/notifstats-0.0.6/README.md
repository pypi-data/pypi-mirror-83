## Stats collector

Notification event collector 

### Instalation
Install with pip: 

```
$ pip install notifstats
```

### API
`capture_event` receives two arguments:  

`data` : Analytic data to be captured. See Usage section.  
`is_production`: Default to True. If False, the data will be sent to staging BigQuery.  

### Usage
Requires `google-cloud-bigquery>=1.20.0`

```
from datetime import datetime
from notifstats import capture_event


if __name__ == "__main__":
    data = {
        "notification_id": "test-12345",
        "event_type": "sent_to_slackbot",
        "object_id": "test-67890",
        "taxonomy_id": "test-2345",
        "created_at": datetime.now().isoformat(),
        "notification_type": "segmented",
    }

    capture_event(data=data, is_production=False)
```


Available events_type:  
```
available_events = [
    "notification_requested",
    "notification_sent_to_onesignal",
    "notification_statistic_stored",
    "notification_history_written",
    "sent_to_slackbot",
]
```


### License
MIT