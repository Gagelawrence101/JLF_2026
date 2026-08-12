"""Decode raw scope files into calibrated (time_s, voltage_V, clipped) arrays.

Two data eras in the SLUG archive:
- Keysight UXR0134A: raw ADC counts + per-channel scale factors in HDF5
  (Waveforms/<Channel>/...).
- Older Tektronix MSO4054: already-calibrated CSV export (TIME,<CH> columns).
"""

import h5py
import numpy as np


def load_h5_channel(full_path, chname):
    with h5py.File(full_path, "r") as f:
        grp = f[f"Waveforms/{chname}"]
        a = grp.attrs
        counts = f[f"Waveforms/{chname}/{chname}Data"][:]
        xorg, xinc = float(a["XOrg"]), float(a["XInc"])
        yorg, yinc = float(a["YOrg"]), float(a["YInc"])
        yref = float(a.get("YReference", 0))
        ydisp = float(a.get("YDispRange", np.nan))
    t = xorg + np.arange(counts.shape[0]) * xinc
    v = yorg + (counts.astype(np.float64) - yref) * yinc
    cmin, cmax = np.iinfo(np.int16).min, np.iinfo(np.int16).max
    clipped = bool(np.any(counts <= cmin + 1) or np.any(counts >= cmax - 1))
    return t, v, clipped, ydisp


def load_csv_channel(full_path, colname):
    with open(full_path, "r", errors="replace") as fh:
        lines = fh.readlines()
    header_idx = next(i for i, line in enumerate(lines) if line.strip().startswith("TIME,"))
    header = [h.strip() for h in lines[header_idx].strip().split(",")]
    col_idx = header.index(colname)
    t, v = [], []
    for line in lines[header_idx + 1:]:
        parts = line.strip().split(",")
        if len(parts) <= col_idx:
            continue
        try:
            tv, vv = float(parts[0]), float(parts[col_idx])
        except ValueError:
            continue
        t.append(tv)
        v.append(vv)
    t, v = np.array(t), np.array(v)
    clipped = bool(np.any(~np.isfinite(v)))  # Tek export writes literal "inf" on over-range
    finite = np.isfinite(v)
    return t[finite], v[finite], clipped, None


def load_channel(data_dir, kind, rel_path, chname):
    import os
    full_path = os.path.join(data_dir, rel_path)
    if kind == "h5":
        return load_h5_channel(full_path, chname)
    return load_csv_channel(full_path, chname)
