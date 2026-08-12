"""Automated pulse characterization for a single decoded waveform.

Heuristic, not a substitute for eyeballing the plot: smooths the trace over a
fixed ~0.3 ns window, thresholds at 6-sigma above the pre-trigger baseline
noise, merges nearby excursions into discrete "features," calls the earliest
one the x-ray candidate (prompt, travels at c) and the largest later one the
proton candidate (TOF-delayed).
"""

import numpy as np


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

    if snr < 4:
        category = "No significant pulse (noise-level)"
    elif clipped:
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
        snr=snr, clipped=clipped, n_features=n_feat, features=sig_features,
        category=category, duration_ns=(t[-1] - t[0]) * 1e9,
        xray_candidate=xray, proton_candidate=proton,
    )
