# SLUG

Proton time-of-flight diagnostic for the JLF_2026 campaign (Keysight UXR0134A /
Tektronix MSO4054 oscilloscope traces). One of several diagnostics that will
eventually sit alongside this folder — the `good` flag in `shot_log.py` means
"is the SLUG data usable for this shot," not a verdict on the shot overall.

## Layout

- **`shot_log.py`** — shot organization. `SHOT_LOG` (target, thickness, note,
  good/bad per shot, all 43 shots) and `FILE_MAP` (which file(s)/channel(s)
  hold each shot's data). Start here if you're looking for "what happened on
  shot N."
- **`helpers/`** — generic plumbing: decoding raw h5/csv into calibrated
  `(time, voltage)` arrays (`loaders.py`), plotting (`plotting.py`).
- **`shot_characterization/`** — the actual pulse-finding logic
  (`characterize.py`): baseline/noise estimation, x-ray-candidate and
  proton-candidate detection, category labeling. This is a heuristic, not a
  substitute for eyeballing the plot.
- **`analysis/`** — notebooks that import from the three folders above.
  Start with `shot_review.ipynb`.

## Getting the data

Raw data isn't in git — see the top-level repo README. Once you have it
locally, either extract it into `SLUG/data/` (what `shot_log.py` expects by
default) or point the `JLF_SLUG_DATA_DIR` environment variable at wherever
you put it.

## Shot numbering

Shots are numbered 1–43 per the group's shot log. Not every number has data:
some were missed targets, blocked shots, or otherwise have nothing worth
keeping — `shot_log.NO_DATA_SHOTS` lists which.
