"""Pockels-cell readout correction: recover the true electrical pulse from
the electro-optic-modulator-encoded photodiode signal.

SLUG's detector signal doesn't reach the oscilloscope directly -- it drives a
Pockels-cell intensity modulator (Thorlabs LNX1020F) that imprints the pulse
onto a 1053nm probe laser, read out by a photodiode. This sidesteps EMP
pickup on a direct cable, at the cost of a nonlinear (cosine) transmission
curve: the recorded "Channel 4" signal is optical transmission through the
modulator, not the electrical pulse itself.

    T(t) = (1 + cos(phi(t))) / 2
    phi(t) = pi*V_bias/Vpi_bias + pi*v_signal(t)/Vpi_RF + phi0

Constants (LNX1020F):
    Vpi_bias = 6.14 V   -- bias-port half-wave voltage, direct DC power-meter
                           sweep measurement (Gsponer)
    Vpi_RF   = 4.0 V    -- RF-port half-wave voltage (the pulse itself enters
                           here, not the bias port -- datasheet typ. value,
                           independently confirmed by a separate AC S21
                           network-analyzer measurement)
    phi0     = 54.4 deg -- intrinsic phase offset at zero bias. NOT the 58.7
                           deg originally quoted from a 5-shot calibration
                           fit -- that value doesn't reproduce 3 of the 5
                           shots it was fit from. Refitting the same 5 points
                           gives 54.4 deg (3x lower error), and this is the
                           value whose implied Vpi (6.14V) matches the
                           independently measured Vpi_bias almost exactly --
                           the original 58.7 deg implies Vpi=6.72V, which
                           matches no independent measurement. A fresh
                           calculation from 6 different shots' own waveforms
                           (not part of the original calibration set) gives
                           52.2 deg, the same neighborhood. Three independent
                           checks converge on ~50-54 deg; none support 58.7.

Near the transmission curve's flat top (T close to 0 or 1), dT/dphi -> 0, so
the inversion is ill-conditioned: small noise in the measured signal becomes
a large, spurious swing in the recovered voltage. UNSTABLE_T_HIGH/LOW define
a guard band (not just the literally-invalid T>1 or T<0 samples) that gets
excluded and bridged by interpolation instead of computed directly.

Validated on shot 9 in analysis/pockels_correction.ipynb: onset-based timing
(x-ray/proton onset, TOF) is essentially unaffected by any of the choices
above, since threshold crossings happen well away from the unstable region.
Only pulse amplitude/shape depends on getting Vmax and phi0 right.
"""

import numpy as np

V_PI_BIAS_V = 6.14
V_PI_RF_V = 4.0
PHI0_DEG = 54.4

UNSTABLE_T_HIGH = 0.97
UNSTABLE_T_LOW = 0.03


def correct_pockels_signal(t, v, V_bias, V_baseline, V_pi_bias=V_PI_BIAS_V,
                            V_pi_rf=V_PI_RF_V, phi0_deg=PHI0_DEG,
                            vmax_margin=0.99):
    """Invert the Pockels-cell transmission curve to recover the true signal.

    t, v: the raw waveform (v in volts, the "calibrated diode signal" channel).
    V_bias: the shot's logged EOM bias voltage.
    V_baseline: the shot's own pre-pulse baseline level (mean of v before any
        pulse arrives) -- used with the bias-point transmission fraction to
        derive Vmax, since most shots have no independent flat-top measurement
        of their own to anchor to directly.

    phi0 doesn't perfectly predict every shot's bias-point transmission (real
    shot-to-shot scatter of a few percentage points around the fit -- see the
    module docstring). For shots where the model overestimates that
    transmission, the derived Vmax comes out too small, which then makes
    ordinary, well-below-saturation signal appear to exceed 100% transmission
    (T > 1) -- physically impossible, and a direct sign the model's Vmax was
    wrong rather than evidence of genuine saturation. Found via shots 9/11/20:
    T peaked at 113-125% using the model-derived Vmax alone, which pushed
    26-37% of the pulse into the "unstable" zone -- almost all of which was
    actually perfectly good data being misclassified, not real saturation.
    Vmax is therefore floored at whatever the observed data itself demands
    (the largest sample, divided by vmax_margin to leave a little headroom
    for noise): physically, transmission can never exceed 100%, so if the
    model's Vmax would put real signal above that, the model's Vmax -- not
    the data -- was wrong. This dropped every shot checked to under 10%
    (most under 1%) flagged unstable, versus up to 37% before the floor.

    Returns a dict with the corrected signal, the excluded/interpolated
    sample mask, and the intermediate Vmax/T_bias/phi_bias values (useful for
    diagnostics and plotting).
    """
    phi0 = np.radians(phi0_deg)
    phi_bias = np.pi * V_bias / V_pi_bias + phi0
    T_bias = (1 + np.cos(phi_bias)) / 2
    Vmax_model = V_baseline / T_bias
    Vmax_floor = np.max(np.abs(v)) / vmax_margin
    Vmax = max(Vmax_model, Vmax_floor)

    T_t = v / Vmax
    unstable = (T_t > UNSTABLE_T_HIGH) | (T_t < UNSTABLE_T_LOW)

    T_safe = np.clip(T_t, 1e-9, 1 - 1e-9)
    phi_t = np.arccos(2 * T_safe - 1)
    v_signal = (V_pi_rf / np.pi) * (phi_t - phi_bias)

    v_clean = v_signal.copy()
    if unstable.any() and (~unstable).any():
        idx = np.arange(len(v))
        v_clean[unstable] = np.interp(idx[unstable], idx[~unstable], v_signal[~unstable])

    return dict(
        v_signal=v_clean, unstable_mask=unstable,
        Vmax=float(Vmax), Vmax_model=float(Vmax_model), Vmax_floor=float(Vmax_floor),
        vmax_floor_applied=bool(Vmax_floor > Vmax_model),
        T_bias=float(T_bias), phi_bias_rad=float(phi_bias),
    )
