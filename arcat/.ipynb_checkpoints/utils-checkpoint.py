"""
Utility functions for AR categorization.
"""

import numpy as np


def compute_steps_per_day(time_resolution_hours: int) -> int:
    """
    Compute number of timesteps per day.

    Parameters
    ----------
    time_resolution_hours : int
        Temporal resolution of input data in hours.

    Returns
    -------
    int
        Number of timesteps corresponding to 1 day.
    """
    return int(24 / time_resolution_hours)


def bin_ivt(ivt_array: np.ndarray, bin_width: float, max_category: int):
    """
    Convert IVT values to AR categories.

    IVT is divided into bins of size `bin_width`.

    Example:
        0–249   -> 0
        250–499 -> 1
        etc.
    """
    bins = np.floor(ivt_array / bin_width)
    bins = np.clip(bins, 0, max_category)
    return bins.astype(int)


def cumulative_reset(values: np.ndarray, mask: np.ndarray):
    """
    Compute cumulative sum that resets when mask == 0.

    Used to compute cumulative IVT per AR event.
    """
    result = np.zeros_like(values, dtype=float)
    running_sum = 0.0

    for i in range(len(values)):
        if mask[i] == 0:
            running_sum = 0.0
        else:
            running_sum += values[i]
        result[i] = running_sum

    return result


def max_bounded_replace(arr: np.ndarray):
    """
    Replace each nonzero segment by its maximum value.

    Example:
        [1,2,3,0,2,1] -> [3,3,3,0,2,2]

    Used in event-based scheme to collapse AR event
    to peak intensity.
    """
    arr = arr.copy()
    n = len(arr)
    start = None

    for i in range(n):
        if arr[i] == 0:
            if start is not None:
                arr[start:i] = np.max(arr[start:i])
                start = None
        else:
            if start is None:
                start = i

    if start is not None:
        arr[start:n] = np.max(arr[start:n])

    return arr
