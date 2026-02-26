import unittest
from src.status_engine import evaluate_status

class TestStatusEngine(unittest.TestCase):

    def test_active_to_suspended_transition(self):
        status = evaluate_status("ACTIVE", 200, 100)
        self.assertEqual(status, "SUSPENDED")

    def test_suspended_to_active_transition(self):
        status = evaluate_status("SUSPENDED", 50, 100)
        self.assertEqual(status, "ACTIVE")

    def test_cancelled_status_unchanged(self):
        status = evaluate_status("CANCELLED", 500, 100)
        self.assertEqual(status, "CANCELLED")