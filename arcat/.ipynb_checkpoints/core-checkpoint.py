"""
Core AR categorization algorithms for the arcat package.

This module contains:
- Event-based AR categorization (collapses to peak intensity)
- Evolution-based AR categorization (keeps intensity evolution)
- IVT-only and duration-only outputs for detailed analysis
"""

import numpy as np  # Import NumPy for array operations
from .utils import (  # Import helper functions from utils
    compute_steps_per_day,  # Converts time resolution (hours) to timesteps per day
    bin_ivt,                # Converts IVT values into AR categories
    cumulative_reset,       # Computes cumulative IVT resetting at zeros
    max_bounded_replace     # Collapses nonzero segments to their maximum value
)

# ------------------------
# Internal helper functions
# ------------------------

def _adjust_segment(arr, start, end, duration, steps_per_day):
    """
    Apply duration adjustment rule to a segment (in-place modification).

    Parameters
    ----------
    arr : np.ndarray
        Array of AR categories to modify.
    start : int
        Start index of the event segment.
    end : int
        End index of the event segment.
    duration : int
        Duration of the segment in timesteps.
    steps_per_day : int
        Number of timesteps that correspond to 1 day.
    """

    # If duration is shorter than 1 day, downgrade the category by 1
    if duration < steps_per_day:
        arr[start:end] -= 1  # Subtract 1 from all elements in the segment

    # If duration is longer than or equal to 2 days, upgrade the category by 1
    elif duration >= 2 * steps_per_day:
        arr[start:end] += 1  # Add 1 to all elements in the segment

    # Otherwise (duration 1–2 days), do nothing (leave category unchanged)

# ------------------------
def _apply_duration_rule(categories, steps_per_day, max_category):
    """
    Apply the duration adjustment to continuous AR events.

    Parameters
    ----------
    categories : np.ndarray
        Array of initial AR categories per timestep.
    steps_per_day : int
        Number of timesteps corresponding to 1 day.
    max_category : int
        Maximum AR category allowed.

    Returns
    -------
    final : np.ndarray
        Array of AR categories after duration adjustment.
    duration_arr : np.ndarray
        Array of duration (in timesteps) for each AR event at each index.
    """

    final = categories.copy()  # Copy categories to avoid modifying input
    n = len(categories)  # Total number of timesteps
    start = None  # Initialize start index of current event
    duration_arr = np.zeros_like(categories, dtype=float)  # Store duration per timestep

    # Loop over each timestep to find AR events
    for i in range(n):
        if categories[i] == 0:  # Found a zero → end of AR event
            if start is not None:  # There was an ongoing event
                end = i  # End index of the event
                duration = end - start  # Compute duration in timesteps
                _adjust_segment(final, start, end, duration, steps_per_day)  # Apply duration rule
                duration_arr[start:end] = duration  # Store duration for all timesteps in event
                start = None  # Reset start for next event
        else:
            if start is None:  # Found start of a new AR event
                start = i  # Mark start index

    # Handle event that goes until the last timestep
    if start is not None:
        end = n  # End index is last timestep
        duration = end - start  # Duration of the event
        _adjust_segment(final, start, end, duration, steps_per_day)  # Apply duration rule
        duration_arr[start:end] = duration  # Store duration

    # Ensure all categories are within allowed bounds
    return np.clip(final, 0, max_category), duration_arr  # Return adjusted categories and duration array

# ------------------------
# Event-based AR categorization
# ------------------------

def AR_categorization_scheme(
    ivt_array: np.ndarray,  # Input IVT values
    time_resolution_hours: int = 6,  # Time resolution of data in hours
    bin_width: float = 250.0,  # Width of each IVT bin for categorization
    max_category: int = 6  # Maximum AR category
):
    """
    Event-based AR categorization (collapses each event to peak intensity).

    Returns:
        final_categories : np.ndarray -> categorized AR values
        cumulative_ivt : np.ndarray -> cumulative IVT over AR events
        ivt_event : np.ndarray -> IVT values only during AR events
        duration_event : np.ndarray -> duration in timesteps for each AR event
    """

    # Compute how many timesteps correspond to 1 day
    steps_per_day = compute_steps_per_day(time_resolution_hours)

    # Copy IVT array to preserve original
    original_ivt = ivt_array.copy()

    # Bin IVT values into categories
    categories = bin_ivt(ivt_array, bin_width, max_category)

    # Collapse each nonzero event segment to its maximum value
    categories = max_bounded_replace(categories)

    # Apply duration rule to event segments and get duration per timestep
    final_categories, duration_event = _apply_duration_rule(categories, steps_per_day, max_category)

    # Create mask of where AR events occur (category > 0)
    mask = final_categories > 0

    # Compute cumulative IVT over AR events
    cumulative_ivt = cumulative_reset(original_ivt, mask)

    # Extract IVT values only during AR events, zero elsewhere
    ivt_event = np.where(mask, original_ivt, 0)

    # Return final categories, cumulative IVT, IVT-only, duration-only arrays
    return final_categories, cumulative_ivt, ivt_event, duration_event

# ------------------------
# Evolution-based AR categorization
# ------------------------

def AR_categorization_evolution_scheme(
    ivt_array: np.ndarray,  # Input IVT values
    time_resolution_hours: int = 6,  # Time resolution of data in hours
    bin_width: float = 250.0,  # IVT bin width
    max_category: int = 6  # Maximum AR category
):
    """
    Evolution-based AR categorization (keeps intensity evolution inside each event).

    Returns:
        final_categories : np.ndarray -> categorized AR values
        cumulative_ivt : np.ndarray -> cumulative IVT over AR events
        ivt_event : np.ndarray -> IVT values only during AR events
        duration_event : np.ndarray -> duration in timesteps for each AR event
    """

    # Compute timesteps per day
    steps_per_day = compute_steps_per_day(time_resolution_hours)

    # Copy IVT array to preserve original
    original_ivt = ivt_array.copy()

    # Bin IVT values into categories
    categories = bin_ivt(ivt_array, bin_width, max_category)

    # No collapsing for evolution scheme
    # Apply duration rule to event segments and get duration per timestep
    final_categories, duration_event = _apply_duration_rule(categories, steps_per_day, max_category)

    # Mask of AR events
    mask = final_categories > 0

    # Compute cumulative IVT over AR events
    cumulative_ivt = cumulative_reset(original_ivt, mask)

    # Extract IVT values only during AR events, zero elsewhere
    ivt_event = np.where(mask, original_ivt, 0)

    # Return final categories, cumulative IVT, IVT-only, duration-only arrays
    return final_categories, cumulative_ivt, ivt_event, duration_event
