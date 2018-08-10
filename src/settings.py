import os


def default(name: str, val):
    return os.environ[name] if name in os.environ else val

USE_KUBECONF = default('USE_KUBECONF', False)
CACHE_TTL = default('CACHE_TTL', 10)
CHECK_INTERVAL = default('CHECK_INTERVAL', 10)
HTTP_PROXY = default('HTTP_PROXY', None)
HTTPS_PROXY = default('HTTPS_PROXY', None)
SLACK_ACCESS_TOKEN = default('SLACK_ACCESS_TOKEN', None)
SLACK_CHANNEL = default('SLACK_CHANNEL', None)
STORE_FILE = default('STORE_FILE', 'store.pkl')
STORE_LIMIT = default('STORE_LIMIT', 100)
NOTIFY_ERROR = default('NOTIFY_ERROR', True)
NOTIFY_WARNING = default('NOTIFY_WARNING', True)
NOTIFY_INFO = default('NOTIFY_INFO', False)
NOTIFY_UNHEALTHY = default('NOTIFY_UNHEALTHY', False)
NOTIFY_FAILEDSYNC = default('NOTIFY_FAILEDSYNC', False)
MUTED = False
