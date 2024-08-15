"""Measure the execution time of a function when called."""

import time
from collections.abc import Callable
from typing import Any

__all__ = ["timer"]


def timer(func: Callable, *args: Any, **kwargs: Any) -> tuple[Any, float]:
    """
    Measure the execution time of a function when called.

    Parameters
    ----------
    func : Callable
        The function to measure.
    *args : tuple
        Positional arguments to pass to the function.
    **kwargs : dict
        Keyword arguments to pass to the function.

    Returns
    -------
    tuple
        A tuple containing the result of the function and the execution duration.
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    execution_duration = end_time - start_time
    return result, execution_duration
