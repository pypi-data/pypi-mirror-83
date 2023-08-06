import json
import os

from .dt_resp import *


def test_load_sample_data():
    return

    in_file = os.path.join(os.path.dirname(__file__), "..", "test.json")
    out_file = os.path.join(os.path.dirname(__file__), "..", "out.json")

    with open(in_file) as fp:
        origin = json.load(fp)

    out = GenericResp(**origin)
    o2 = json.dumps(out.dict(), ensure_ascii=False)
    o1 = json.dumps(origin, ensure_ascii=False)

    assert o2 == o1
