"""
Contains a function.
"""
from pathlib import Path
from typing import List
import math


def myfunction(directory_path: Path) -> List[Path]:
    """
    Get files in directory_path.
    """
    return list(directory_path.glob("*"))


def do_math(values: List[float]):
    """
    Do some maths.
    """
    value_sum = sum(values)
    logs = [math.log10(val) for val in values]
    avg = value_sum / len(values)
    rads = [math.radians(val) for val in values]
    return value_sum, logs, avg, rads
