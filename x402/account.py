"""Prepaid USD balance account manager backed by local JSON file."""
import os
import json
import threading
from typing import Optional


class PrepaidUSDAccount:
    """Thread-safe prepaid USD account backed by local JSON file storage."""

    def __init__(self, file_path: Optional[str] = None):
        if file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "account_balance.json")
        self.file_path = file_path
        self._lock = threading.Lock()

        initial_env_val = float(os.environ.get("X402_PREPAID_BALANCE_USD", "1.00"))
        self._init_account(default_balance=initial_env_val)

    def _init_account(self, default_balance: float = 1.00) -> None:
        with self._lock:
            if not os.path.exists(self.file_path):
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                data = {"balance_usd": default_balance}
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

    def get_balance(self) -> float:
        """Get current prepaid USD balance."""
        with self._lock:
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        return float(data.get("balance_usd", 0.0))
                except Exception:
                    pass
            return 0.0

    def deduct(self, amount: float) -> bool:
        """Deduct specified USD amount if sufficient balance exists."""
        if amount <= 0:
            return True
        with self._lock:
            balance = 0.0
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        balance = float(data.get("balance_usd", 0.0))
                except Exception:
                    return False

            if balance >= amount:
                new_balance = round(balance - amount, 6)
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump({"balance_usd": new_balance}, f, indent=2)
                return True
            return False

    def top_up(self, amount: float) -> float:
        """Add funds to the prepaid USD account."""
        if amount <= 0:
            return self.get_balance()
        with self._lock:
            balance = 0.0
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        balance = float(data.get("balance_usd", 0.0))
                except Exception:
                    balance = 0.0
            new_balance = round(balance + amount, 6)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"balance_usd": new_balance}, f, indent=2)
            return new_balance
