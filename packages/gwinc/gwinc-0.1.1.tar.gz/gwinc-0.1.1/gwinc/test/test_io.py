import os
import numpy as np

from .. import IFOS, load_budget
from .. import io


def test_io(tmpdir):
    freq = np.logspace(
        np.log10(5),
        np.log10(6000),
        1000,
    )
    budget = load_budget(IFOS[0], freq)
    traces = budget.run()
    path = os.path.join(tmpdir, 'foo.h5')
    io.save_hdf5(path, traces, ifo=budget.ifo)
    otraces = io.load_hdf5(path)
    assert np.all(traces.freq == otraces.freq)
    assert np.all(traces.psd == otraces.psd)
    for name, trace in otraces.items():
        assert np.all(traces[name].freq == trace.freq)
        assert np.all(traces[name].psd == trace.psd)
    assert budget.ifo == otraces.ifo
