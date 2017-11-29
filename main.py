import time

from kubernetes import config, client
from src.settings import SLACK_ACCESS_TOKEN, SLACK_CHANNEL, CHECK_INTERVAL
from src.pod_bot import PodBot
from src.notifier import Notifier


def main():
    if not SLACK_ACCESS_TOKEN:
        print('missing SLACK_ACCESS_TOKEN environment variable')
        return exit(1)

    if not SLACK_CHANNEL:
        print('missing SLACK_CHANNEL environment variable')
        return exit(1)

    config.load_incluster_config()

    notifier = Notifier(SLACK_ACCESS_TOKEN, SLACK_CHANNEL)
    pod_bot = PodBot(notifier, client)

    while True:
        pod_bot.run()
        notifier.cleanup_cache()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
