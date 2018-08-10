from kubernetes.client import CoreV1Api, V1Event
from src.settings import NOTIFY_ERROR, NOTIFY_WARNING, NOTIFY_INFO, NOTIFY_UNHEALTHY, NOTIFY_FAILEDSYNC
from src.notifier import Notifier
from src.event_store import EventStore


class EventBot(object):
    def __init__(self, store: EventStore, notifier: Notifier, v1: CoreV1Api):
        self.notifier = notifier
        self.v1 = v1
        self.store = store

    def check(self, event: V1Event):

        if not NOTIFY_ERROR and event.type == 'Failed':
            return

        if not NOTIFY_WARNING and event.type == 'Warning':
            return

        if not NOTIFY_INFO and event.type == 'Normal':
            return
        
        if not NOTIFY_UNHEALTHY and event.reason == 'Unhealthy':
            return
        
        if not NOTIFY_FAILEDSYNC and event.reason == 'FailedSync':
            return
        
        if self.store.contains(event.metadata.uid):
            return

        if event.type == 'Failed':
            color = "#e74c3c"
        if event.type == "Warning":
            color = "#f39c12"
        if event.type == 'Normal':
            color = "#3498db"

        fields = [
            {
                "title": "Reason",
                "value": event.reason,
                "short": True
            },
            {
                "title": "Kind",
                "value": event.involved_object.kind,
                "short": True
            },
            {
                "title": "Namespace",
                "value": event.involved_object.namespace,
                "short": True
            },
            {
                "title": "Name",
                "value": event.involved_object.name,
                "short": True
            },
            {
                "title": "Message",
                "value": event.message,
                "short": False
            }
        ]

        if event.source.host:
            fields.append({
                "title": "Host",
                "value": event.source.host,
                "short": True
            })
            
        fields.append({
            "title": "Time",
            "value": event.last_timestamp,
            "short": True
        })

        self.notifier.send_message(fields=fields, color=color)
        self.store.store(event.metadata.uid)

    def run(self):
        event_list = self.v1.list_event_for_all_namespaces(limit=100)
        """:type : V1EventList"""

        for item in event_list.items:
            self.check(item)
