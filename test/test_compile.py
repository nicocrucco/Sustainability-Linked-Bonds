"""
Sustainability Linked Bond - Test Suite
"""

from src.slb_app import SLB


def test_app_compile() -> None:
    SLB().dump("./src/artifacts")
