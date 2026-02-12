import numpy as np
from arcat.core import AR_categorization_scheme


def test_short_event_downgrade():
    ivt = np.array([300, 300, 0])
    cat, _ = AR_categorization_scheme(ivt, time_resolution_hours=6)
    assert np.all(cat[:2] == 0)


def test_long_event_upgrade():
    ivt = np.array([800] * 12)
    cat, _ = AR_categorization_scheme(ivt, time_resolution_hours=6)
    assert np.all(cat >= 3)
