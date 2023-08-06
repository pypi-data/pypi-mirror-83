import unittest
import sys
import os
sys.path.append(os.path.join(os.path.abspath(__file__), ".."))
from time_boss import TimeBoss
import time

class TestTimeBoss(unittest.TestCase):

    def test_root_timers(self):
        TimeBoss.reset()
        with TimeBoss("root"):
            time.sleep(0.01)
        with TimeBoss("root"):
            time.sleep(0.01)
        with TimeBoss("root2"):
            time.sleep(0.01)
        self.assertEqual(len(TimeBoss.all_timers), 2)

    def test_nested_timers(self):
        TimeBoss.reset()
        with TimeBoss("root"):
            with TimeBoss("sub"):
                time.sleep(0.01)
                self.assertEqual(len(TimeBoss.timer_stack), 2)
            cur_stack = TimeBoss.timer_stack[-1]
            self.assertEqual(len(cur_stack.sub_timers), 1)
            self.assertEqual(cur_stack.sub_timers[-1].name , "sub")
        self.assertEqual(len(TimeBoss.all_timers), 2)

    def test_timing(self):
        TimeBoss.reset()
        with TimeBoss("root"):
            time.sleep(0.1)
        with TimeBoss("root"):
            time.sleep(0.2)
        self.assertEqual(len(TimeBoss.root_timers[0].timings), 2)
        self.assertAlmostEqual(TimeBoss.root_timers[0].timings[0], 0.1, 3)
        self.assertAlmostEqual(TimeBoss.root_timers[0].timings[1], 0.2, 3)



if __name__ == '__main__':
    unittest.main()
