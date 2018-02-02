from src.settings import HTTP_PROXY, HTTPS_PROXY, MUTED
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
        self.proxies = None
        
        if HTTP_PROXY or HTTPS_PROXY:
            self.proxies = {}
        if HTTP_PROXY:
            self.proxies['http'] = HTTP_PROXY
        if HTTPS_PROXY:
            self.proxies['https'] = HTTPS_PROXY

    def send_message(self, fields=None, color=None):
        if MUTED:
            return

        sc = SlackClient(self.access_token, self.proxies)
        res = sc.api_call('chat.postMessage',
                          channel=self.channel,
                          icon_url='',
                          attachments=[{
                              "fields": fields,
                              "color": color,
                          }])

        if not res['ok']:
            print(res['error'])

    def send_pod_info(self, pod: Pod):
        if not self.has_changed(pod):
            return

        if not pod.is_error():
            return

        self.send_message(pod.message_title(), pod.message_content())

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
