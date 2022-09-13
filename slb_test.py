"""
Sustainability Linked Bond - Test Suite
"""

import json
from slb_app import SLB


def test_app_compile() -> None:

    slb = SLB()

    with open("slb_abi.json", "w") as f:
        f.write(json.dumps(slb.contract.dictify(), indent=4))

    with open("slb_approval.teal", "w") as f:
        f.write(slb.approval_program)

    with open("slb_clear.teal", "w") as f:
        f.write(slb.clear_program)
