import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from x402.account import PrepaidUSDAccount


def test_deduct_success():
    """Start with balance 1.00, deduct 0.002, assert remaining balance is 0.998."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "account_balance.json")
        account = PrepaidUSDAccount(file_path=json_file)
        assert account.get_balance() == 1.00

        success = account.deduct(0.002)
        assert success is True
        assert round(account.get_balance(), 3) == 0.998


def test_deduct_insufficient():
    """Start with balance 0.001, attempt to deduct 0.002, assert returns False."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "account_balance.json")
        account = PrepaidUSDAccount(file_path=json_file)
        # Deduct 0.999 first to leave 0.001
        account.deduct(0.999)
        assert round(account.get_balance(), 3) == 0.001

        success = account.deduct(0.002)
        assert success is False
        assert round(account.get_balance(), 3) == 0.001
