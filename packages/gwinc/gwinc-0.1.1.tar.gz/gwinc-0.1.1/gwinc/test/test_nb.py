import numpy as np

from .. import freq_from_spec, load_budget
from .. import nb


def test_nb():
    freq = freq_from_spec()
    budget = load_budget('Aplus', freq)
    assert np.all(budget.freq == freq)
