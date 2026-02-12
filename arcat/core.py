"""
Core AR categorization algorithms.

Contains:
- Event-based scheme
- Evolution-based scheme
"""

import numpy as np
from .utils import (
    compute_steps_per_day,
    bin_ivt,
    cumulative_reset,
    max_bounded_replace,
)


def _adjust_segment(arr, start, end, duration, steps_per_day):
    """
    Apply duration adjustment rule to a segment.

    Rules:
    - < 1 day  -> downgrade
    - 1–2 days -> unchanged
    - >= 2 days -> upgrade
    """
    if duration < steps_per_day:
        arr[start:end] -= 1
    elif duration >= 2 * steps_per_day:
        arr[start:end] += 1


def _apply_duration_rule(categories, steps_per_day, max_category):
    """
    Apply duration adjustment to continuous AR events.

    Events are defined as consecutive timesteps
    where category > 0.
    """
    final = categories.copy()
    n = len(categories)
    start = None

    for i in range(n):
        if categories[i] == 0:
            if start is not None:
                end = i
                duration = end - start
                _adjust_segment(final, start, end, duration, steps_per_day)
                start = None
        else:
            if start is None:
                start = i

    if start is not None:
        end = n
        duration = end - start
        _adjust_segment(final, start, end, duration, steps_per_day)

    return np.clip(final, 0, max_category)


# ============================================================
# EVENT-BASED SCHEME
# ============================================================

def AR_categorization_scheme(
    ivt_array: np.ndarray,
    time_resolution_hours: int = 6,
    bin_width: float = 250.0,
    max_category: int = 6,
):
    """
    Event-based AR categorization.

    Steps:
    1. Bin IVT into categories
    2. Collapse each AR event to peak intensity
    3. Apply duration rule to event
    4. Compute cumulative IVT
    """

    steps_per_day = compute_steps_per_day(time_resolution_hours)

    original_ivt = ivt_array.copy()

    categories = bin_ivt(ivt_array, bin_width, max_category)
    categories = max_bounded_replace(categories)

    final_categories = _apply_duration_rule(
        categories, steps_per_day, max_category
    )

    mask = final_categories > 0
    cumulative_ivt = cumulative_reset(original_ivt, mask)

    return final_categories, cumulative_ivt


# ============================================================
# EVOLUTION-BASED SCHEME
# ============================================================

def AR_categorization_evolution_scheme(
    ivt_array: np.ndarray,
    time_resolution_hours: int = 6,
    bin_width: float = 250.0,
    max_category: int = 6,
):
    """
    Evolution-based AR categorization.

    Same as event-based scheme except:
    - Does NOT collapse event to peak intensity.
    - Duration rule still applied event-wise.
    """

    steps_per_day = compute_steps_per_day(time_resolution_hours)

    original_ivt = ivt_array.copy()

    categories = bin_ivt(ivt_array, bin_width, max_category)

    final_categories = _apply_duration_rule(
        categories, steps_per_day, max_category
    )

    mask = final_categories > 0
    cumulative_ivt = cumulative_reset(original_ivt, mask)

    return final_categories, cumulative_ivt
