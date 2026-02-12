"""
arcat: Atmospheric River Categorization Toolkit

Provides:
- Event-based AR categorization
- Evolution-based AR categorization
- xarray + Dask support
"""

from .version import __version__
from .core import (
    AR_categorization_scheme,
    AR_categorization_evolution_scheme,
)
