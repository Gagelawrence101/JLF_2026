# shot_characterization

`characterize.py` — the pulse-finder. Takes a decoded `(time, voltage)` trace
from `helpers.loaders` and returns a category, plus x-ray/proton pulse
candidates if any are found. This is a heuristic (envelope-smooth, threshold,
merge nearby excursions into "features"), not a substitute for eyeballing
the plot — treat it as a first pass, especially on anything not in the
"plausible TOF" categories below.

## Categories

| Category | Meaning |
|---|---|
| `No significant pulse (noise-level)` | Signal never clears ~4x the baseline noise |
| `Saturated / clipped pulse` | ADC hit rail, or (Tek CSV) literal `inf` on over-range |
| `Broad unresolved feature (no distinct sub-peaks)` | Signal is above threshold but never resolves into a discrete feature |
| `Single narrow pulse` | One feature, width < 5% of the record span |
| `Single broad pulse` | One feature, width >= 5% of the record span |
| `Double pulse (prompt + delayed candidate)` | Two features — the classic x-ray-then-proton TOF signature |
| `Multi-pulse / complex structure` | 3+ features — often cable ringing/reflections rather than real physics, check manually |
| `NO DATA FILE` | Nothing in the archive for this shot |

## Every shot, by category (main channel only)

Regenerate this by running `characterize()` over `shot_log.ALL_SHOTS` — see
`analysis/shot_review.ipynb`'s summary table for the live version with SNR,
x-ray/proton timing, etc. Snapshot as of the last time this was run:

| Shot | Log status | Category |
|---|---|---|
| 1 | good | No significant pulse (noise-level) |
| 2 | bad | NO DATA FILE |
| 3 | good | Saturated / clipped pulse |
| 4 | bad | Single narrow pulse |
| 5 | bad | Double pulse (prompt + delayed candidate) |
| 6 | bad | Single narrow pulse |
| 7 | good | Double pulse (prompt + delayed candidate) |
| 8 | good | Multi-pulse / complex structure |
| 9 | good | Double pulse (prompt + delayed candidate) |
| 10 | good | Single narrow pulse |
| 11 | good | Multi-pulse / complex structure |
| 12 | bad | Single narrow pulse |
| 13 | bad | Single narrow pulse |
| 14 | bad | NO DATA FILE |
| 15 | good | NO DATA FILE |
| 16 | good | NO DATA FILE |
| 17 | good | Broad unresolved feature (no distinct sub-peaks) |
| 18 | good | Single narrow pulse |
| 19 | good | Multi-pulse / complex structure |
| 20 | good | Multi-pulse / complex structure |
| 21 | good | Multi-pulse / complex structure |
| 22 | good | Single broad pulse |
| 23 | bad | Multi-pulse / complex structure |
| 24 | bad | NO DATA FILE |
| 25 | good | Double pulse (prompt + delayed candidate) |
| 26 | good | Double pulse (prompt + delayed candidate) |
| 27 | good | Single broad pulse |
| 28 | bad | Single narrow pulse |
| 29 | bad | Multi-pulse / complex structure |
| 30 | bad | Single narrow pulse |
| 31 | bad | NO DATA FILE |
| 32 | bad | Multi-pulse / complex structure |
| 33 | bad | NO DATA FILE |
| 34 | bad | Single narrow pulse |
| 35 | good | Single narrow pulse |
| 36 | good | Single narrow pulse |
| 37 | good | Single narrow pulse |
| 38 | good | Single narrow pulse |
| 39 | good | Single narrow pulse |
| 40 | bad | NO DATA FILE |
| 41 | good | Single narrow pulse |
| 42 | good | Single narrow pulse |
| 43 | good | Single narrow pulse |

Two things worth flagging from this pass:
- **Shots 13 and 23** are logged as "No data" / "no real data" but both
  actually have a file with a detectable category — worth a manual look
  before trusting the log's call on those two.
- **"Multi-pulse / complex structure"** shots (8, 11, 19–21, 23, 29, 32) are
  the least trustworthy category — often cable ringing rather than a real
  third pulse. Check these visually via `analysis/shot_review.ipynb` before
  using them in anything quantitative.
