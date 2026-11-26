import math
import unittest

from src.experiment_e02 import run_scenario, wilson_interval
from src.statistical_audit import generate_uniform
from src.temporal_audit import (
    adjacent_repeat_count,
    generate_sticky_uniform,
    permutation_test,
)


class TemporalAuditTests(unittest.TestCase):
    def test_sticky_generator_range_and_reproducibility(self):
        values = generate_sticky_uniform(2_000, 17)
        self.assertEqual(values, generate_sticky_uniform(2_000, 17))
        self.assertEqual(len(values), 2_000)
        self.assertTrue(all(1 <= value <= 36 for value in values))
        self.assertNotEqual(values, generate_sticky_uniform(2_000, 18))
        self.assertEqual(len(set(generate_sticky_uniform(20, 17, 1))), 1)

    def test_sticky_control_keeps_marginal_and_adds_repeats(self):
        count = 36_000
        dependent = generate_sticky_uniform(count, 23)
        independent = generate_uniform(count, 23)
        self.assertAlmostEqual(dependent.count(1) / count, 1 / 36,
                               delta=0.005)
        self.assertGreater(adjacent_repeat_count(dependent),
                           adjacent_repeat_count(independent) + 300)

    def test_sticky_generator_invalid_inputs(self):
        for count, seed, probability in (
            (1, 1, 0.02), (True, 1, 0.02), (2, True, 0.02),
            (2, 1, -0.1), (2, 1, 1.1), (2, 1, math.nan),
            (2, 1, math.inf), (2, 1, True),
        ):
            with self.subTest(count=count, seed=seed, probability=probability):
                with self.assertRaises(ValueError):
                    generate_sticky_uniform(count, seed, probability)

    def test_adjacent_repeat_count(self):
        self.assertEqual(adjacent_repeat_count([1, 1, 2, 2, 2]), 3)
        self.assertEqual(adjacent_repeat_count([1, 2, 1, 2]), 0)
        for values in ([], [1], [1, 37], [True, 1]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                adjacent_repeat_count(values)

    def test_permutation_test_ties_and_reproducibility(self):
        identical = permutation_test([1] * 20, seed=11, permutations=19)
        self.assertEqual(identical.observed_repeats, 19)
        self.assertEqual(identical.extreme_permutations, 19)
        self.assertEqual(identical.p_value, 1)
        self.assertFalse(identical.rejects)
        values = [1] * 10 + [2] * 10
        first = permutation_test(values, seed=12, permutations=199)
        self.assertEqual(first, permutation_test(values, seed=12, permutations=199))
        self.assertEqual(first.p_value,
                         (first.extreme_permutations + 1) / 200)
        self.assertTrue(first.rejects)

    def test_permutation_invalid_inputs(self):
        for seed, permutations in ((True, 19), (1, 0), (1, 18),
                                   (1, 1.5), (1, True)):
            with self.subTest(seed=seed, permutations=permutations):
                with self.assertRaises(ValueError):
                    permutation_test([1, 2], seed, permutations)

    def test_wilson_interval(self):
        low, high = wilson_interval(50, 100)
        self.assertAlmostEqual(low, 0.4038, places=3)
        self.assertAlmostEqual(high, 0.5962, places=3)
        self.assertEqual(wilson_interval(0, 100)[0], 0)
        self.assertEqual(wilson_interval(100, 100)[1], 1)
        for successes, trials in ((-1, 100), (101, 100), (1, 0),
                                  (True, 100), (1, True)):
            with self.subTest(successes=successes, trials=trials):
                with self.assertRaises(ValueError):
                    wilson_interval(successes, trials)

    def test_scenario_reproducibility_and_validation(self):
        first = run_scenario("control", generate_uniform, runs=2,
                             observations_per_run=180, permutations=19, seed=7)
        self.assertEqual(first, run_scenario("control", generate_uniform,
                                             runs=2, observations_per_run=180,
                                             permutations=19, seed=7))
        self.assertEqual(sum(first.absolute_frequencies.values()), 360)
        self.assertTrue(0 <= first.rejections <= 2)
        seen_seeds = []

        def recording_generator(count, seed):
            seen_seeds.append(seed)
            return generate_uniform(count, seed)

        run_scenario("control", recording_generator, runs=3,
                     observations_per_run=180, permutations=19, seed=7)
        self.assertEqual(len(seen_seeds), len(set(seen_seeds)))
        with self.assertRaises(ValueError):
            run_scenario("control", lambda count, seed: [1], runs=1,
                         observations_per_run=180, permutations=19)
        for name, runs, count in (("", 1, 180), ("control", 0, 180),
                                  ("control", 1, 1)):
            with self.subTest(name=name, runs=runs, count=count):
                with self.assertRaises(ValueError):
                    run_scenario(name, generate_uniform, runs=runs,
                                 observations_per_run=count, permutations=19)


if __name__ == "__main__":
    unittest.main()
