"""
Tests for mypackage.myscript.
"""

import pytest
from pathlib import Path
from typing import List
from mypackage.myscript import myfunction, do_math


@pytest.mark.parametrize(
    "directory_path,assume_result",
    [
        (Path(__file__).parent, ["test_myscript.py"]),
        (Path(__file__).parent.parent, ["tests", "mypackage"]),
    ],
)
def test_myfunction(directory_path: Path, assume_result: List[str]):
    """
    Test myfunction.
    """
    result = myfunction(directory_path=directory_path)
    assert all([assume in str(result) for assume in assume_result])


def test_do_math():
    """
    Test do_math.
    """
    result = do_math([1.0, 56.0, 345345.1, 45.436])
    assert isinstance(result, tuple)
