import unittest
import pandas as pd
from src.usage_aggregator import aggregate_usage

class TestUsageAggregator(unittest.TestCase):

    def test_multiple_usage_records(self):
        df = pd.DataFrame({
            "subscription_id": [1, 1],
            "usage_date": ["2024-03-01", "2024-03-02"],
            "data_used_gb": [10, 20]
        })
        result = aggregate_usage(df)
        self.assertEqual(result[1], 30)

    def test_no_usage_records(self):
        df = pd.DataFrame(columns=["subscription_id", "usage_date", "data_used_gb"])
        result = aggregate_usage(df)
        self.assertEqual(result, {})

    def test_invalid_usage_dates(self):
        df = pd.DataFrame({
            "subscription_id": [1],
            "usage_date": ["invalid"],
            "data_used_gb": [10]
        })
        result = aggregate_usage(df)
        self.assertEqual(result, {})