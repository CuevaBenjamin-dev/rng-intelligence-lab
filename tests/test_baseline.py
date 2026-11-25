import unittest
from src.baseline import accuracy, evaluate, generate_uniform


class BaselineTests(unittest.TestCase):
    def test_range_and_reproducibility(self):
        values = generate_uniform(1000)
        self.assertEqual(len(values), 1000)
        self.assertTrue(all(1 <= value <= 36 for value in values))
        self.assertEqual(values, generate_uniform(1000))

    def test_accuracy(self):
        self.assertAlmostEqual(accuracy([1, 2, 3], [1, 9, 3]), 2 / 3)
        with self.assertRaises(ValueError):
            accuracy([], [])
        with self.assertRaises(ValueError):
            accuracy([1, 2], [1])

    def test_evaluation(self):
        result = evaluate()
        self.assertEqual(result['train_count'], 8000)
        self.assertEqual(result['test_count'], 2000)
        self.assertAlmostEqual(result['theoretical_uniform'], 1 / 36)
        self.assertEqual(result, evaluate())
        self.assertTrue(0 <= result['uniform_accuracy'] <= 1)
        self.assertTrue(0 <= result['frequency_accuracy'] <= 1)

    def test_invalid_count(self):
        with self.assertRaises(ValueError):
            generate_uniform(0)
        with self.assertRaises(ValueError):
            evaluate(4)


if __name__ == '__main__':
    unittest.main()
