from typing import Mapping
from src.pod import Pod
from slackclient import SlackClient

from src.cache import Cache


class Notifier(object):
    cache: Mapping[str, Cache]

    def __init__(self, access_token: str, channel: str):
        self.cache = {}
        self.access_token = access_token
        self.channel = channel

    def send_pod_info(self, pod: Pod):
        if not self.has_changed(pod):
            return

        if not pod.is_error():
            return

        sc = SlackClient(self.access_token)
        sc.api_call('chat.postMessage',
                    channel=self.channel,
                    icon_url='',
                    attachments=[{
                        "pretext": pod.message_title(),
                        "text": pod.message_content()
                    }])

    def has_changed(self, status: Pod):
        identifier = status.identifier()
        if identifier not in self.cache:
            self.cache[identifier] = Cache(status.status_value())
            return True

        cache = self.cache[identifier]

        if cache.value != status.status_value():
            self.cache[identifier] = Cache(status.status_value())
            return True
        else:
            cache.ttl = cache.ttl + 1

        return False

    def cleanup_cache(self):
        keys = list(self.cache.keys())
        for key in keys:
            cache = self.cache[key]
            cache.ttl = cache.ttl - 1
            if cache.ttl < 0:
                self.cache.pop(key, None)
