import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from x402.fx_engine import FXEngine


def test_fallback_rate():
    """Mock network failure and assert rate falls back to 83.50."""
    engine = FXEngine(fallback_rate=83.50)
    with patch("httpx.get", side_effect=Exception("Network error")):
        rate = engine.get_rate()
        assert rate == 83.50


def test_dual_format():
    """Assert dual format contains USD and INR currency symbol."""
    engine = FXEngine(fallback_rate=83.50)
    formatted = engine.format_dual(0.002)
    assert "$0.002 (₹" in formatted
