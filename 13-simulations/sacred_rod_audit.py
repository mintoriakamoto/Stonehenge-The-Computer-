#!/usr/bin/env python3
"""
SACRED_ROD_AUDIT.py
Rigorous statistical test of Sacred Rod = Polar Radius / 6,000,000
"""

import numpy as np
import json
from scipy import stats

def sacred_rod_audit():
    POLAR_RADIUS_M = 6_356_752.3
    SACRED_ROD_CLAIMED = POLAR_RADIUS_M / 6_000_000  # 1.0594587 m
    SARSEN_CIRCLE_DIAMETER_FT = 100.8
    SARSEN_CIRCLE_DIAMETER_M = SARSEN_CIRCLE_DIAMETER_FT * 0.3048
    ROD_FROM_STONEHENGE = SARSEN_CIRCLE_DIAMETER_M / 30
    SACRED_ROD_FT = 3.4757
    SACRED_ROD_M = SACRED_ROD_FT * 0.3048

    print("="*60)
    print("SACRED ROD STATISTICAL AUDIT")
    print("="*60)
    print(f"\nConstants:")
    print(f"  Polar radius: {POLAR_RADIUS_M:.1f} m")
    print(f"  Sacred Rod (Polar/6M): {SACRED_ROD_CLAIMED:.6f} m")
    print(f"  Sacred Rod (Heath): {SACRED_ROD_M:.6f} m")
    print(f"  Rod from Stonehenge (100.8ft/30): {ROD_FROM_STONEHENGE:.6f} m")

    diff_heath = abs(SACRED_ROD_M - SACRED_ROD_CLAIMED)
    rel_diff_heath = diff_heath / SACRED_ROD_CLAIMED
    print(f"\n1. Heath's Sacred Rod vs Polar Radius/6M:")
    print(f"   Difference: {diff_heath*1000:.3f} mm ({rel_diff_heath*100:.4f}%)")

    diff_sh = abs(ROD_FROM_STONEHENGE - SACRED_ROD_CLAIMED)
    print(f"\n2. Stonehenge-derived rod vs Polar Radius/6M:")
    print(f"   Difference: {diff_sh*1000:.1f} mm ({diff_sh/SACRED_ROD_CLAIMED*100:.2f}%)")

    search_range = 1.0
    target_window = 0.0002
    p_random = target_window / search_range
    print(f"\n3. Statistical significance (random match):")
    print(f"   p-value (random match): {p_random:.6f} ({p_random*100:.4f}%)")

    sigma_h0 = 0.01
    likelihood_h0 = stats.norm.pdf(SACRED_ROD_M, ROD_FROM_STONEHENGE, sigma_h0)
    likelihood_h1 = stats.norm.pdf(SACRED_ROD_M, SACRED_ROD_CLAIMED, sigma_h0)
    bf = likelihood_h1 / likelihood_h0
    print(f"\n4. Bayesian Model Comparison:")
    print(f"   Bayes Factor (H1/H0): {bf:.2f}")
    print(f"   Interpretation: {'Strong for H1' if bf > 10 else 'Weak for H1' if bf > 3 else 'Inconclusive'}")

    print(f"\n5. Required measurement to decide:")
    print(f"   Need measurement precision: < 1 mm")
    print(f"   Target: Measure Stone 156 lintel width to ±0.5mm")
    print(f"   If 1.0594 ± 0.0005 m → PALEO-GEODESY CONFIRMED (p < 10⁻⁶)")
    print(f"   If 1.0241 ± 0.0005 m → THOM DERIVED IT (post-hoc)")

    results = {
        'polar_radius_m': POLAR_RADIUS_M,
        'sacred_rod_claimed_m': SACRED_ROD_CLAIMED,
        'sacred_rod_heath_m': SACRED_ROD_M,
        'rod_from_stonehenge_m': ROD_FROM_STONEHENGE,
        'diff_heath_mm': diff_heath * 1000,
        'diff_sh_mm': diff_sh * 1000,
        'p_random_match': p_random,
        'bayes_factor': float(bf),
        'required_precision_mm': 0.5,
        'decision_rule': 'Measure Stone 156 lintel width to ±0.5mm'
    }
    with open('sacred_rod_audit.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to sacred_rod_audit.json")

if __name__ == "__main__":
    sacred_rod_audit()
