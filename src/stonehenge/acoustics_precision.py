# ACOUSTICS_PRECISION.py
# Standards-based acoustic calculations for the Late Neolithic sarsen circle,
# with Monte Carlo uncertainty on every input. Every result is reported as
# median and 95% interval; a dB figure is only as precise as its interval.

import json
import numpy as np
from scipy.special import jnp_zeros

# Inputs: ('normal', mean, sd) or ('uniform', low, high). Each carries its basis.
INPUTS = {
    'temp_c':        (('normal', 3.5, 2.5),     "Midwinter evening, Salisbury Plain (Met Office Dec means ~4 C) - ASSUMPTION"),
    'rh_pct':        (('uniform', 80.0, 95.0),  "Midwinter relative humidity - ASSUMPTION"),
    'pressure_kpa':  (('normal', 100.1, 1.5),   "~100 m altitude, synoptic spread - ASSUMPTION"),
    'radius_m':      (('normal', 14.785, 0.05), "Sarsen circle inner diameter 97.0 ft = 29.57 m (Thom)"),
    'height_m':      (('normal', 4.9, 0.3),     "Upright ~4.1 m above ground + lintel ~0.8 m"),
    'gap_width_m':   (('uniform', 0.8, 1.2),    "Gap between adjacent sarsen uprights"),
    'n_gaps':        (('uniform', 30.0, 30.0),  "30 uprights -> 30 gaps"),
    'alpha_ground':  (('uniform', 0.05, 0.30),  "Grass/chalk ground absorption, 500-1000 Hz - ASSUMPTION"),
    'alpha_stone':   (('uniform', 0.01, 0.03),  "Dressed sarsen absorption - ASSUMPTION"),
    't30_cox_s':     (('normal', 0.64, 0.03),   "Cox et al. 2020 JAS 122:105218, 1:12 model, 500-1000 Hz - PUBLISHED"),
    'gain_cox_db':   (('normal', 4.3, 0.9),     "Cox et al. 2020 speech amplification - PUBLISHED"),
}

JND_LEVEL_DB = 1.0     # just-noticeable level difference for speech-like sounds (~0.5-1 dB)
NODAL_PERIOD_DAYS = 6798.38       # lunar nodal regression period (standard lunar theory)
TROPICAL_YEAR_DAYS = 365.24219


def sample_inputs(n=200_000, seed=20200801):
    rng = np.random.default_rng(seed)
    out = {}
    for key, ((kind, a, b), _) in INPUTS.items():
        out[key] = rng.normal(a, b, n) if kind == 'normal' else rng.uniform(a, b, n)
    return out


def summarize(x, decimals=3):
    lo, med, hi = np.percentile(x, [2.5, 50, 97.5])
    return {'median': round(float(med), decimals), 'ci95': [round(float(lo), decimals), round(float(hi), decimals)]}


def speed_of_sound(temp_c):
    """Dry-air ideal-gas speed of sound, m/s (humidity adds <0.3% at these temperatures)."""
    return 331.3 * np.sqrt(1 + temp_c / 273.15)


def air_absorption_db_per_m(f, temp_c, rh_pct, pressure_kpa):
    """Pure-tone atmospheric absorption, ISO 9613-1:1993 Eq. (3)-(5)."""
    T = temp_c + 273.15
    T0, T01, pr = 293.15, 273.16, 101.325
    pa = pressure_kpa / pr
    C = -6.8346 * (T01 / T) ** 1.261 + 4.6151
    h = rh_pct * 10 ** C / pa
    fr_o = pa * (24 + 4.04e4 * h * (0.02 + h) / (0.391 + h))
    fr_n = pa * (T / T0) ** -0.5 * (9 + 280 * h * np.exp(-4.170 * ((T / T0) ** (-1 / 3) - 1)))
    return 8.686 * f ** 2 * (
        1.84e-11 / pa * (T / T0) ** 0.5
        + (T / T0) ** -2.5 * (0.01275 * np.exp(-2239.1 / T) / (fr_o + f ** 2 / fr_o)
                              + 0.1068 * np.exp(-3352.0 / T) / (fr_n + f ** 2 / fr_n)))


def chamber_geometry(s):
    R, H = s['radius_m'], s['height_m']
    volume = np.pi * R ** 2 * H
    floor = top = np.pi * R ** 2
    wall = 2 * np.pi * R * H
    gaps = s['n_gaps'] * s['gap_width_m'] * (H - 0.8)   # below the lintel ring
    return volume, floor, top, wall, gaps


def reverberation(s, f=707.0):
    """Sabine and Eyring T60 for an open-topped cylinder (sky and gaps absorb fully)."""
    V, floor, top, wall, gaps = chamber_geometry(s)
    c = speed_of_sound(s['temp_c'])
    m = air_absorption_db_per_m(f, s['temp_c'], s['rh_pct'], s['pressure_kpa']) / (10 * np.log10(np.e))
    A = top + gaps + floor * s['alpha_ground'] + (wall - gaps) * s['alpha_stone']
    S = floor + top + wall
    k = 24 * np.log(10) / c
    sabine = k * V / (A + 4 * m * V)
    eyring = k * V / (-S * np.log(1 - A / S) + 4 * m * V)
    return sabine, eyring


def schroeder_frequency(t60, volume):
    """Above this, modes overlap and no single 'resonance' can be singled out."""
    return 2000 * np.sqrt(t60 / volume)


def modal_density_per_hz(f, volume, c):
    return 4 * np.pi * volume * f ** 2 / c ** 3


def cylinder_mode(m, n, p, R, H, c):
    """Rigid floor/wall, pressure-release (open) top. n counts radial roots of J'_m, n>=1."""
    root = 0.0 if (m == 0 and n == 0) else jnp_zeros(m, n)[-1]
    k_r = root / R
    k_z = (p + 0.5) * np.pi / H
    return c / (2 * np.pi) * np.sqrt(k_r ** 2 + k_z ** 2)


def barron_gain_db(r, t60, volume):
    """Reflected-energy level gain over free field at distance r (Barron & Lee 1988 revised theory)."""
    direct = 100 / r ** 2
    reflected = 31200 * t60 / volume * np.exp(-0.04 * r / t60)
    return 10 * np.log10(1 + reflected / direct)


def analyze(n=200_000, seed=20200801):
    s = sample_inputs(n, seed)
    c = speed_of_sound(s['temp_c'])
    V = chamber_geometry(s)[0]
    sabine, eyring = reverberation(s)
    t_cox = s['t30_cox_s']
    fs = schroeder_frequency(t_cox, V)
    wavelength_8hz = c / 8.1

    # Distance between Cox's speaker and listeners is not given here; sweep the horseshoe-to-circle range.
    gains = {f'{r:.0f}m': summarize(barron_gain_db(r, t_cox, V), 2) for r in (2.0, 5.0, 10.0, 14.0)}

    absorption = {}
    for f in (8.1, 114.0, 500.0, 1000.0, 2000.0, 4000.0):
        a = air_absorption_db_per_m(f, s['temp_c'], s['rh_pct'], s['pressure_kpa'])
        across = a * 2 * s['radius_m']
        absorption[f'{f:g}Hz'] = {'db_per_km': summarize(a * 1000, 4),
                                  'db_across_circle': summarize(across, 5),
                                  'audible_vs_jnd': bool(np.percentile(across, 97.5) >= JND_LEVEL_DB)}

    R_med, H_med, c_med = (float(np.median(x)) for x in (s['radius_m'], s['height_m'], c))
    modes = {
        '(0,0,0) vertical': cylinder_mode(0, 0, 0, R_med, H_med, c_med),
        '(1,1,0)': cylinder_mode(1, 1, 0, R_med, H_med, c_med),
        '(20,20,0)': cylinder_mode(20, 20, 0, R_med, H_med, c_med),
    }
    density_114 = modal_density_per_hz(114.0, V, c)
    bandwidth_114 = 6.91 / (np.pi * t_cox)          # 3 dB modal bandwidth = 2.2/T60
    nodal_years = NODAL_PERIOD_DAYS / TROPICAL_YEAR_DAYS

    return {
        'inputs': {k: {'distribution': list(v[0]), 'basis': v[1]} for k, v in INPUTS.items()},
        'samples': n, 'seed': seed,
        'speed_of_sound_m_s': summarize(c, 3),
        'volume_m3': summarize(V, 1),
        'reverb_t60_s': {
            'sabine_model': summarize(sabine, 3),
            'eyring_model': summarize(eyring, 3),
            'cox_2020_measured': summarize(t_cox, 3),
            'cox_inside_sabine_ci95': bool(np.percentile(sabine, 2.5) <= 0.64 <= np.percentile(sabine, 97.5)),
            'note': 'Diffuse-field formulas are approximate for a roofless ring; treat as a consistency check, not a derivation.',
        },
        'schroeder_frequency_hz': summarize(fs, 2),
        'claim_114hz': {
            'modes_per_hz_at_114': summarize(density_114, 2),
            'modal_bandwidth_hz': summarize(bandwidth_114, 2),
            'overlapping_modes_in_one_bandwidth': summarize(density_114 * bandwidth_114, 1),
            'cylinder_(20,20,0)_hz': round(float(modes['(20,20,0)']), 2),
            'verdict': '114 Hz lies far above the Schroeder frequency: dozens of modes overlap, so no single 114 Hz resonance exists.',
        },
        'claim_8_1hz': {
            'wavelength_m': summarize(wavelength_8hz, 2),
            'circle_diameter_m': summarize(2 * s['radius_m'], 2),
            'cylinder_(1,1,0)_hz': round(float(modes['(1,1,0)']), 2),
            'lowest_vertical_mode_hz': round(float(modes['(0,0,0) vertical']), 2),
            'verdict': 'The 8.1 Hz wavelength exceeds the circle diameter and the lowest modes sit near 17-18 Hz; an open-topped ring cannot hold an 8 Hz mode.',
        },
        'speech_gain_db': {
            'barron_model_by_distance': gains,
            'cox_2020_measured': summarize(s['gain_cox_db'], 2),
            'jnd_db': JND_LEVEL_DB,
            'note': 'Barron theory assumes an enclosed diffuse field; Cox 4.3 dB falls between the 5 m and 10 m model values.',
        },
        'air_absorption': absorption,
        'aubrey_arithmetic': {
            'nodal_period_years': round(nodal_years, 5),
            'three_nodal_periods_years': round(3 * nodal_years, 4),
            '56_over_3_years': round(56 / 3, 5),
            'drift_per_step_years': round(nodal_years - 56 / 3, 5),
            'repo_value_18_618_error_years': round(18.618 - nodal_years, 5),
        },
    }


def main():
    report = analyze()
    with open('acoustics_precision.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(json.dumps({k: v for k, v in report.items() if k != 'inputs'}, indent=2))


if __name__ == '__main__':
    main()
