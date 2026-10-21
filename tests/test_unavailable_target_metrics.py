import unittest
from failure_analysis.validation_metrics import evaluate_target_metrics


class UnavailableTargetTests(unittest.TestCase):
    def test_missing_observation_cannot_look_like_improvement(self):
        plan = {'fixes': [{'target_metrics': ['error_rate']}]}
        for before, after in [({'error_rate': .5}, {}), ({}, {'error_rate': .5}), ({}, {})]:
            with self.subTest(before=before, after=after):
                with self.assertRaisesRegex(ValueError, 'error_rate'):
                    evaluate_target_metrics(plan, {'metrics': before}, {'metrics': after})

    def test_invalid_observations_are_rejected(self):
        for value in [None, '0', float('nan'), float('inf'), float('-inf')]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, 'error_rate'):
                    evaluate_target_metrics({'fixes': [{'target_metrics': ['error_rate']}]},
                        {'metrics': {'error_rate': .5}}, {'metrics': {'error_rate': value}})

    def test_actual_zero_is_valid(self):
        result = evaluate_target_metrics({'fixes': [{'target_metrics': ['error_rate']}]},
            {'metrics': {'error_rate': .5}}, {'metrics': {'error_rate': 0}})
        self.assertEqual(result['improved_metric_count'], 1)
        self.assertEqual(result['aggregate_delta'], .5)

    def test_default_metric_still_works(self):
        result = evaluate_target_metrics({}, {'mode': 'gaia', 'metrics': {'accuracy': .2}},
            {'metrics': {'accuracy': .3}})
        self.assertEqual(result['improved_metric_count'], 1)
