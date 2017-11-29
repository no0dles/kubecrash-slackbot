import os

CACHE_TTL = os.environ['CACHE_TTL'] if 'CACHE_TTL' in os.environ else 10
CHECK_INTERVAL = os.environ['CHECK_INTERVAL'] if 'CHECK_INTERVAL' in os.environ else 10
SLACK_ACCESS_TOKEN = os.environ['SLACK_ACCESS_TOKEN'] if 'SLACK_ACCESS_TOKEN' in os.environ else None
SLACK_CHANNEL = os.environ['SLACK_CHANNEL'] if 'SLACK_CHANNEL' in os.environ else None
