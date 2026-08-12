"""Plotting helpers for a single shot/channel's decoded waveform."""

import matplotlib.pyplot as plt

# Decimate full-record plots above this many points so matplotlib stays fast.
# shot 23 alone is ~80M points/channel -- an outlier, without this it hangs.
MAX_PLOT_POINTS = 200_000


def plot_shot(entries, load_channel_fn, characterize_fn, data_dir, zoom_pad_ns=50):
    """entries: list of (kind, path, channel_label) for one shot, as in FILE_MAP.
    load_channel_fn(data_dir, kind, path, ch) -> (t, v, clipped, ydisp)
    characterize_fn(t, v, clipped) -> result dict with xray_candidate/proton_candidate
    Returns the list of per-channel characterize() results, in entry order.
    """
    n = len(entries)
    fig, axes = plt.subplots(n, 2, figsize=(12, 3.2 * n), squeeze=False)
    results = []

    for i, (kind, path, ch) in enumerate(entries):
        t, v, clipped, ydisp = load_channel_fn(data_dir, kind, path, ch)
        res = characterize_fn(t, v, clipped)
        results.append(res)

        ax_full, ax_zoom = axes[i]
        t_ns = t * 1e9

        if len(t_ns) > MAX_PLOT_POINTS:
            stride = max(1, len(t_ns) // MAX_PLOT_POINTS)
            ax_full.plot(t_ns[::stride], v[::stride], lw=0.5)
            ax_full.set_title(f"{ch} — full record (decimated {stride}x for display)")
        else:
            ax_full.plot(t_ns, v, lw=0.5)
            ax_full.set_title(f"{ch} — full record")
        ax_full.set_xlabel("time (ns)")
        ax_full.set_ylabel("V")

        xr, pr = res["xray_candidate"], res["proton_candidate"]
        if xr:
            lo = xr["peak_time_ns"] - zoom_pad_ns
            hi = (pr["peak_time_ns"] if pr else xr["peak_time_ns"]) + zoom_pad_ns
            mask = (t_ns >= lo) & (t_ns <= hi)
            ax_zoom.plot(t_ns[mask], v[mask], lw=0.8)
            ax_zoom.axvline(xr["peak_time_ns"], color="tab:orange", ls="--", label="x-ray cand.")
            if pr:
                ax_zoom.axvline(pr["peak_time_ns"], color="tab:green", ls="--", label="proton cand.")
            ax_zoom.legend(fontsize=8)
            ax_zoom.set_title("zoom around detected feature(s)")
        else:
            if len(t_ns) > MAX_PLOT_POINTS:
                stride = max(1, len(t_ns) // MAX_PLOT_POINTS)
                ax_zoom.plot(t_ns[::stride], v[::stride], lw=0.5)
            else:
                ax_zoom.plot(t_ns, v, lw=0.5)
            ax_zoom.set_title("(no feature detected — showing full record)")
        ax_zoom.set_xlabel("time (ns)")

    plt.tight_layout()
    return results
