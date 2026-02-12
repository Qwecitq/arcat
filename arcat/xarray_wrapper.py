import xarray as xr
import numpy as np
from .core import (
    AR_categorization_scheme,
    AR_categorization_evolution_scheme,
)


def apply_ar_scheme(
    ivt_da: xr.DataArray,
    scheme: str = "event",
    time_resolution_hours: int = 6,
):
    func = (
        AR_categorization_scheme
        if scheme == "event"
        else AR_categorization_evolution_scheme
    )

    categories, cumulative = xr.apply_ufunc(
        func,
        ivt_da,
        input_core_dims=[["time"]],
        output_core_dims=[["time"], ["time"]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[np.int32, np.float64],
        kwargs={"time_resolution_hours": time_resolution_hours},
    )

    return categories, cumulative
