## Stats collector

Notification event collector

### Usage
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

    capture_event(data=data)
```

### License
MIT (See LICENSE.txt file)