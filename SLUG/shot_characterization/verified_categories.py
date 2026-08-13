"""Human-verified pulse categories, from a full shot-by-shot manual review
(every one of the 37 shots with data, checked against the waveform image).

This is the source of truth for category going forward -- characterize()'s
auto-detected category is still computed and available, but it's known to
mis-split noisy "sharp x-ray spike + broad proton hump" shots into too many
sub-features (see characterize.py's module docstring / README.md), so don't
treat auto disagreement with this dict as the auto version being right.

Where this disagrees with SHOT_LOG's good/bad call, that's intentional --
shape review can override the log (e.g. shot 7: log says good, but the
pulse is clearly flat-topped/saturated by eye).
"""

VERIFIED_CATEGORY = {
    1:  "No significant pulse (noise-level)",
    3:  "Saturated / clipped pulse",
    4:  "Saturated / clipped pulse",
    5:  "Saturated / clipped pulse",
    6:  "Saturated / clipped pulse",
    7:  "Saturated / clipped pulse",   # log says good; shape overrides
    8:  "No significant pulse (noise-level)",  # auto said multi-pulse; it's ringing, not a real pulse
    9:  "Double pulse (prompt + delayed candidate)",
    10: "Saturated / clipped pulse",
    11: "Double pulse (prompt + delayed candidate)",  # revisited: two clean, well-separated narrow spikes (~96, ~110ns)
    12: "Single narrow pulse",
    13: "Single narrow pulse",
    15: "Double pulse (prompt + delayed candidate)",  # auto said multi-pulse
    16: "Double pulse (prompt + delayed candidate)",  # auto said multi-pulse
    17: "Broad unresolved feature (no distinct sub-peaks)",
    18: "Double pulse (prompt + delayed candidate)",  # auto said single narrow
    19: "Double pulse (prompt + delayed candidate)",  # auto said multi-pulse
    20: "Double pulse (prompt + delayed candidate)",  # auto said multi-pulse
    21: "Double pulse (prompt + delayed candidate)",  # auto said multi-pulse
    22: "Double pulse (prompt + delayed candidate)",  # auto said single broad
    23: "No significant pulse (noise-level)",  # auto said multi-pulse; continuous ringing, no real pulse
    25: "Double pulse (prompt + delayed candidate)",
    26: "Double pulse (prompt + delayed candidate)",
    27: "Double pulse (prompt + delayed candidate)",  # auto said single broad
    28: "Single narrow pulse",
    29: "Single narrow pulse",  # auto said multi-pulse; burst+ringdown, one real transient
    30: "Single narrow pulse",
    32: "Single narrow pulse",  # auto said multi-pulse; burst+ringdown, one real transient
    34: "Single narrow pulse",
    35: "Single narrow pulse",
    36: "Single narrow pulse",
    37: "Single narrow pulse",
    38: "Single narrow pulse",
    39: "Single narrow pulse",
    41: "Single narrow pulse",
    42: "Single narrow pulse",
    43: "Single narrow pulse",
}
