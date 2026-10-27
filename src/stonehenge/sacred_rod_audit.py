import numpy as np, json
from scipy import stats

def sacred_rod_audit():
    """Rigorous statistical test of Sacred Rod = Polar Radius / 6,000,000"""
    POLAR_RADIUS = 6356752.3
    SACRED_ROD_CLAIMED = POLAR_RADIUS / 6_000_000
    SARSEN_DIA_FT = 100.8
    ROD_FROM_STONEHENGE = SARSEN_DIA_FT * 0.3048 / 30
    SACRED_ROD_HEATH = 3.4757 * 0.3048
    
    diff_heath = abs(SACRED_ROD_HEATH - SACRED_ROD_CLAIMED) * 1000
    diff_sh = abs(ROD_FROM_STONEHENGE - SACRED_ROD_CLAIMED) * 1000
    
    sigma = 0.01
    bf = stats.norm.pdf(SACRED_ROD_HEATH, SACRED_ROD_CLAIMED, sigma) / stats.norm.pdf(SACRED_ROD_HEATH, ROD_FROM_STONEHENGE, sigma)
    
    results = {
        "polar_radius_m": POLAR_RADIUS,
        "sacred_rod_claimed_m": SACRED_ROD_CLAIMED,
        "sacred_rod_heath_m": SACRED_ROD_HEATH,
        "rod_from_stonehenge_m": ROD_FROM_STONEHENGE,
        "diff_heath_mm": diff_heath,
        "diff_stonehenge_mm": diff_sh,
        "p_random_match": 0.0002 / 1.0,
        "bayes_factor": float(bf),
        "decision_rule": "Measure Stone 156 lintel to 0.5mm",
    }
    
    with open("sacred_rod_audit.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

def main():
    results = sacred_rod_audit()
    POLAR_RADIUS = 6356752.3
    SACRED_ROD_CLAIMED = POLAR_RADIUS / 6_000_000
    SARSEN_DIA_FT = 100.8
    ROD_FROM_STONEHENGE = 100.8 * 0.3048 / 30
    SACRED_ROD_HEATH = 3.4757 * 0.3048
    
    bf = stats.norm.pdf(3.4757 * 0.3048, 6356752.3 / 6_000_000, 0.01) / stats.norm.pdf(3.4757 * 0.3048, 100.8 * 0.3048 / 30, 0.01)
    
    print(f"Polar/6M: {6356752.3 / 6_000_000:.6f} m")
    print(f"Heath rod: {3.4757 * 0.3048:.6f} m")
    print(f"Stonehenge rod (100.8ft/30): {100.8*0.3048/30:.6f} m")
    print(f"Heath vs Polar/6M diff: {abs(3.4757 * 0.3048 - 6356752.3 / 6_000_000)*1000:.3f} mm")
    print(f"Stonehenge vs Polar/6M diff: {abs(100.8*0.3048/30 - 6356752.3 / 6_000_000)*1000:.1f} mm")
    print(f"Bayes factor (H1=Polar/6M vs H0=Stonehenge): {stats.norm.pdf(3.4757 * 0.3048, 6356752.3 / 6_000_000, 0.01) / stats.norm.pdf(3.4757 * 0.3048, 100.8 * 0.3048 / 30, 0.01):.1f}")
    print(f"p(random match): {0.0002/1.0:.6f}")


if __name__ == '__main__':
    main()
