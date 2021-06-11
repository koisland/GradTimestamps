import unittest
from main import time_to


class TestMain(unittest.TestCase):

    def test_frames_to_time(self):
        case_1 = 694494
        case_1_fps = 30

        self.assertEqual(time_to(case_1, case_1_fps), (6, 25, 49))
