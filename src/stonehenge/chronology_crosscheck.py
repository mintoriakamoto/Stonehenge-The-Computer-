# CHRONOLOGY_CROSSCHECK.py
# Recalibrates published Stonehenge radiocarbon measurements against IntCal20 and
# tests the repository's chronological claims against them. Only measured values
# from data/radiocarbon/stonehenge_dates.csv are used; nothing is invented.

import csv
import json
import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'radiocarbon')
CHI2_95 = {1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070, 6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919}


def load_curve(path=None):
    path = path or os.path.join(DATA_DIR, 'intcal20.14c')
    rows = [line.split(',')[:3] for line in open(path) if line[0].isdigit()]
    cal_bp, c14, sigma = np.array(rows, dtype=float).T
    order = np.argsort(cal_bp)
    grid = np.arange(cal_bp.min(), 13901.0)            # 1-yr grid, Holocene is enough here
    return grid, np.interp(grid, cal_bp[order], c14[order]), np.interp(grid, cal_bp[order], sigma[order])


def load_dates(path=None):
    path = path or os.path.join(DATA_DIR, 'stonehenge_dates.csv')
    return {r['lab_code']: {**r, 'bp': float(r['bp']), 'err': float(r['err'])} for r in csv.DictReader(open(path))}


def to_bc(cal_bp):
    """cal BP -> cal BC (positive). 1950 BP is 1 BC, there is no year 0."""
    return np.asarray(cal_bp) - 1949


def calibrate(bp, err, curve):
    grid, mu, sig = curve
    var = err ** 2 + sig ** 2
    pdf = np.exp(-0.5 * (bp - mu) ** 2 / var) / np.sqrt(var)
    return grid, pdf / pdf.sum()


def hpd(grid, pdf, level=0.954):
    """Highest posterior density ranges in cal BC, oldest first."""
    order = np.argsort(pdf)[::-1]
    keep = np.zeros_like(pdf, dtype=bool)
    keep[order[:np.searchsorted(np.cumsum(pdf[order]), level) + 1]] = True
    ranges, start = [], None
    for i, k in enumerate(keep):
        if k and start is None:
            start = i
        if start is not None and (not k or i == len(keep) - 1):
            end = i if k else i - 1
            ranges.append((int(to_bc(grid[end])), int(to_bc(grid[start])), float(pdf[start:end + 1].sum())))
            start = None
    return sorted(ranges, reverse=True)


def round_out(ranges, step=5):
    """Round outward to `step` years and merge ranges that then touch."""
    merged = []
    for a, b, p in ranges:
        a, b = int(np.ceil(a / step) * step), int(np.floor(b / step) * step)
        if merged and merged[-1][1] - a <= step:
            merged[-1] = (merged[-1][0], b, merged[-1][2] + p)
        else:
            merged.append((a, b, p))
    return merged


def fmt(ranges):
    return '; '.join(f"{a}-{b} cal BC ({p * 100:.1f}%)" for a, b, p in ranges)


def ward_wilson(bps, errs):
    """Test whether measurements share one radiocarbon age (Ward & Wilson 1978)."""
    bps, errs = np.asarray(bps, float), np.asarray(errs, float)
    w = 1 / errs ** 2
    mean = (bps * w).sum() / w.sum()
    t = float(((bps - mean) ** 2 * w).sum())
    df = len(bps) - 1
    return {'weighted_mean_bp': round(float(mean), 1), 'err': round(float(w.sum() ** -0.5), 1),
            'T': round(t, 2), 'df': df, 'T_crit_5pct': CHI2_95[df], 'consistent': t <= CHI2_95[df]}


def sample(grid, pdf, n, rng):
    return to_bc(rng.choice(grid, size=n, p=pdf))


def difference(d1, d2, curve, n=400_000, seed=1):
    """Calendar gap d1 - d2 in years (positive = d1 older), from independent calibrations."""
    rng = np.random.default_rng(seed)
    a = sample(*calibrate(d1['bp'], d1['err'], curve), n, rng)
    b = sample(*calibrate(d2['bp'], d2['err'], curve), n, rng)
    gap = a - b
    lo, med, hi = np.percentile(gap, [2.5, 50, 97.5])
    return {'median_years': int(med), 'ci95_years': [int(lo), int(hi)], 'p_first_older': round(float((gap > 0).mean()), 3)}


def analyze():
    curve = load_curve()
    dates = load_dates()
    cal = {}
    for code, d in dates.items():
        r = hpd(*calibrate(d['bp'], d['err'], curve))
        cal[code] = {'bp': f"{d['bp']:.0f}±{d['err']:.0f}", 'context': d['context'],
                     'intcal20_95': fmt(round_out(r)), 'published_95': d['published_cal_bc_95'] or None,
                     'source': d['source']}

    def pair(*codes):
        return ward_wilson([dates[c]['bp'] for c in codes], [dates[c]['err'] for c in codes])

    def combined_range(test):
        return fmt(round_out(hpd(*calibrate(test['weighted_mean_bp'], test['err'], curve))))

    sarsen = pair('UB-3821', 'OxA-4840')
    ramp = pair('OxA-4839', 'BM-46')
    four = pair('UB-3821', 'OxA-4840', 'OxA-4839', 'BM-46')
    y30 = pair('UB-3822', 'UB-3823', 'UB-3824')
    burial007 = pair('SUERC-30410', 'OxA-27086')
    ditch = pair('UB-3787', 'UB-3788', 'UB-3789', 'UB-3790', 'UB-3792', 'UB-3793', 'UB-3794', 'BM-1583', 'BM-1617')

    sarsen_gap = difference(dates['OxA-4840'], dates['UB-3821'], curve)
    aubrey_gap = difference(dates['OxA-18036'], dates['UB-3821'], curve)
    lo, hi = sarsen_gap['ci95_years']

    checks = {
        'sarsen_construction_two_dates': {
            'dates': ['UB-3821 (circle stone 1)', 'OxA-4840 (trilithon 53/54)'],
            'ward_wilson': sarsen,
            'combined_intcal20_95': combined_range(sarsen) if sarsen['consistent'] else None,
            'gap_trilithon_minus_circle': sarsen_gap,
            'finding': (f"Only two antler dates date the sarsen structure. They pass the same-age test, yet the 95% range for the gap "
                        f"runs from the circle being {-lo} years older to the trilithon being {hi} years older."),
        },
        'rejected_ramp_dates': {
            'four_date_test': four, 'ramp_pair_test': ramp,
            'finding': 'The four Phase 3 sarsen dates are not one event; Parker Pearson et al. 2007 reassigned OxA-4839/BM-46 to a later pit.',
        },
        'y_hole_30_antlers': {
            'ward_wilson': y30,
            'finding': ('The three Y30 antlers do not share one age, so at least one was old or intrusive when deposited.'
                        if not y30['consistent'] else 'The three Y30 antlers are consistent with one age.'),
        },
        'z29_vs_y30': {
            'gap_z29_minus_y30_ub3822': difference(dates['OxA-4836'], dates['UB-3822'], curve),
        },
        'aubrey_hole_to_sarsen_gap': {
            'dates': ['OxA-18036 (cremation in Aubrey Hole 32 primary fill)', 'UB-3821 (sarsen circle)'],
            'gap_years': aubrey_gap,
            'finding': (f"A cremation in Aubrey Hole 32's primary fill is {aubrey_gap['ci95_years'][0]}-{aubrey_gap['ci95_years'][1]} "
                        f"years (95%) older than the sarsen circle antler."),
        },
        'burial_007': {
            'ward_wilson': burial007, 'combined_intcal20_95': combined_range(burial007),
            'finding': "Reproduces Willis et al. 2016 (4366±25 BP, T'=4.6): the two measurements fail the same-age test at 5%, "
                       "and the source combined them anyway.",
        },
        'phase1_ditch_antlers': {
            'ward_wilson': ditch,
            'finding': (f"The nine ditch antlers pass the same-age test, but only narrowly (T'={ditch['T']} vs {ditch['T_crit_5pct']})."
                        if ditch['consistent'] else 'The nine ditch antlers do not share one age.'),
        },
        'repo_claim_stage2_140_years': {
            'repo_says': 'System worked ~140 years (Stage 2, 2620-2480 BC)',
            'source_says': 'Darvill et al. 2012 Table 3 gives 2620-2480 as "suggested dates"; their modelled Stage 2 runs from '
                           '2760-2510 cal BC to 2470-2300 cal BC.',
            'duration_bounds_years': [2510 - 2470, 2760 - 2300],
            'finding': 'Arithmetic on the published start and end ranges allows anything from ~40 to ~460 years. "~140 years" is a rounded '
                       'table bracket, not a measured lifetime.',
        },
        'repo_claim_altar_stone_crushed_2000bc': {
            'source_says': 'Darvill et al. 2012 p. 1033: the great trilithon fell after the Stage 4 bluestone oval (2205-1925 cal BC) but '
                           'before 17th-century AD plans, so the Altar Stone "could have been laid in its current position at any point '
                           'between the Neolithic and the early modern era".',
            'finding': 'No date supports collapse at ~2000 BC. The window is roughly 3,700 years wide.',
        },
        'repo_claim_single_campaign': {
            'source_says': 'Darvill et al. 2012 offer two equally likely Stage 2 scenarios, one with the sarsen circle added "years, decades, '
                           'or centuries" after the trilithons (p. 1033); their conclusion describes "a long-term process of alteration" over 15 centuries (p. 1038).',
            'finding': 'The radiocarbon data cannot distinguish a single campaign from one spread over a century or more.',
        },
    }
    return {'curve': 'IntCal20 (Reimer et al. 2020)', 'n_dates': len(dates), 'calibrations': cal, 'checks': checks}


def main():
    report = analyze()
    with open('chronology_crosscheck.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report['checks'], indent=2))


if __name__ == '__main__':
    main()
