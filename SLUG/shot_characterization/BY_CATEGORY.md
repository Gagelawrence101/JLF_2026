# Shots by category

Same 35 shots-with-data as [README.md](README.md), grouped by auto-detected
category instead of by shot number — useful for e.g. pulling every "Single
narrow pulse" shot for a thickness scan, or eyeballing all the 🟡 shots
together to see if they share a common cause.

**Has ref ch. (Ch2)** — whether the shot's h5 file includes Channel 2, the
low-gain reference/noise-monitor channel (see `ref.ipynb` in the old
notebooks). ✅ means both Channel 2 and Channel 4 (and sometimes Channel 3)
were captured for that shot; `—` means either it's a single-channel h5
(Channel 4 only) or an old-scope Tektronix CSV shot, which doesn't have this
concept at all.

See [README.md](README.md) for what each category/color means.

---

### 🟢 Double pulse (prompt + delayed candidate) (5 shots)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 5 | ❌ | — | [<img src="waveforms/shot_5.png" width="180">](waveforms/shot_5.png) |
| 7 | ✅ | — | [<img src="waveforms/shot_7.png" width="180">](waveforms/shot_7.png) |
| 9 | ✅ | — | [<img src="waveforms/shot_9.png" width="180">](waveforms/shot_9.png) |
| 25 | ✅ | ✅ | [<img src="waveforms/shot_25.png" width="180">](waveforms/shot_25.png) |
| 26 | ✅ | ✅ | [<img src="waveforms/shot_26.png" width="180">](waveforms/shot_26.png) |

### 🟢 Single narrow pulse (17 shots)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 4 | ❌ | — | [<img src="waveforms/shot_4.png" width="180">](waveforms/shot_4.png) |
| 6 | ❌ | — | [<img src="waveforms/shot_6.png" width="180">](waveforms/shot_6.png) |
| 10 | ✅ | — | [<img src="waveforms/shot_10.png" width="180">](waveforms/shot_10.png) |
| 12 | ❌ | — | [<img src="waveforms/shot_12.png" width="180">](waveforms/shot_12.png) |
| 13 | ❌ | — | [<img src="waveforms/shot_13.png" width="180">](waveforms/shot_13.png) |
| 18 | ✅ | ✅ | [<img src="waveforms/shot_18.png" width="180">](waveforms/shot_18.png) |
| 28 | ❌ | — | [<img src="waveforms/shot_28.png" width="180">](waveforms/shot_28.png) |
| 30 | ❌ | — | [<img src="waveforms/shot_30.png" width="180">](waveforms/shot_30.png) |
| 34 | ❌ | ✅ | [<img src="waveforms/shot_34.png" width="180">](waveforms/shot_34.png) |
| 35 | ✅ | ✅ | [<img src="waveforms/shot_35.png" width="180">](waveforms/shot_35.png) |
| 36 | ✅ | ✅ | [<img src="waveforms/shot_36.png" width="180">](waveforms/shot_36.png) |
| 37 | ✅ | ✅ | [<img src="waveforms/shot_37.png" width="180">](waveforms/shot_37.png) |
| 38 | ✅ | ✅ | [<img src="waveforms/shot_38.png" width="180">](waveforms/shot_38.png) |
| 39 | ✅ | ✅ | [<img src="waveforms/shot_39.png" width="180">](waveforms/shot_39.png) |
| 41 | ✅ | ✅ | [<img src="waveforms/shot_41.png" width="180">](waveforms/shot_41.png) |
| 42 | ✅ | ✅ | [<img src="waveforms/shot_42.png" width="180">](waveforms/shot_42.png) |
| 43 | ✅ | ✅ | [<img src="waveforms/shot_43.png" width="180">](waveforms/shot_43.png) |

### 🟢 Single broad pulse (2 shots)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 22 | ✅ | ✅ | [<img src="waveforms/shot_22.png" width="180">](waveforms/shot_22.png) |
| 27 | ✅ | — | [<img src="waveforms/shot_27.png" width="180">](waveforms/shot_27.png) |

### 🟡 Multi-pulse / complex structure (8 shots)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 8 | ✅ | — | [<img src="waveforms/shot_8.png" width="180">](waveforms/shot_8.png) |
| 11 | ✅ | — | [<img src="waveforms/shot_11.png" width="180">](waveforms/shot_11.png) |
| 19 | ✅ | ✅ | [<img src="waveforms/shot_19.png" width="180">](waveforms/shot_19.png) |
| 20 | ✅ | ✅ | [<img src="waveforms/shot_20.png" width="180">](waveforms/shot_20.png) |
| 21 | ✅ | ✅ | [<img src="waveforms/shot_21.png" width="180">](waveforms/shot_21.png) |
| 23 | ❌ | ✅ | [<img src="waveforms/shot_23.png" width="180">](waveforms/shot_23.png) |
| 29 | ❌ | — | [<img src="waveforms/shot_29.png" width="180">](waveforms/shot_29.png) |
| 32 | ❌ | ✅ | [<img src="waveforms/shot_32.png" width="180">](waveforms/shot_32.png) |

### 🟡 Broad unresolved feature (no distinct sub-peaks) (1 shot)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 17 | ✅ | ✅ | [<img src="waveforms/shot_17.png" width="180">](waveforms/shot_17.png) |

### 🔴 Saturated / clipped pulse (1 shot)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 3 | ✅ | — | [<img src="waveforms/shot_3.png" width="180">](waveforms/shot_3.png) |

### 🔴 No significant pulse (noise-level) (1 shot)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 1 | ✅ | — | [<img src="waveforms/shot_1.png" width="180">](waveforms/shot_1.png) |

### 🔴 NO DATA FILE (8 shots)

| Shot | Log | Has ref ch. (Ch2) | Waveform |
|---|---|---|---|
| 2 | ❌ | — | — |
| 14 | ❌ | — | — |
| 15 | ✅ | — | — |
| 16 | ✅ | — | — |
| 24 | ❌ | — | — |
| 31 | ❌ | — | — |
| 33 | ❌ | — | — |
| 40 | ❌ | — | — |

## Quick takeaways

- **Reference channel coverage lines up with campaign date, not category.**
  Shots 1–13 never have Channel 2 (older single-channel setup). From shot 17
  onward it's standard on every shot with data — **except 27–30**, which were
  captured single-channel again for some reason, worth asking whoever ran
  those.
- The 🟡 "Multi-pulse/complex" group is a mix of both — having a reference
  channel doesn't predict which category a shot lands in, so ringing/noise
  isn't simply explained by "no reference channel to subtract."
