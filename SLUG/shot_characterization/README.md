# shot_characterization

`characterize.py` — the pulse-finder. Takes a decoded `(time, voltage)` trace
from `helpers.loaders` and returns a category, plus x-ray/proton pulse
candidates if any are found. This is a heuristic (envelope-smooth, threshold,
merge nearby excursions into "features"), not a substitute for eyeballing
the plot — click a waveform below before trusting anything in 🟡 or 🔴.

## Categories

| | Category | Meaning |
|---|---|---|
| 🟢 | `Single narrow/broad pulse` | One clean feature |
| 🟢 | `Double pulse (prompt + delayed candidate)` | Two features — the classic x-ray-then-proton TOF signature |
| 🟡 | `Multi-pulse / complex structure` | 3+ features — often cable ringing/reflections rather than real physics, check manually |
| 🟡 | `Broad unresolved feature` | Above threshold but never resolves into a discrete feature |
| 🔴 | `No significant pulse (noise-level)` | Signal never clears ~4x the baseline noise |
| 🔴 | `Saturated / clipped pulse` | ADC hit rail, or (Tek CSV) literal `inf` on over-range |
| 🔴 | `NO DATA FILE` | Nothing in the archive for this shot |

**Log** column is the shot-log's own good/bad call (✅/❌), independent of the
category above — a shot can be logged good but still land in 🔴/🟡 here (or
vice versa), which is itself worth noticing.

Waveform images and the table below are a **snapshot** — regenerate with
`analysis/shot_review.ipynb`'s `next_shot()`/summary table for live results,
or rerun the image-generation pass if the data changes.

## Every shot

Click any waveform to open it full-size.

| Shot | Log | Category | Waveform |
|---|---|---|---|
| 1 | ✅ | 🔴 No significant pulse (noise-level) | [<img src="waveforms/shot_1.png" width="180">](waveforms/shot_1.png) |
| 2 | ❌ | 🔴 NO DATA FILE | — |
| 3 | ✅ | 🔴 Saturated / clipped pulse | [<img src="waveforms/shot_3.png" width="180">](waveforms/shot_3.png) |
| 4 | ❌ | 🟢 Single narrow pulse | [<img src="waveforms/shot_4.png" width="180">](waveforms/shot_4.png) |
| 5 | ❌ | 🟢 Double pulse (prompt + delayed candidate) | [<img src="waveforms/shot_5.png" width="180">](waveforms/shot_5.png) |
| 6 | ❌ | 🟢 Single narrow pulse | [<img src="waveforms/shot_6.png" width="180">](waveforms/shot_6.png) |
| 7 | ✅ | 🟢 Double pulse (prompt + delayed candidate) | [<img src="waveforms/shot_7.png" width="180">](waveforms/shot_7.png) |
| 8 | ✅ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_8.png" width="180">](waveforms/shot_8.png) |
| 9 | ✅ | 🟢 Double pulse (prompt + delayed candidate) | [<img src="waveforms/shot_9.png" width="180">](waveforms/shot_9.png) |
| 10 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_10.png" width="180">](waveforms/shot_10.png) |
| 11 | ✅ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_11.png" width="180">](waveforms/shot_11.png) |
| 12 | ❌ | 🟢 Single narrow pulse | [<img src="waveforms/shot_12.png" width="180">](waveforms/shot_12.png) |
| 13 | ❌ | 🟢 Single narrow pulse | [<img src="waveforms/shot_13.png" width="180">](waveforms/shot_13.png) |
| 14 | ❌ | 🔴 NO DATA FILE | — |
| 15 | ✅ | 🔴 NO DATA FILE | — |
| 16 | ✅ | 🔴 NO DATA FILE | — |
| 17 | ✅ | 🟡 Broad unresolved feature (no distinct sub-peaks) | [<img src="waveforms/shot_17.png" width="180">](waveforms/shot_17.png) |
| 18 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_18.png" width="180">](waveforms/shot_18.png) |
| 19 | ✅ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_19.png" width="180">](waveforms/shot_19.png) |
| 20 | ✅ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_20.png" width="180">](waveforms/shot_20.png) |
| 21 | ✅ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_21.png" width="180">](waveforms/shot_21.png) |
| 22 | ✅ | 🟢 Single broad pulse | [<img src="waveforms/shot_22.png" width="180">](waveforms/shot_22.png) |
| 23 | ❌ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_23.png" width="180">](waveforms/shot_23.png) |
| 24 | ❌ | 🔴 NO DATA FILE | — |
| 25 | ✅ | 🟢 Double pulse (prompt + delayed candidate) | [<img src="waveforms/shot_25.png" width="180">](waveforms/shot_25.png) |
| 26 | ✅ | 🟢 Double pulse (prompt + delayed candidate) | [<img src="waveforms/shot_26.png" width="180">](waveforms/shot_26.png) |
| 27 | ✅ | 🟢 Single broad pulse | [<img src="waveforms/shot_27.png" width="180">](waveforms/shot_27.png) |
| 28 | ❌ | 🟢 Single narrow pulse | [<img src="waveforms/shot_28.png" width="180">](waveforms/shot_28.png) |
| 29 | ❌ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_29.png" width="180">](waveforms/shot_29.png) |
| 30 | ❌ | 🟢 Single narrow pulse | [<img src="waveforms/shot_30.png" width="180">](waveforms/shot_30.png) |
| 31 | ❌ | 🔴 NO DATA FILE | — |
| 32 | ❌ | 🟡 Multi-pulse / complex structure | [<img src="waveforms/shot_32.png" width="180">](waveforms/shot_32.png) |
| 33 | ❌ | 🔴 NO DATA FILE | — |
| 34 | ❌ | 🟢 Single narrow pulse | [<img src="waveforms/shot_34.png" width="180">](waveforms/shot_34.png) |
| 35 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_35.png" width="180">](waveforms/shot_35.png) |
| 36 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_36.png" width="180">](waveforms/shot_36.png) |
| 37 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_37.png" width="180">](waveforms/shot_37.png) |
| 38 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_38.png" width="180">](waveforms/shot_38.png) |
| 39 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_39.png" width="180">](waveforms/shot_39.png) |
| 40 | ❌ | 🔴 NO DATA FILE | — |
| 41 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_41.png" width="180">](waveforms/shot_41.png) |
| 42 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_42.png" width="180">](waveforms/shot_42.png) |
| 43 | ✅ | 🟢 Single narrow pulse | [<img src="waveforms/shot_43.png" width="180">](waveforms/shot_43.png) |

Two things worth flagging from this pass:
- **Shots 13 and 23** are logged as "No data" / "no real data" but both
  actually have a file with a detectable category — worth a manual look
  before trusting the log's call on those two.
- **🟡 shots** (8, 11, 17, 19–21, 23, 29, 32) are the least trustworthy —
  often cable ringing rather than a real third pulse. Check these visually
  before using them in anything quantitative.
