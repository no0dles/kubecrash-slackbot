import unittest
from src.event_bot_test import TestEventBot

if __name__ == '__main__':
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    suite = loader.loadTestsFromTestCase(TestEventBot)
    runner.run(suite)
