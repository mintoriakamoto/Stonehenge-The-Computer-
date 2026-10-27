# STRANGER_AUDIT.py
# The repository says the builders "left a crash dump for the stranger". This module is the
# stranger reading it: every numeric claim the docs make that can be recomputed is recomputed
# here, and the repo's own Strangers' Test is evaluated against published data.

import json
import numpy as np
from scipy.optimize import brentq

from stonehenge.acoustics_precision import air_absorption_db_per_m

LATITUDE = 51 + 10 / 60 + 44 / 3600          # 51°10'44"N (Wikipedia, Stonehenge)
LUNAR_INCLINATION = 5.145                     # mean inclination of lunar orbit, degrees
LUNAR_PARALLAX = 0.951                        # mean horizontal parallax, degrees
SUN_SEMIDIAMETER, MOON_SEMIDIAMETER = 0.267, 0.259


# ---------------------------------------------------------------- arithmetic and units

def arithmetic_checks():
    kcal = 4184.0                             # J per kcal
    checks = {}

    q = 500 * 1.4e-12
    checks['piezo_force_times_d'] = {
        'repo': 'V = F x d14 = 500 N x 1.4 pC/N = 0.73 mV (04_THE_MASTER_COPY)',
        'computed': f'{q:.2e} C',
        'finding': 'F x d is a charge in coulombs, not a voltage, and 500 x 1.4e-12 = 7.0e-10, not 7.3e-4. '
                   'A voltage needs a capacitance (V = Q/C), which the repo never states.',
        'verdict': 'WRONG (units and arithmetic)',
    }
    pigs = 10_000 * 100 * 20
    labour = 4000 * 2500 * kcal * 200 / 1e6
    checks['energy_budget_02'] = {
        'repo': 'Pigs 10,000 x 100 kg x 20 MJ/kg = 20,000 MJ; labour 4,000 x 2,500 kcal x 200 d = 8,400 MJ',
        'computed': {'pigs_MJ': pigs, 'labour_MJ': round(labour)},
        'factor_off': {'pigs': pigs / 20_000, 'labour': round(labour / 8_400)},
        'verdict': 'WRONG by a factor of 1000 in both lines',
    }
    labour_per_day = 200_000 / (4000 * 200)
    checks['energy_budget_reverse_doc'] = {
        'repo': 'Human labour 4,000 x 200 days = ~200,000 MJ (REVERSE_ENGINEERING_STONEHENGE.md)',
        'implied_MJ_per_person_day': labour_per_day,
        'repo_own_2500_kcal_in_MJ': round(2500 * kcal / 1e6, 2),
        'verdict': 'WRONG: implies 0.25 MJ/day, about 1/42 of the 2,500 kcal the repo assumes elsewhere. '
                   'The two docs also disagree on inputs (1,000 x 50 kg pigs vs 10,000 x 100 kg).',
    }
    checks['lintel_level_percent'] = {
        'repo': '<=3 cm over 30 m (0.01%)',
        'computed_percent': 0.03 / 30 * 100,
        'verdict': 'WRONG: 3 cm / 30 m = 0.1%',
    }
    combined = 1e-4 * 5e-3 * 3e-3
    checks['combined_anomaly_p'] = {
        'repo': '1e-4 x 5e-3 x 3e-3 -> p < 1e-10 (09_METROLOGY)',
        'computed': combined,
        'verdict': 'WRONG even on its own inputs: the product is 1.5e-9. Multiplying p-values that '
                   'were chosen after looking at the data is also not a valid test.',
    }
    checks['rate_distortion_channel'] = {
        'repo': '50 x 15,000 x 0.85 x 0.73 = 409,185 bits',
        'computed': 50 * 15_000 * 0.85 * 0.73,
        'verdict': 'WRONG: the stated factors give 465,375. 409,185 comes from different factors in knowledge_decay.py.',
    }
    nodal = 6798.38 / 365.24219
    checks['aubrey_true_cycle'] = {
        'repo': '56 / 3.049 = 18.37 -> true cycle',
        'computed': round(56 / 3.049, 4), 'true_nodal_period_years': round(nodal, 4),
        'verdict': 'WRONG: 18.37 is 0.24 yr off the real 18.613-yr nodal period',
    }
    drift = nodal - 56 / 3
    holes_per_rev = abs(drift) * 3                     # node marker moves 3 holes per year
    checks['leap_hole_rule'] = {
        'repo': 'Skip/add one hole every 6 standstills (111.7 yr)',
        'drift_per_revolution_years': round(drift, 5),
        'drift_days': round(drift * 365.24219, 1),
        'holes_slip_per_revolution': round(holes_per_rev, 4),
        'revolutions_per_hole_slip': round(1 / holes_per_rev, 3),
        'residual_after_1100_years_holes': round((1100 / (56 / 3)) * holes_per_rev - (1100 / (6 * 56 / 3)) // 1, 2),
        'verdict': 'SOUND as arithmetic: one hole slips every 6.25 revolutions, so "+1 hole per 6" keeps the '
                   'marker within half a hole for over a millennium. The repo gives the drift as +0.049 yr; it is -0.053 yr.',
    }
    checks['altar_prediction_vs_lifetime'] = {
        'repo': 'Altar Stone holds 560 remanence layers at 18.6-yr spacing; 56 TL peaks at 18.6-yr periodicity',
        'years_needed_560_layers': round(560 * 18.6),
        'years_needed_56_peaks': round(56 * 18.6),
        'repo_own_lifetimes_years': {'working_life': 140, 'stage2_to_stage5': 2620 - 1520},
        'standstills_in_140_years': round(140 / 18.6, 1),
        'verdict': 'SELF-CONTRADICTORY: 560 layers need 10,416 years and 56 peaks need 1,042 years, '
                   'but the repo says the machine ran for 140 years (7.5 standstills).',
    }
    checks['yz_59_pits'] = {
        'repo': '59 pits = 2 x 29.53 (lunar months)',
        'computed': round(2 * 29.530589, 3),
        'verdict': 'ARITHMETIC TRUE, MEANING UNSUPPORTED: Z hole 8 may lie under stone 8 (count uncertain), and any count '
                   'near 59 matches something.',
    }
    return checks


# ---------------------------------------------------------------- acoustic exclusion

def speech_at_distance(r, level_1m=60.0, f=1000.0, temp_c=3.5, rh=87.5, p_kpa=100.1):
    spreading = 20 * np.log10(r)
    air = air_absorption_db_per_m(f, temp_c, rh, p_kpa) * r
    return level_1m - spreading - air


def exclusion_check():
    lvl = speech_at_distance(2500.0)
    return {
        'repo': 'Builders at Durrington 2.5 km away excluded by a 5 dB acoustic shadow',
        'speech_60dB_at_1m_heard_at_2500m_dB_SPL': round(float(lvl), 1),
        'hearing_threshold_1kHz_dB_SPL': 0,
        'verdict': 'Distance alone puts speech about 17 dB below the threshold of hearing, before any stones. '
                   'The 5 dB "shadow" plays no role in excluding anyone 2.5 km away.',
    }


# ---------------------------------------------------------------- coding theory

def gf2_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def gf2_divmod(a, b):
    q, db = 0, b.bit_length()
    while a.bit_length() >= db:
        shift = a.bit_length() - db
        q ^= 1 << shift
        a ^= b << shift
    return q, a


def cyclic_code_min_distance(h, n=56):
    """Binary cyclic (n, deg h) code with check polynomial h: enumerate all 2^k codewords."""
    g, rem = gf2_divmod((1 << n) | 1, h)
    assert rem == 0, 'h must divide x^n + 1'
    k = h.bit_length() - 1
    return min(bin(gf2_mul(m, g)).count('1') for m in range(1, 1 << k))


def code_checks():
    g = 0b1011                                  # x^3 + x + 1
    _, rem = gf2_divmod((1 << 7) | 1, g)
    checks = {
        'repo': '(56,3) cyclic code, generator g(x) = x^3+x+1, d_min = 18, corrects 8-hole bursts, "Reed-Solomon equivalent"',
        'generator_degree_implies_k': 56 - 3,
        'x7_plus_1_divisible_by_g': rem == 0,
        'd_min_if_g_is_generator': 2,
        'd_min_if_g_is_check_polynomial': cyclic_code_min_distance(g),
        'd_min_other_k3_codes': {
            'x^3+x^2+1': cyclic_code_min_distance(0b1101),
            '(x+1)^3': cyclic_code_min_distance(0b1111),
        },
    }
    checks['verdict'] = (
        "WRONG: a degree-3 generator makes a (56,53) code, and since x^3+x+1 divides x^7+1 that code has weight-2 "
        f"codewords (d = 2). Used as a check polynomial it gives a (56,3) code with d = {checks['d_min_if_g_is_check_polynomial']}. "
        "No version has d = 18. Reed-Solomon codes need symbols from a field with more than n elements, so a "
        "binary length-56 code cannot be one. And three moving markers are not codeword symbols anyway."
    )
    return checks


# ---------------------------------------------------------------- astronomy

def obliquity_deg(year_astronomical):
    """Laskar (1986) mean obliquity; valid for +/-10,000 years around J2000."""
    U = (year_astronomical - 2000) / 10_000
    c = [84381.448, -4680.93, -1.55, 1999.25, -51.38, -249.67, -39.05, 7.12, 27.87, 5.79, 2.45]
    return sum(ci * U ** i for i, ci in enumerate(c)) / 3600


def refraction_deg(apparent_alt):
    """Bennett (1982) refraction for an apparent altitude in degrees."""
    return (1 / np.tan(np.radians(apparent_alt + 7.31 / (apparent_alt + 4.4)))) / 60


def rise_azimuth(dec, lat, horizon_alt, semidiameter, parallax=0.0, physical=True):
    """Azimuth (deg from N) at rising. physical=True: upper limb first gleam on an apparent horizon at
    horizon_alt, with refraction and parallax. physical=False: centre on a flat geometric horizon."""
    h = horizon_alt - refraction_deg(horizon_alt) - semidiameter + parallax if physical else 0.0
    phi, d, hr = np.radians(lat), np.radians(dec), np.radians(h)
    return np.degrees(np.arccos((np.sin(d) - np.sin(phi) * np.sin(hr)) / (np.cos(phi) * np.cos(hr))))


def station_angle(lat, eps, horizon_alt, physical=True):
    """Angle between midsummer sunrise and southern major-standstill moonrise directions."""
    sun = rise_azimuth(eps, lat, horizon_alt, SUN_SEMIDIAMETER, physical=physical)
    moon = rise_azimuth(-(eps + LUNAR_INCLINATION), lat, horizon_alt, MOON_SEMIDIAMETER, LUNAR_PARALLAX, physical)
    return moon - sun


def astronomy_checks(year_bc=2500):
    year = 1 - year_bc
    eps = obliquity_deg(year)
    horizons = [0.0, 0.3, 0.6, 0.9]
    sunrise = {h: round(float(rise_azimuth(eps, LATITUDE, h, SUN_SEMIDIAMETER)), 2) for h in horizons}
    # setting azimuth of declination d is 360 - rising azimuth of d
    sunset_sw = {h: round(float(360 - rise_azimuth(-eps, LATITUDE, h, SUN_SEMIDIAMETER)), 2) for h in horizons}

    def right_angle_latitude(h, physical=True):
        return round(brentq(lambda la: station_angle(la, eps, h, physical) - 90, 40, 58), 2)

    geometric_angle = float(station_angle(LATITUDE, eps, 0.0, physical=False))
    right_angle_lat = {h: right_angle_latitude(h) for h in horizons}
    dtheta_dlat = (station_angle(LATITUDE + 0.05, eps, 0.6) - station_angle(LATITUDE - 0.05, eps, 0.6)) / 0.1
    band = {tol: round(2 * tol / abs(dtheta_dlat), 2) for tol in (0.5, 1.0)}
    britain_span = 58.67 - 49.96                 # Lizard Point to Dunnet Head

    return {
        'epoch': f'{year_bc} BC', 'obliquity_deg': round(eps, 4),
        'major_standstill_moon_declination_deg': round(eps + LUNAR_INCLINATION, 3),
        'midsummer_sunrise_azimuth_by_horizon_alt': sunrise,
        'midwinter_sunset_azimuth_by_horizon_alt': sunset_sw,
        'axis_measured_lockyer_1901_deg': [49.572, 50.2],
        'station_rectangle': {
            'geometric_convention': {'angle_at_stonehenge_deg': round(geometric_angle, 2),
                                     'latitude_of_exact_right_angle': right_angle_latitude(0.0, physical=False)},
            'first_gleam_convention_angle_by_horizon_alt': {h: round(float(station_angle(LATITUDE, eps, h)), 2) for h in horizons},
            'first_gleam_latitude_of_exact_right_angle_by_horizon_alt': right_angle_lat,
            'dangle_dlat_deg_per_deg': round(float(dtheta_dlat), 3),
            'latitude_band_width_deg_for_angle_within': band,
            'band_km_for_0_5deg': round(band[0.5] * 111.2),
            'fraction_of_britain_latitudes_for_0_5deg': round(band[0.5] / britain_span, 3),
        },
        'verdict': (f"At Stonehenge the two directions meet at {geometric_angle:.1f} deg (simple geometry) to "
                    f"{station_angle(LATITUDE, eps, 0.9):.1f} deg (first gleam, refraction, parallax), not 90. An exact "
                    f"right angle falls at {min(right_angle_lat.values()):.1f}-{right_angle_latitude(0.0, physical=False):.1f} N, "
                    "south of Stonehenge. The angle changes 2.7 deg per degree of latitude, so a rectangle good to 0.5 deg "
                    f"fits a band ~{round(band[0.5] * 111.2)} km wide ({round(100 * band[0.5] / britain_span)}% of Britain's span). "
                    "That is a loose coincidence, not \"ONLY at 51.18 N +/-50 km\"."),
    }


# ---------------------------------------------------------------- look-elsewhere effect

EARTH_LENGTHS_M = {
    'polar_radius': 6_356_752.3, 'equatorial_radius': 6_378_137.0, 'mean_radius': 6_371_008.8,
    'meridian_quadrant': 10_001_965.7, 'equatorial_circumference': 40_075_016.7,
    'meridian_circumference': 40_007_862.9, 'mean_meridian_degree': 111_132.95, 'nautical_mile': 1852.0,
}


def look_elsewhere(n=200_000, rel_tol=6.2e-5, seed=7):
    """How often does a random rod length match (Earth length / round number) as well as Heath's rod?"""
    rng = np.random.default_rng(seed)
    results = {}
    for label, mantissas in (('1-9 x 10^n', range(1, 10)), ('1-99 x 10^n', range(1, 100))):
        cands = np.array(sorted({L / (m * 10.0 ** e) for L in EARTH_LENGTHS_M.values()
                                 for m in mantissas for e in range(-1, 9)
                                 if 0.5 <= L / (m * 10.0 ** e) <= 2.0}))
        rods = np.exp(rng.uniform(np.log(0.5), np.log(2.0), n))
        idx = np.clip(np.searchsorted(cands, rods), 1, len(cands) - 1)
        nearest = np.minimum(np.abs(rods - cands[idx - 1]), np.abs(rods - cands[idx])) / rods
        results[label] = {'candidate_targets': int(len(cands)), 'p_match_as_good': round(float((nearest <= rel_tol).mean()), 4)}
    return {
        'repo': 'p(random match) = 0.0002; p < 1e-4',
        'heath_relative_error': round(abs(1.059393 - 6_356_752.3 / 6e6) / 1.059393, 7),
        'random_rod_0.5_to_2m': results,
        'verdict': 'With 8 Earth lengths and round divisors, a random rod length in 0.5-2 m matches something this well '
                   'far more often than 1 in 5,000, and the rod itself (Heath) is a reconstruction, not a measurement.',
    }


# ---------------------------------------------------------------- the repo's own Strangers' Test

def strangers_test():
    """docs/BLUESTONE_REMOVAL_YZ_HOLES_ANALYSIS.md `verify_crash_report`, checked against sources."""
    rows = [
        ('y_holes_30', 'Y holes = 30', '30 (Wikipedia, Y and Z Holes)', 'PASS'),
        ('z_holes_29', 'Z holes = 29', '29 known; Z8 may lie under fallen stone 8', 'PASS (with caveat)'),
        ('y_diameter_18m', 'Y ring 18 m', 'Best-fit Y circuit ~54 m', 'FAIL'),
        ('z_diameter_22m', 'Z ring 22 m', 'Z circuit ~39 m (and Z is the inner ring)', 'FAIL'),
        ('fill_windblown', 'Windblown chalk ONLY', 'Windblown, largely stone-free fill; antlers placed at the base; later finds '
                                                   '(Iron Age to medieval pottery, coins, human remains)', 'FAIL'),
        ('no_stone_imprints', 'Never held stones', 'Darvill 2012: "cannot rule out" small standing stones', 'UNDETERMINED'),
        ('rebuild_coords_match', 'Y/Z = current sarsen upright/lintel positions', 'Sarsen circle ~30 m across; Y ~54 m, Z ~39 m', 'FAIL'),
        ('altar_buried_under_55', 'Altar Stone under fallen 55', 'Darvill 2012: great trilithon collapsed on top of it', 'PASS'),
        ('bluestones_gone', 'Bluestones = 0', '43 traceable today (Wikipedia; repo 06_MATERIALS also says 43)', 'FAIL'),
        ('knowledge_extinct', 'Oral tradition = 0', 'Not a measurable quantity', 'UNTESTABLE'),
    ]
    return {
        'repo_says': 'all(checks) -> TRUE',
        'checks': [{'check': c, 'claim': cl, 'evidence': ev, 'result': r} for c, cl, ev, r in rows],
        'tally': {r: sum(1 for *_, x in rows if x.startswith(r)) for r in ('PASS', 'FAIL', 'UNDETERMINED', 'UNTESTABLE')},
        'returns': False,
    }


def internal_contradictions():
    return [
        {'a': '01_MUSIC: adding outer bluestones +0.03 s, inner oval +0.03 s (Cox config sweep)',
         'b': 'BLUESTONE_REMOVAL: adding bluestones -0.02 to -0.03 s', 'note': 'Opposite signs for the same "Cox 2020" sweep'},
        {'a': 'Decay tables: Stage 4 (2200 BC) T30 = 0.61 s', 'b': 'Cox 2020 modelled the c. 2200 BC layout: 0.64 s',
         'note': 'The repo assigns Cox\'s value to Stage 2 and a lower invented value to the stage Cox actually modelled'},
        {'a': 'Strangers\' Test: bluestones_gone == 0 -> PASS', 'b': '06_MATERIALS: "BLUESTONES (43 SURVIVING)"', 'note': ''},
        {'a': 'Altar Stone table: sarsen quartz 99.7%, piezoelectric NONE', 'b': 'Altar Stone ~60% quartz, piezo "STRONG" via muscovite',
         'note': 'Quartz is the piezoelectric mineral; muscovite (C2/c, point group 2/m) is centrosymmetric and cannot be'},
        {'a': 'Altar Stone = horizontal "contact platform"', 'b': 'Darvill 2012: "a former standing stone lying prone"', 'note': ''},
        {'a': 'Stage 5 laborers "local only (Madgwick 2019)"', 'b': 'Madgwick 2019 analysed Late Neolithic pigs (c. 2500 BC)', 'note': 'Wrong period'},
        {'a': 'Leap-hole drift +0.049 yr', 'b': 'Code: DRIFT = 18.618 - 56/3 = -0.049', 'note': 'Sign flips between docs and code'},
        {'a': 'Avenue "cutoff" c/2W = 8.6 Hz matches 8.1 Hz mode', 'b': 'Physics', 'note': 'The fundamental mode of a duct has no cutoff; c/2W is where the first cross-mode starts. Low earth banks cannot guide a 41 m wavelength.'},
    ]


def analyze():
    return {
        'arithmetic': arithmetic_checks(),
        'acoustic_exclusion': exclusion_check(),
        'aubrey_code': code_checks(),
        'astronomy': astronomy_checks(),
        'sacred_rod_look_elsewhere': look_elsewhere(),
        'strangers_test': strangers_test(),
        'internal_contradictions': internal_contradictions(),
    }


def main():
    report = analyze()
    with open('stranger_audit.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(json.dumps({k: report[k] for k in ('aubrey_code', 'astronomy', 'sacred_rod_look_elsewhere', 'acoustic_exclusion')},
                     indent=2, default=str))
    print('Strangers\' Test tally:', report['strangers_test']['tally'])


if __name__ == '__main__':
    main()
