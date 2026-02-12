import numpy as np
import time
from arcat.core import AR_categorization_scheme

ivt = np.random.rand(10_000_000) * 1500

t0 = time.time()
AR_categorization_scheme(ivt)
print("Elapsed:", time.time() - t0)
