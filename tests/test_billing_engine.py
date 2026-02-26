import unittest
from src.billing_engine import calculate_bill

class TestBillingEngine(unittest.TestCase):

    def test_bill_without_overage(self):
        bill, overage = calculate_bill(100, 50, 100, "ACTIVE")
        self.assertEqual(bill, 100)
        self.assertEqual(overage, 0)

    def test_bill_with_overage(self):
        bill, overage = calculate_bill(100, 150, 100, "ACTIVE")
        self.assertEqual(overage, 50)
        self.assertEqual(bill, 100 + 50 * 10)

    def test_suspended_subscription_billing(self):
        bill, overage = calculate_bill(100, 200, 100, "SUSPENDED")
        self.assertEqual(bill, 100)
        self.assertEqual(overage, 0)

    def test_cancelled_subscription_billing(self):
        bill, overage = calculate_bill(100, 200, 100, "CANCELLED")
        self.assertEqual(bill, 0)
        self.assertEqual(overage, 0)