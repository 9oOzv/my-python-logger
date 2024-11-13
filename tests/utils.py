from random import (
    randint,
    uniform,
    choice
)
from typing import Any
import json

from datetime import datetime


Timestamp = str | int | float | datetime


def assert_timestamp(
    t: Timestamp,
    cmp: Timestamp = datetime.now(),
    threshold_seconds: int = 0.1
):
    if isinstance(t, str):
        t = datetime.fromisoformat(t)
    if isinstance(t, float) or isinstance(t, int):
        t = datetime.fromtimestamp(t)
    delta = cmp - t
    assert abs(delta.total_seconds()) < threshold_seconds


def assert_data(a: Any, b: Any):
    a = json.dumps(a, default=str)
    b = json.dumps(b, default=str)
    assert a == b
