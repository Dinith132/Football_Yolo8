import unittest
from trackers.trackers import Tracker

class TestTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = Tracker("dummy_model_path")

if __name__ == '__main__':
    unittest.main()
