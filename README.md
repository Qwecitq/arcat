# ARCat: Atmospheric River Categorization Toolkit

**ARCat** is a Python package for **categorizing Atmospheric River (AR) events** based on Integrated Vapor Transport (IVT) data. It provides:

- **Event-based AR categorization**: Collapses each AR event to its peak intensity.
- **Evolution-based AR categorization**: Preserves the intensity evolution within AR events.

Additionally, ARCat computes:

- **Cumulative IVT** per AR event.
- **IVT-only values** for each AR event.
- **Duration-only values** (number of timesteps per event).

It is fully compatible with **NumPy arrays**, **xarray**, and **Dask**, allowing analysis of large datasets efficiently.

---

## Features

- Event-based and evolution-based AR categorization.
- Automatic handling of duration rules:
  - Events < 1 day → downgrade category
  - Events 1–2 days → unchanged
  - Events ≥ 2 days → upgrade category
- Maximum category enforcement.
- Option to extract IVT-only and duration-only arrays.
- Easy integration with **xarray/Dask** for large datasets.
- Fully documented and tested, with CI support.

---

## Installation

Clone the repository and install locally:

```bash
git clone https://github.com/yourusername/arcat.git
cd arcat
pip install -e .
````
## Quick Start

### Import the package

```python
import numpy as np
from arcat.core import AR_categorization_scheme, AR_categorization_evolution_scheme
```

### Prepare your IVT array

```python
# Example: random IVT values for demonstration
ivt = np.random.rand(20) * 1500  # IVT in kg/m/s
```

### Event-based AR categorization

```python
# Run the event-based AR scheme
final_cat, cum_ivt, ivt_event, duration_event = AR_categorization_scheme(
    ivt,
    time_resolution_hours=6,  # Data resolution in hours
    bin_width=250.0,           # IVT bin size
    max_category=6             # Maximum AR category
)

print("Categorized AR events:", final_cat)
print("Cumulative IVT:", cum_ivt)
print("IVT-only values:", ivt_event)
print("Duration per timestep:", duration_event)
```

### Evolution-based AR categorization

```python
# Run the evolution-based AR scheme
final_cat, cum_ivt, ivt_event, duration_event = AR_categorization_evolution_scheme(
    ivt,
    time_resolution_hours=6,  # Data resolution in hours
    bin_width=250.0,           # IVT bin size
    max_category=6             # Maximum AR category
)

print("Evolution categories:", final_cat)
print("Cumulative IVT:", cum_ivt)
print("IVT-only values:", ivt_event)
print("Duration per timestep:", duration_event)
```

---

## Parameters

| Parameter               | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| `ivt_array`             | 1D NumPy array of IVT values (kg/m/s)                   |
| `time_resolution_hours` | Temporal resolution of your data in hours (default: 6)  |
| `bin_width`             | Width of each IVT bin for categorization (default: 250) |
| `max_category`          | Maximum AR category (default: 6)                        |

---

## Returns

1. `final_categories`: Array of AR categories (1–6) after duration adjustments.
2. `cumulative_ivt`: Cumulative IVT during AR events.
3. `ivt_event`: Original IVT values during AR events (0 elsewhere).
4. `duration_event`: Number of timesteps per AR event (0 elsewhere).

---

## Usage Notes

* Event-based scheme collapses each AR event to its maximum intensity (`max_bounded_replace`).
* Evolution-based scheme preserves temporal evolution of IVT within AR events.
* Duration rules are applied **per continuous AR segment**.
* Works with any **NumPy array**, and can be integrated with **xarray or Dask arrays** for large datasets.

---
## Adopting for xarray data
```python
final_cat, cum_ivt, ivt_event, duration_event = xr.apply_ufunc(AR_categorization_scheme, 
                             Ivt_ds['IVT'].as_numpy(),
                             input_core_dims = [['time']],
                             output_core_dims = [['time'],['time'],['time'],['time']],
                             vectorize=True,  # Auto-vectorize over lat/lon
                             dask='parallelized',  # Enable parallelization using Dask
                             output_dtypes=[np.int8,np.float32,np.float32, np.int8])

```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests
5. Submit a pull request

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## References

* Ralph, F. M., Rutz, J. J., Cordeira, J. M., Dettinger, M., Anderson, M., Reynolds, D., ... & Smallcomb, C. (2019). A scale to characterize the strength and impacts of atmospheric rivers. Bulletin of the American Meteorological Society, 100(2), 269-289.
* Visit the [Atmospheric River Tracking Model Intercomparison Project (ARTMIP)](https://ncar.github.io/ARTMIP/intro.html) to follow Atmospheric River community research and publications.
