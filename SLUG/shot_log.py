"""Shot organization for the SLUG diagnostic.

SLUG is one diagnostic within the JLF_2026 campaign (Keysight UXR0134A /
Tektronix MSO4054 oscilloscope traces, proton time-of-flight). As other
diagnostics (streak camera, RCF, etc.) get their own folders alongside this
one, each will carry its own shot_log.py with the same shape -- the `good`
flag here specifically means "is the SLUG data usable for this shot," not a
verdict on the shot as a whole.

Source: the group's shot-log spreadsheet (Book 3.pdf). `good` mirrors that
sheet's own "Good Shot/no saturation" column -- it is not inferred here.
"""

import os

# Where the raw data actually lives. Defaults to a local `data/` folder next
# to this file (matches .gitignore, which excludes SLUG/data/) -- extract
# the shared-drive archive there, or point JLF_SLUG_DATA_DIR at wherever you
# already have it.
DATA_DIR = os.environ.get(
    "JLF_SLUG_DATA_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"),
)

SHOT_LOG = {
    1:  dict(target="Cu",      thickness_um=150,  note="",                  good=True),
    2:  dict(target="Cu",      thickness_um=150,  note="missed target",     good=False),
    3:  dict(target="Cu",      thickness_um=150,  note="",                  good=True),
    4:  dict(target="Cu",      thickness_um=150,  note="Protons saturated", good=False),
    5:  dict(target="Cu",      thickness_um=150,  note="Protons saturated", good=False),
    6:  dict(target="Cu",      thickness_um=150,  note="Protons saturated", good=False),
    7:  dict(target="Cu",      thickness_um=150,  note="",                  good=True),
    8:  dict(target="Cu",      thickness_um=50,   note="",                  good=True),
    9:  dict(target="Cu",      thickness_um=25,   note="",                  good=True),
    10: dict(target="Al",      thickness_um=7,    note="",                  good=True),
    11: dict(target="Al",      thickness_um=25,   note="sample rate bad",   good=True),
    12: dict(target="Al",      thickness_um=1.2,  note="No Protons",        good=False),
    13: dict(target="Mylar",   thickness_um=1,    note="No data",           good=False),
    14: dict(target="Cu film", thickness_um=100,  note="missed target",     good=False),
    15: dict(target="Cu film", thickness_um=100,  note="",                  good=True),
    16: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    17: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    18: dict(target="Al",      thickness_um=12.5, note="",                  good=True),
    19: dict(target="rod",     thickness_um=None, note="Slug moved",        good=True),
    20: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    21: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    22: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    23: dict(target="Mylar",   thickness_um=1,    note="no real data",      good=False),
    24: dict(target="Mylar",   thickness_um=1,    note="Missing",           good=False),
    25: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    26: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    27: dict(target="Mylar",   thickness_um=1,    note="",                  good=True),
    28: dict(target="Al",      thickness_um=1.2,  note="blocked",           good=False),
    29: dict(target="Mylar",   thickness_um=0.5,  note="blocked",           good=False),
    30: dict(target="Al",      thickness_um=0.65, note="blocked",           good=False),
    31: dict(target="Al",      thickness_um=2.5,  note="blocked",           good=False),
    32: dict(target="Mylar",   thickness_um=2,    note="blocked",           good=False),
    33: dict(target="Al",      thickness_um=0.65, note="missed target",     good=False),
    34: dict(target="Mylar",   thickness_um=0.5,  note="no protons",        good=False),
    35: dict(target="Al",      thickness_um=4.5,  note="",                  good=True),
    36: dict(target="Al",      thickness_um=2.5,  note="",                  good=True),
    37: dict(target="Al",      thickness_um=1.2,  note="",                  good=True),
    38: dict(target="Al",      thickness_um=0.65, note="",                  good=True),
    39: dict(target="Al",      thickness_um=4.5,  note="",                  good=True),
    40: dict(target="Mylar",   thickness_um=1,    note="no data",           good=False),
    41: dict(target="Al",      thickness_um=7,    note="",                  good=True),
    42: dict(target="CD",      thickness_um=25,   note="",                  good=True),
    43: dict(target="CD",      thickness_um=25,   note="",                  good=True),
}

# shot -> list of (kind, path, channel_label). Paths are relative to DATA_DIR.
# kind is "h5" (Keysight) or "csv" (Tektronix). Shots with an empty list have
# no data file in the archive at all -- usually because the log says the shot
# was missed/blocked/missing and nothing worth keeping was captured.
FILE_MAP = {
    1:  [("csv", "Shot 1_772026/tek0000ALL.csv", "CH1"),
         ("csv", "Shot 1_772026/tek0000ALL.csv", "CH3")],
    2:  [],  # missed target
    3:  [("csv", "Shot 3_782026/50um_Si_C8_C9.csv", "CH1")],
    4:  [("csv", "Shot 4_782026/tek0001CH1.csv", "CH1"),
         ("csv", "Shot 4_782026/tek0000RF3.csv", "REF3")],
    5:  [("csv", "Shot 5_792026/tek0000CH1.csv", "CH1")],
    6:  [("csv", "Shot 6_792026/tek0000CH1.csv", "CH1")],
    7:  [("csv", "Shot 7_792026/tek0000CH1.csv", "CH1")],
    8:  [("h5", "Shot 8_07102026/shot8.h5", "Channel 4")],
    9:  [("h5", "Shot 9_07102026/shot9.h5", "Channel 4")],
    10: [("h5", "Shot 10_ 07132026/shot10.h5", "Channel 4")],
    11: [("h5", "Shot 11_ 07132026/shot11.h5", "Channel 4")],
    12: [("h5", "Shot 12_ 07132026/shot12.h5", "Channel 4")],
    13: [("h5", "Shot 13_ 07132026/shot13.h5", "Channel 4")],
    14: [],  # missed target
    15: [],  # marked good in log, but no file in archive
    16: [],  # marked good in log, but no file in archive
    17: [("h5", "shot17.h5", "Channel 2"), ("h5", "shot17.h5", "Channel 4")],
    18: [("h5", "shot18.h5", "Channel 2"), ("h5", "shot18.h5", "Channel 4")],
    19: [("h5", "shot19.h5", "Channel 2"), ("h5", "shot19.h5", "Channel 4")],
    20: [("h5", "shot20.h5", "Channel 2"), ("h5", "shot20.h5", "Channel 4")],
    21: [("h5", "shot21.h5", "Channel 2"), ("h5", "shot21.h5", "Channel 3"), ("h5", "shot21.h5", "Channel 4")],
    22: [("h5", "shot22.h5", "Channel 2"), ("h5", "shot22.h5", "Channel 3"), ("h5", "shot22.h5", "Channel 4")],
    23: [("h5", "shot23.h5", "Channel 2"), ("h5", "shot23.h5", "Channel 3"), ("h5", "shot23.h5", "Channel 4")],  # 480 MB, 100 ms window -- an outlier
    24: [],  # "Missing" per log
    25: [("h5", "shot25.h5", "Channel 2"), ("h5", "shot25.h5", "Channel 4")],
    26: [("h5", "shot26.h5", "Channel 2"), ("h5", "shot26.h5", "Channel 3"), ("h5", "shot26.h5", "Channel 4")],
    27: [("h5", "shot27.h5", "Channel 4")],
    28: [("h5", "shot28.h5", "Channel 4")],
    29: [("h5", "shot29.h5", "Channel 4")],
    30: [("h5", "shot30.h5", "Channel 4")],
    31: [],  # blocked
    32: [("h5", "shot32.h5", "Channel 2"), ("h5", "shot32.h5", "Channel 4")],
    33: [],  # missed target
    34: [("h5", "shot34.h5", "Channel 2"), ("h5", "shot34.h5", "Channel 4")],
    35: [("h5", "shot35.h5", "Channel 2"), ("h5", "shot35.h5", "Channel 4")],
    36: [("h5", "shot36.h5", "Channel 2"), ("h5", "shot36.h5", "Channel 4")],
    37: [("h5", "shot37.h5", "Channel 2"), ("h5", "shot37.h5", "Channel 4")],
    38: [("h5", "shot38.h5", "Channel 2"), ("h5", "shot38.h5", "Channel 4")],
    39: [("h5", "shot39.h5", "Channel 2"), ("h5", "shot39.h5", "Channel 4")],
    40: [],  # no data
    41: [("h5", "shot41.h5", "Channel 2"), ("h5", "shot41.h5", "Channel 4")],
    42: [("h5", "shot42.h5", "Channel 2"), ("h5", "shot42.h5", "Channel 4")],
    43: [("h5", "shot43.h5", "Channel 2"), ("h5", "shot43.h5", "Channel 4")],
}

ALL_SHOTS = sorted(SHOT_LOG.keys())
GOOD_SHOTS = [s for s in ALL_SHOTS if SHOT_LOG[s]["good"]]
BAD_SHOTS = [s for s in ALL_SHOTS if not SHOT_LOG[s]["good"]]
NO_DATA_SHOTS = [s for s in ALL_SHOTS if not FILE_MAP.get(s)]


def main_channel_entry(shot):
    """The calibrated diode signal for a shot -- not the low-gain reference
    channel or the RF/EMP pickup on Channel 3."""
    entries = FILE_MAP.get(shot, [])
    for kind, path, ch in entries:
        if ch in ("Channel 4", "CH1"):
            return (kind, path, ch)
    return entries[0] if entries else None


def h5_channels_for(shot):
    """Unique h5 (Keysight) channel names for a shot, in file order."""
    seen = []
    for kind, path, ch in FILE_MAP.get(shot, []):
        if kind == "h5" and ch not in seen:
            seen.append(ch)
    return seen


if __name__ == "__main__":
    print(f"{len(ALL_SHOTS)} total shots: {len(GOOD_SHOTS)} good, {len(BAD_SHOTS)} bad/blocked/missing")
    print(f"{len(NO_DATA_SHOTS)} shots have no data file at all:", NO_DATA_SHOTS)
    print("DATA_DIR =", DATA_DIR)
