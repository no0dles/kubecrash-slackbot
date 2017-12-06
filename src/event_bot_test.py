import unittest
from unittest.mock import MagicMock, Mock
from src.event_bot import EventBot
import src.settings


class TestEventBot(unittest.TestCase):
    def test_do_not_notify_info(self):
        store = MagicMock()
        store.store = MagicMock()

        notifier = MagicMock()
        notifier.send_message = MagicMock()

        v1 = MagicMock()
        list_result = Mock()
        list_result.items = []

        item = Mock()
        item.type = 'Normal'
        list_result.items.append(item)

        v1.list_event_for_all_namespaces = MagicMock(return_value=list_result)

        src.settings.NOTIFY_INFO = False

        bot = EventBot(store, notifier, v1)
        bot.run()

        v1.list_event_for_all_namespaces.assert_called()
        notifier.send_message.assert_not_called()
        store.store.assert_not_called()
