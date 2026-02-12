import numpy as np
from arcat.core import AR_categorization_scheme, AR_categorization_evolution_scheme


def test_short_event_downgrade():
    ivt = np.array([300, 300, 0])
    final_cat, cum_ivt, ivt_event, duration_event = AR_categorization_scheme(
        
        ivt,
        time_resolution_hours=6,  # Data resolution in hours
        bin_width=250.0,           # IVT bin size
        max_category=6             # Maximum AR category
    )
    
    assert np.all(final_cat[:2] == 0)

# Run the event-based AR scheme
def test_long_event_upgrade():
    ivt = np.array([800] * 12)
    # Run the evolution-based AR scheme
    final_cat, cum_ivt, ivt_event, duration_event = AR_categorization_evolution_scheme(
        ivt,
        time_resolution_hours=6,  # Data resolution in hours
        bin_width=250.0,           # IVT bin size
        max_category=6             # Maximum AR category
    )

    assert np.all(final_cat >= 3)