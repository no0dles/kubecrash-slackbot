import time
import os

from kubernetes import config, client
from src.settings import SLACK_ACCESS_TOKEN, SLACK_CHANNEL, CHECK_INTERVAL, USE_KUBECONF
from src.event_bot import EventBot
from src.event_store import EventStore
from src.notifier import Notifier


def main():
    if not SLACK_ACCESS_TOKEN:
        print('missing SLACK_ACCESS_TOKEN environment variable')
        return exit(1)

    if not SLACK_CHANNEL:
        print('missing SLACK_CHANNEL environment variable')
        return exit(1)

    if USE_KUBECONF:
        config.load_kube_config()
    else:
        config.load_incluster_config()

    notifier = Notifier(SLACK_ACCESS_TOKEN, SLACK_CHANNEL)
    event_store = EventStore()
    event_bot = EventBot(event_store, notifier, client.CoreV1Api())

    while True:
        event_bot.run()
        notifier.cleanup_cache()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
