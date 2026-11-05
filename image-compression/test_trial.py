import unittest
from trial import evaluate, objective


class TrialTests(unittest.TestCase):
    def test_quality_boundary(self):
        self.assertLess(objective(100000, 1, .95), 1)
        self.assertGreater(objective(1, 100000, .949999), 1)

    def test_parameters_affect_real_encoding(self):
        low = evaluate(50, 0)
        high = evaluate(100, 6)
        self.assertNotEqual(low["total_bytes"], high["total_bytes"])
        self.assertGreater(high["minimum_ssim"], low["minimum_ssim"])

    def test_bad_inputs(self):
        for quality, method in [(49, 4), (101, 4), (80, -1), (80, 7)]:
            with self.assertRaises(ValueError):
                evaluate(quality, method)
        with self.assertRaises(ValueError):
            evaluate(80, 4, "missing")


if __name__ == "__main__":
    unittest.main()
