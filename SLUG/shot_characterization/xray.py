"""X-ray (prompt) feature characterization: peak, onset, rise/fall time, FWHM.

Validated in analysis/xray_analysis.ipynb across all 12 verified double-pulse
shots before being promoted here.
"""

import numpy as np
from .characterize import boxcar_smooth


def find_xray_shape(t, v, baseline, noise, peak_search_frac=0.5, peak_local_ns=2.0,
                     onset_sigma=2.0, fall_search_ns=5.0):
    t_ns = t * 1e9
    dt_ns = float(np.median(np.diff(t_ns[:min(2000, len(t_ns))])))
    dev = np.abs(v - baseline)
    global_peak = dev.max()

    # peak: raw-signal threshold crossing, refined to local max
    thresh = peak_search_frac * global_peak
    above = np.where(dev >= thresh)[0]
    if len(above) == 0:
        return None
    first_i = above[0]
    win_samp = max(1, int(round(peak_local_ns / dt_ns)))
    lo, hi = max(0, first_i - win_samp), min(len(v), first_i + win_samp)
    peak_i = lo + int(np.argmax(dev[lo:hi]))
    peak_dev = dev[peak_i]

    # onset: walk backward from peak to ~baseline noise level
    onset_thresh = onset_sigma * noise
    i = peak_i
    while i > 0 and dev[i] > onset_thresh:
        i -= 1
    onset_i = i

    # rise edge: bounded to [onset, peak] -- the pulse's own validated start,
    # not a fixed window that can span into unrelated earlier noise (a fixed
    # window picked up pre-pulse noise on several shots and produced ~4-5ns
    # "rise times" that were really just the window boundary)
    def first_cross_rise(level):
        for j in range(onset_i, peak_i + 1):
            if dev[j] >= level:
                return j
        return None

    # fall edge: first crossing walking forward from the peak, within a
    # fixed window -- these pulses ring for several ns after the peak, so
    # the *last* crossing in a window picks up a random later ringing bump
    # instead of the true initial decay (found via shot 9: 25x too large)
    fall_search_samp = max(1, int(round(fall_search_ns / dt_ns)))
    hi2 = min(len(v), peak_i + fall_search_samp)

    def first_cross_fall(level):
        for j in range(peak_i, hi2):
            if dev[j] <= level:
                return j
        return None

    edges = {}
    for frac, name in [(0.1, "10"), (0.5, "50"), (0.9, "90")]:
        edges[f"r{name}_i"] = first_cross_rise(frac * peak_dev)
        edges[f"f{name}_i"] = first_cross_fall(frac * peak_dev)

    def t_of(key):
        i = edges.get(key)
        return float(t_ns[i]) if i is not None else None

    rise_time = (t_of("r90_i") - t_of("r10_i")) if edges["r90_i"] is not None and edges["r10_i"] is not None else None
    fall_time = (t_of("f10_i") - t_of("f90_i")) if edges["f10_i"] is not None and edges["f90_i"] is not None else None
    fwhm = (t_of("f50_i") - t_of("r50_i")) if edges["f50_i"] is not None and edges["r50_i"] is not None else None

    return dict(
        peak_i=peak_i, onset_i=onset_i,
        peak_time_ns=float(t_ns[peak_i]), peak_val_V=float(v[peak_i]),
        onset_time_ns=float(t_ns[onset_i]), onset_val_V=float(v[onset_i]),
        rise_time_ns=rise_time, fall_time_ns=fall_time, fwhm_ns=fwhm,
        edge_times_ns={k: t_of(k) for k in edges},
    )
