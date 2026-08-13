"""Automated pulse characterization for a single decoded waveform.

Heuristic, not a substitute for eyeballing the plot: smooths the trace over a
fixed ~0.3 ns window, thresholds at 6-sigma above the pre-trigger baseline
noise, merges nearby excursions into discrete "features," calls the earliest
one the x-ray candidate (prompt, travels at c) and the largest later one the
proton candidate (TOF-delayed).
"""

import numpy as np

# A saturated/clipped pulse plateaus at the top instead of rounding off, so
# its width near full height (90%) is close to its width near half height
# (50%). A smooth, unclipped pulse is much narrower at 90% than at 50%.
# Deliberately a *ratio*, not a time -- this project mixes a 2.5 GS/s scope
# (old Tek CSV shots) with a ~128 GS/s scope (Keysight h5 shots), a 50x
# difference in time resolution, so any absolute-time plateau-width
# threshold would not be comparable across the two.
PLATEAU_RATIO_THRESH = 0.65


def boxcar_smooth(v, win):
    if win <= 1:
        return v.copy()
    kernel = np.ones(win) / win
    return np.convolve(v, kernel, mode="same")


def regions_above(mask):
    d = np.diff(mask.astype(np.int8))
    starts = np.where(d == 1)[0] + 1
    ends = np.where(d == -1)[0] + 1
    if mask[0]:
        starts = np.r_[0, starts]
    if mask[-1]:
        ends = np.r_[ends, len(mask)]
    return list(zip(starts, ends))


def plateau_ratio(t, v, baseline, min_w50_samples=8):
    """width-at-90%-height / width-at-50%-height of the dominant excursion,
    whichever direction (positive or negative-going) it is. Near 1.0 means
    a flat-topped/saturated pulse; well below ~0.5 means a smooth peak.

    The "dominant excursion" is the *widest* region crossing 50% of the
    global peak deviation, not whichever region happens to contain the
    first-occurring sample tied for the max value. That distinction matters:
    a real flat plateau has many samples tied at (or near) the peak, so
    argmax()'s first-occurrence tiebreak can land on an unrelated narrow
    spike elsewhere in the record that happens to reach the same height,
    completely missing the actual saturated region (found via shot 10,
    which has a 7ns hard-flat plateau that a peak-index-only search missed
    entirely in favor of a 0.2ns spike earlier in the trace).

    Deliberately uses the *raw* trace, not the boxcar-smoothed one used for
    peak-finding elsewhere: that smoothing window is sized for detecting
    pulses in general, and is wide enough relative to some genuinely narrow
    real spikes that it artificially broadens/flattens their top -- i.e. it
    creates a fake plateau rather than revealing a real one. Requires w50 to
    span a real number of samples (not just 1-2, which would make the ratio
    a discretization artifact rather than evidence of shape).
    """
    dev = v - baseline
    sign = 1 if abs(dev.max()) >= abs(dev.min()) else -1
    peak_val = baseline + sign * float(np.abs(dev).max())

    level50 = baseline + sign * 0.5 * abs(peak_val - baseline)
    mask50 = (v >= level50) if sign > 0 else (v <= level50)
    regs50 = regions_above(mask50)
    if not regs50:
        return 0.0
    s50, e50 = max(regs50, key=lambda se: se[1] - se[0])
    w50 = (t[e50 - 1] - t[s50]) * 1e9

    dt_ns = float(np.median(np.diff(t[:min(2000, len(t))]))) * 1e9
    if w50 <= 0 or w50 < min_w50_samples * dt_ns:
        return 0.0

    local_peak = v[s50:e50][np.argmax(v[s50:e50] * sign)]
    level90 = baseline + sign * 0.9 * abs(local_peak - baseline)
    mask90 = (v >= level90) if sign > 0 else (v <= level90)
    w90 = 0.0
    for s, e in regions_above(mask90):
        if s < e50 and e > s50:  # overlaps the chosen 50%-region
            w90 = max(w90, (t[min(e, e50) - 1] - t[max(s, s50)]) * 1e9)

    return w90 / w50 if w50 > 0 else 0.0


def characterize(t, v, clipped, baseline_frac=0.2, smooth_ns=0.3,
                  merge_gap_ns=3.0, min_region_ns=0.15, thresh_k=6.0,
                  rel_amp_frac=0.3, xray_proton_gap_ns=1.0):
    n = len(v)
    nb = max(10, int(n * baseline_frac))
    baseline = np.median(v[:nb])
    mad_raw = np.median(np.abs(v[:nb] - baseline)) * 1.4826
    noise_raw = mad_raw if mad_raw > 0 else np.std(v[:nb])
    noise_raw = noise_raw or 1e-12

    dt = float(np.median(np.diff(t[:min(2000, n)])))
    if dt <= 0:
        dt = float((t[-1] - t[0]) / max(1, n - 1))

    win = max(1, int(round((smooth_ns * 1e-9) / dt)))
    smooth = boxcar_smooth(v, win)
    base_s = np.median(smooth[:nb])
    noise_s = np.median(np.abs(smooth[:nb] - base_s)) * 1.4826
    if noise_s == 0:
        noise_s = noise_raw / max(1, np.sqrt(win))
    dev = np.abs(smooth - base_s)
    peak_amp = float(np.max(np.abs(v - base_s)))
    snr = peak_amp / noise_raw if noise_raw > 0 else 0

    thresh = thresh_k * noise_s
    mask = dev > thresh
    regs = regions_above(mask)
    min_region_samp = max(1, int(round((min_region_ns * 1e-9) / dt)))
    regs = [(s, e) for s, e in regs if (e - s) >= min_region_samp]
    merge_gap_samp = max(1, int(round((merge_gap_ns * 1e-9) / dt)))
    merged = []
    for s, e in regs:
        if merged and s - merged[-1][1] <= merge_gap_samp:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    regs = merged

    all_features = []
    for s, e in regs:
        seg = dev[s:e]
        pk_i = s + int(np.argmax(seg))
        all_features.append(dict(
            t_start_ns=t[s] * 1e9, t_end_ns=t[e - 1] * 1e9,
            width_ns=(t[e - 1] - t[s]) * 1e9, peak_time_ns=t[pk_i] * 1e9,
            peak_val_V=float(v[pk_i]), peak_dev_V=float(dev[pk_i]),
        ))

    sig_cut = rel_amp_frac * peak_amp
    sig_features = [dict(f) for f in all_features if f["peak_dev_V"] >= sig_cut]
    for f in sig_features:
        f.pop("peak_dev_V")
    n_feat = len(sig_features)

    plat_ratio = plateau_ratio(t, v, baseline) if snr >= 4 else 0.0
    is_flat_top = plat_ratio >= PLATEAU_RATIO_THRESH
    is_saturated = bool(clipped or is_flat_top)

    if snr < 4:
        category = "No significant pulse (noise-level)"
    elif is_saturated:
        category = "Saturated / clipped pulse"
    elif n_feat == 0:
        category = "Broad unresolved feature (no distinct sub-peaks)"
    elif n_feat == 1:
        w, span = sig_features[0]["width_ns"], (t[-1] - t[0]) * 1e9
        category = "Single narrow pulse" if w < 0.05 * span else "Single broad pulse"
    elif n_feat == 2:
        category = "Double pulse (prompt + delayed candidate)"
    else:
        category = "Multi-pulse / complex structure"

    xray = proton = None
    if all_features:
        by_time = sorted(all_features, key=lambda f: f["t_start_ns"])
        xray = by_time[0]
        later = [f for f in by_time[1:] if f["peak_time_ns"] > xray["peak_time_ns"] + xray_proton_gap_ns]
        if later:
            proton = max(later, key=lambda f: f["peak_dev_V"])
    for f in (xray, proton):
        if f:
            f.pop("peak_dev_V", None)

    return dict(
        n_points=n, baseline_V=baseline, noise_V=noise_raw, peak_amp_V=peak_amp,
        snr=snr, clipped=clipped, plateau_ratio=plat_ratio, is_flat_top=is_flat_top,
        is_saturated=is_saturated, n_features=n_feat, features=sig_features,
        category=category, duration_ns=(t[-1] - t[0]) * 1e9,
        xray_candidate=xray, proton_candidate=proton,
    )
