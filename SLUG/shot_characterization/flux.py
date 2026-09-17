"""Proton flux (dN/dE) from the diamond detector's charge signal, via PSTAR.

The diamond detector's signal is a *current*, not a proton count -- each
proton crossing the diamond deposits energy via ionization, creating
electron-hole pairs swept out as current. Recovering proton count per
energy bin:

    1. I(t) = v_signal(t) / R_load           -- current from the corrected
                                                 voltage (needs the Pockels
                                                 correction first: only a
                                                 signal linear in the true
                                                 detector current can be
                                                 divided by a resistance to
                                                 get a physically meaningful
                                                 current)
    2. PSTAR gives the stopping power dE/dx(E) for protons in carbon: how
       much energy *one* proton at energy E deposits crossing the diamond
    3. That deposited energy, divided by diamond's ~13 eV per
       electron-hole pair, gives the charge q(E) one proton contributes
    4. dN/dE = [I(t) / q(E)] * |dt/dE|, reusing the TOF Jacobian already
       used to build the energy axis (see energy_spectrum.ipynb)

Recovered from the original preliminary/spectrum.ipynb notebooks (same
source as the TOF-to-energy physics in energy_spectrum.ipynb) -- these
constants and the PSTAR table were already worked out before this project's
notebooks existed, just never ported in.

Detector: 30 micron thick diamond, 400x600 micron active area,
density 3.51 g/cm^3. Assumes R_load = 50 Ohm and charge collection
efficiency (CCE) = 1 (optimistic upper bound -- real diamond detectors
typically run 60-90% depending on bias and crystal quality).
"""

import numpy as np

from .characterize import boxcar_smooth

# NIST PSTAR -- proton total stopping power in carbon (MeV cm^2/g). Mass
# stopping power is density-independent; diamond's actual density is
# applied separately in charge_per_proton().
PSTAR_ENERGY_MEV = np.array([
    8.0, 8.5, 9.0, 9.5, 10.0, 12.5, 15.0, 17.5, 20.0,
    25.0, 27.5, 30.0, 35.0, 40.0,
])
PSTAR_STOPPING_POWER = np.array([  # MeV cm^2/g
    48.47, 46.20, 44.14, 42.27, 40.57, 33.91, 29.26, 25.83, 23.18,
    19.34, 17.91, 16.69, 14.74, 13.24,
])

RHO_DIAMOND = 3.51        # g/cm^3
THICKNESS_CM = 30e-4      # 30 micron
R_LOAD = 50.0             # ohms
W_EHPAIR_EV = 13.0        # eV per electron-hole pair in diamond
CCE = 1.0                 # charge collection efficiency (optimistic upper bound)
ACTIVE_AREA_UM = (400, 600)

E_CHARGE = 1.602176634e-19  # C

_log_e = np.log(PSTAR_ENERGY_MEV)
_log_s = np.log(PSTAR_STOPPING_POWER)


def stopping_power(energy_mev):
    """Proton stopping power in carbon (MeV cm^2/g), log-log interpolated
    from the PSTAR table. Smooth in log-log space, unlike linear."""
    return np.exp(np.interp(np.log(energy_mev), _log_e, _log_s))


def charge_per_proton(energy_mev, rho=RHO_DIAMOND, thickness_cm=THICKNESS_CM,
                       w_ehpair_ev=W_EHPAIR_EV, cce=CCE):
    """Charge (C) deposited by a single proton of the given energy crossing
    the diamond: PSTAR stopping power -> deposited energy -> e-h pairs."""
    dE_dep_mev = stopping_power(energy_mev) * rho * thickness_cm
    n_ehpairs = (dE_dep_mev * 1e6) / w_ehpair_ev
    return E_CHARGE * n_ehpairs * cce


def flag_jitter_outliers(v_signal, t_ns, baseline_mask, smooth_ns=2.0, n_sigma=5.0):
    """Flag samples where the corrected signal deviates from its own local
    trend by more than n_sigma times the pre-pulse baseline noise -- a
    *different* failure mode from pockels.py's T-based unstable_mask, and
    both matter for flux specifically (T-based catches literally-invalid or
    near-invalid transmission; this catches noise jitter riding on top of
    an otherwise-real trend).

    Why a separate check: an earlier, simpler diagnostic in this session
    flagged "large |v_signal|" near the pulse peak as automatically
    suspicious -- but that was wrong. Two shots sharing the same EOM bias
    voltage (19 and 20) showed identical large boundary values regardless
    of their very different noise levels, which turned out to mean those
    values were just the transmission curve's value at a fixed T
    threshold, not a symptom of amplified noise -- a real, growing pulse
    legitimately reaches its largest amplitude near its own peak. Penalizing
    "large" would incorrectly exclude genuine signal along with actual
    jitter. Checking deviation from a local smoothed trend targets the
    actual problem (erratic sample-to-sample jitter) without conflating it
    with legitimate large-but-smooth amplitude.

    v_signal: the full (not pulse-sliced) corrected signal array, so the
    smoothed trend and baseline noise are computed consistently with the
    rest of the trace.
    t_ns: matching time array, for the smoothing window and baseline_mask.
    baseline_mask: boolean mask selecting the pre-pulse region, to measure
    what this shot's own correction noise floor looks like absent any real
    signal.
    """
    dt_ns = float(np.median(np.diff(t_ns[:min(2000, len(t_ns))])))
    win = max(1, int(round(smooth_ns / dt_ns)))
    trend = boxcar_smooth(v_signal, win)
    residual = v_signal - trend
    baseline_std = residual[baseline_mask].std()
    if baseline_std == 0:
        return np.zeros_like(v_signal, dtype=bool)
    return np.abs(residual) > n_sigma * baseline_std


def proton_flux_spectrum(t_pulse_ns, v_signal_pulse, energy_pulse_mev, R_load=R_LOAD,
                          unstable_mask=None):
    """dN/dE (protons/MeV landing on the detector's active area) from the
    Pockels-corrected pulse voltage and its per-sample energy axis.

    t_pulse_ns, v_signal_pulse, energy_pulse_mev: same-length arrays over
    the proton pulse window -- v_signal_pulse must already be the
    Pockels-corrected signal (baseline-subtracted), not the raw compressed
    Channel 4 reading, since only the corrected signal is linear in the
    true detector current.

    unstable_mask: same-length boolean array (from correct_pockels_signal's
    result), True where that sample sits in the ill-conditioned near-flat-top
    region of the transmission curve. There, `v_signal_pulse` is already the
    *interpolated bridge* value, not a measurement -- appropriate for timing
    (an onset crossing doesn't care about the exact interpolated shape), but
    not for flux, which needs a real amplitude at every sample. This is a
    confirmed mathematical singularity (dT/dphi -> 0 as T -> 1), not
    something a better threshold or pre-smoothing fixes -- checked directly
    this session: even smoothing the raw signal before correction left the
    peak amplitude error unchanged (~1806mV either way), because a true
    singularity amplifies *any* residual noise without bound, however small.
    So rather than compute a fabricated dN/dE there, those samples are set
    to NaN -- an honest "unknown," not a guess. Integrate with
    proton_flux_total(), which is NaN-aware and reports what fraction of
    the pulse (by energy range, not just sample count) had to be excluded.

    Uses |v_signal_pulse|, not the signed value. The Pockels correction's
    sign convention comes from which side of phi_bias the real signal
    happens to sit on -- a property of the bias point, not the physics --
    so a real pulse can legitimately come out consistently negative in
    v_signal (checked this session: ~98% of a pulse's samples share one
    sign, matching the raw signal sitting mostly above its own baseline,
    not noise scatter). A particle flux is inherently non-negative -- the
    sign carries no physical meaning here, only magnitude does. Taking the
    signed value would produce a mostly-negative "total proton count",
    which is meaningless; taking the absolute value is the correct fix, not
    a cosmetic one.

    Returns (dN_dE, order) -- order sorts by ascending energy, since TOF
    decreases as energy increases (later time = slower = lower energy).
    dN_dE is NaN wherever unstable_mask is True (if given).
    """
    current = np.abs(v_signal_pulse) / R_load
    q_of_e = charge_per_proton(energy_pulse_mev)

    dE_dt = np.gradient(energy_pulse_mev, t_pulse_ns * 1e-9)  # MeV/s
    dt_dE = 1.0 / np.abs(dE_dt)

    dN_dE = (current / q_of_e) * dt_dE
    if unstable_mask is not None:
        dN_dE = np.where(unstable_mask, np.nan, dN_dE)
    order = np.argsort(energy_pulse_mev)
    return dN_dE, order


def proton_flux_total(dN_dE, energy_pulse_mev, order):
    """Integrate dN/dE over energy, skipping NaN-flagged (unrecoverable)
    samples -- trapezoid rule applied only across the valid stretches, not a
    single naive nan-to-num that would silently treat unknown as zero.

    Returns (total_protons, frac_samples_excluded) -- the second value is
    the fraction of samples that were NaN-flagged as unrecoverable, a
    straightforward lower bound on how much of the pulse's true amplitude
    is missing from the total (straightforward on purpose: samples aren't
    evenly spaced in energy, so a fraction of the *energy span* would be
    ambiguous whenever the excluded samples fall in more than one separate
    stretch, which they typically do -- see pockels.py).
    """
    E = energy_pulse_mev[order]
    y = dN_dE[order]
    valid = ~np.isnan(y)

    if valid.sum() < 2:
        return 0.0, 1.0

    total = np.trapezoid(y[valid], E[valid])
    frac_excluded = float((~valid).mean())
    return float(total), frac_excluded
