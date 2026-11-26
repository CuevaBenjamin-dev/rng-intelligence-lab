import math
import unittest

from src.experiment_e01 import run_scenario
from src.statistical_audit import (
    BIASED_PROBABILITY,
    CHI_SQUARE_CRITICAL_VALUE,
    OTHER_PROBABILITY,
    biased_probabilities,
    frequencies,
    generate_biased,
    generate_uniform,
    pearson_chi_square_uniform,
    reject_uniformity,
)


class StatisticalAuditTests(unittest.TestCase):
    def test_uniform_generator_range_and_reproducibility(self):
        values = generate_uniform(1_000, 12)
        self.assertEqual(values, generate_uniform(1_000, 12))
        self.assertEqual(len(values), 1_000)
        self.assertTrue(all(1 <= value <= 36 for value in values))
        self.assertNotEqual(values, generate_uniform(1_000, 13))

    def test_biased_generator_distribution_and_reproducibility(self):
        probabilities = biased_probabilities()
        self.assertEqual(len(probabilities), 36)
        self.assertEqual(probabilities[0], BIASED_PROBABILITY)
        self.assertTrue(all(p == OTHER_PROBABILITY for p in probabilities[1:]))
        self.assertAlmostEqual(sum(probabilities), 1.0)
        values = generate_biased(36_000, 12)
        self.assertEqual(values, generate_biased(36_000, 12))
        self.assertTrue(all(1 <= value <= 36 for value in values))
        self.assertAlmostEqual(values.count(1) / len(values), 0.08, delta=0.01)

    def test_generator_invalid_inputs(self):
        for generator in (generate_uniform, generate_biased):
            for count, seed in ((0, 1), (-1, 1), (1.5, 1), (True, 1),
                                (1, 1.5), (1, True)):
                with self.subTest(generator=generator.__name__, count=count, seed=seed):
                    with self.assertRaises(ValueError):
                        generator(count, seed)

    def test_frequencies_include_zero_categories(self):
        absolute, relative = frequencies([1, 1, 36])
        self.assertEqual(len(absolute), 36)
        self.assertEqual(absolute[1], 2)
        self.assertEqual(absolute[2], 0)
        self.assertEqual(absolute[36], 1)
        self.assertAlmostEqual(relative[1], 2 / 3)
        self.assertAlmostEqual(sum(relative.values()), 1.0)

    def test_frequencies_invalid_values(self):
        for values in ([], [0], [37], [True], [1.0], [1, -1]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                frequencies(values)

    def test_pearson_statistic_and_rejection(self):
        equal = {number: 100 for number in range(1, 37)}
        self.assertEqual(pearson_chi_square_uniform(equal), 0)
        equal[1] = 180
        equal[2] = 20
        self.assertAlmostEqual(pearson_chi_square_uniform(equal), 128)
        self.assertFalse(reject_uniformity(0))
        self.assertTrue(reject_uniformity(128))
        self.assertTrue(reject_uniformity(CHI_SQUARE_CRITICAL_VALUE))

    def test_pearson_invalid_inputs(self):
        valid = {number: 100 for number in range(1, 37)}
        for counts in ({1: 100}, {**valid, 37: 0},
                       {**valid, 1: -1}, {**valid, 1: 1.5},
                       {number: 4 for number in range(1, 37)}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                pearson_chi_square_uniform(counts)
        for statistic in (-1, math.nan, math.inf, True, "1"):
            with self.subTest(statistic=statistic), self.assertRaises(ValueError):
                reject_uniformity(statistic)

    def test_scenario_reproducibility_and_aggregation(self):
        result = run_scenario("control", generate_uniform, runs=2,
                              observations_per_run=180, seed=77)
        self.assertEqual(result, run_scenario("control", generate_uniform,
                                              runs=2, observations_per_run=180,
                                              seed=77))
        self.assertEqual(sum(result.absolute_frequencies.values()), 360)
        self.assertAlmostEqual(sum(result.relative_frequencies.values()), 1.0)
        self.assertTrue(0 <= result.rejections <= 2)
        with self.assertRaises(ValueError):
            run_scenario("control", generate_uniform, observations_per_run=179)

    def test_scenario_uses_distinct_seeds_and_validates_length(self):
        seen_seeds = []

        def recording_generator(count, seed):
            seen_seeds.append(seed)
            return generate_uniform(count, seed)

        run_scenario("control", recording_generator, runs=3,
                     observations_per_run=180, seed=77)
        self.assertEqual(len(seen_seeds), len(set(seen_seeds)))
        with self.assertRaises(ValueError):
            run_scenario("control", lambda count, seed: [1], runs=1,
                         observations_per_run=180)
        for runs, sample_size, seed in ((0, 180, 1), (1, 180, True),
                                        (1, 179, 1)):
            with self.subTest(runs=runs, sample_size=sample_size, seed=seed):
                with self.assertRaises(ValueError):
                    run_scenario("control", generate_uniform, runs=runs,
                                 observations_per_run=sample_size, seed=seed)


if __name__ == "__main__":
    unittest.main()
