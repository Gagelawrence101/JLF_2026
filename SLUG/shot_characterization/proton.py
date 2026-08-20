"""Proton (delayed) feature characterization: envelope peak and onset.

Broad and noisy rather than a sharp spike -- on most shots. Two campaigns show
two different proton pulse shapes though: shots 9/11 have a narrow, sharp
proton spike (width at 50%-of-peak-height only 3.5-8ns), while the rest have
a broad, gradual ramp (17-36ns). A single fixed onset threshold can't handle
both: 50%-of-peak-envelope is right for the narrow spikes but leaves the
broad ramps' onset way up the slope instead of at its true base; 10% tracks
the broad ramps' true start well but walks too far back on the narrow spikes,
landing in pre-pulse noise. find_proton_onset() measures the feature's own
width first and picks the threshold accordingly.

Validated in analysis/proton_analysis.ipynb across all 10 usable double-pulse
shots (9, 11, 15, 16, 18-22, 27). Known broken on shots 25/26 (a positive bump
transitioning into a much bigger negative dip confuses the sign-agnostic
envelope search) -- treat results on those two as unreliable until that's
fixed.
"""

import numpy as np
from .characterize import boxcar_smooth


def find_proton_onset(t, v, baseline, xray_peak_i, envelope_smooth_ns=3.0,
                       dead_time_ns=8.0, search_window_ns=300.0,
                       narrow_width_thresh_ns=12.0, narrow_frac=0.5, broad_frac=0.1):
    t_ns = t * 1e9
    dt_ns = float(np.median(np.diff(t_ns[:min(2000, len(t_ns))])))
    dev = np.abs(v - baseline)
    win = max(1, int(round(envelope_smooth_ns / dt_ns)))
    envelope = boxcar_smooth(dev, win)

    xray_peak_ns = t_ns[xray_peak_i]
    mask = (t_ns > xray_peak_ns + dead_time_ns) & (t_ns < xray_peak_ns + search_window_ns)
    if not mask.any():
        return None
    idx = np.where(mask)[0]
    peak_i = idx[np.argmax(envelope[idx])]
    peak_env = envelope[peak_i]

    # classify narrow-spike vs. broad-ramp by width at 50% of peak height,
    # then pick the onset threshold suited to that shape (see module
    # docstring -- neither threshold works for both shapes)
    level50 = 0.5 * peak_env
    i = peak_i
    while i > 0 and envelope[i] > level50:
        i -= 1
    j = peak_i
    while j < len(envelope) - 1 and envelope[j] > level50:
        j += 1
    width50_ns = t_ns[j] - t_ns[i]
    onset_frac = narrow_frac if width50_ns < narrow_width_thresh_ns else broad_frac

    level = onset_frac * peak_env
    k = peak_i
    while k > xray_peak_i and envelope[k] > level:
        k -= 1
    onset_i = k

    return dict(
        peak_i=int(peak_i), onset_i=int(onset_i),
        peak_time_ns=float(t_ns[peak_i]), peak_val_V=float(v[peak_i]),
        onset_time_ns=float(t_ns[onset_i]), onset_val_V=float(v[onset_i]),
        width50_ns=float(width50_ns), onset_frac_used=onset_frac,
    )
