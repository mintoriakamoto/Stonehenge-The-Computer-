# The Strangers' Audit

The repository says the builders "left a crash dump for the stranger". We are the strangers. This audit reads the dump:
every numeric claim in the docs that can be recomputed is recomputed, and the repo's own `verify_crash_report()`
Strangers' Test is run against published data instead of being marked PASS by hand.

Source: `src/stonehenge/stranger_audit.py` (run `stonehenge-stranger`). Output: `data/processed/stranger_audit.json`.
Tests: `tests/test_stranger_audit.py`. Companion audits: [chronology](CHRONOLOGY_CROSSCHECK.md), [acoustics](PRECISION_ACOUSTICS.md).

## 1. The Strangers' Test, run for real

From `docs/BLUESTONE_REMOVAL_YZ_HOLES_ANALYSIS.md`, where every check was marked `# PASS` and the function was said to return `TRUE`.

| Check | Repo's claim | Evidence | Result |
|---|---|---|---|
| `y_holes_30` | 30 Y holes | 30 (Wikipedia, *Y and Z Holes*) | PASS |
| `z_holes_29` | 29 Z holes | 29 known; Z8 may lie under fallen stone 8 | PASS (caveat) |
| `y_diameter_18m` | Y ring 18 m | Best-fit Y circuit **~54 m** | **FAIL** |
| `z_diameter_22m` | Z ring 22 m | Z circuit **~39 m**, and Z is the *inner* ring | **FAIL** |
| `fill_windblown` | Windblown chalk ONLY | Windblown, largely stone-free fill, but **antlers were placed at the base** (the dated ones), plus later pottery, coins and human remains | **FAIL** |
| `no_stone_imprints` | Never held stones | Darvill 2012: "cannot rule out" small standing stones | UNDETERMINED |
| `rebuild_coords_match` | Y/Z = sarsen upright and lintel positions | Sarsen circle ~30 m across vs Y ~54 m and Z ~39 m | **FAIL** |
| `altar_buried_under_55` | Altar Stone under fallen 55 | Darvill 2012: the great trilithon collapsed on top of it | PASS |
| `bluestones_gone` | 0 bluestones | **43** traceable today, and the repo's own `06_MATERIALS` says 43 | **FAIL** |
| `knowledge_extinct` | Oral tradition = 0 | Not measurable | UNTESTABLE |

**Result: 3 PASS, 5 FAIL, 1 UNDETERMINED, 1 UNTESTABLE. `verify_crash_report()` returns `False`.**

## 2. Arithmetic and units

| Claim (where) | Recomputed | Verdict |
|---|---|---|
| V = F × d₁₄ = 500 N × 1.4 pC/N = **0.73 mV** (04) | 500 × 1.4×10⁻¹² = **7.0×10⁻¹⁰ C** | Wrong. F × d is a *charge*, not a voltage, and the digits don't match either |
| Pigs 10,000 × 100 kg × 20 MJ/kg = **20,000 MJ** (02) | **20,000,000 MJ** | Wrong ×1000 |
| Labour 4,000 × 2,500 kcal × 200 d = **8,400 MJ** (02) | **8,368,000 MJ** | Wrong ×1000 |
| Labour 4,000 × 200 d ≈ **200,000 MJ** (REVERSE_ENGINEERING) | Implies **0.25 MJ/person-day**; 2,500 kcal is 10.46 MJ | Wrong ×42. The two docs also use different herds (1,000 × 50 kg vs 10,000 × 100 kg) |
| Lintel level ≤ 3 cm / 30 m = **0.01%** | **0.1%** | Wrong ×10 |
| Combined p = 10⁻⁴ × 5×10⁻³ × 3×10⁻³ → **p < 10⁻¹⁰** (09) | **1.5×10⁻⁹** | Wrong on its own inputs, and post-hoc p-values can't be multiplied |
| Channel 50 × 15,000 × 0.85 × 0.73 = **409,185** bits | **465,375** | Wrong. 409,185 comes from other factors in the code |
| 56 / 3.049 = **18.37** = "true cycle" (03) | 18.367 vs real nodal period **18.613** yr | Wrong by 0.25 yr |
| Altar Stone: **560** magnetic layers at 18.6 yr; **56** TL peaks at 18.6 yr | Needs **10,416** yr and **1,042** yr | Contradicts the repo's own 140-yr working life (7.5 standstills) |
| 59 Y+Z pits = 2 × 29.53 lunar months | 59.06 | Arithmetic true. Z count is uncertain; numerology |

### One thing the repo got right

**The leap-hole rule works.** Moving a node marker 3 holes a year, it slips 0.160 hole per revolution (drift **−0.0533 yr = −19.5 days**, not +0.049). That is one hole every 6.25 revolutions, so "+1 hole every 6" keeps the marker within **0.43 hole after 1,100 years**. As a counting scheme it is sound. Whether anyone used it is a separate, untested question.

## 3. The "(56,3) cyclic code"

The repo claims generator g(x) = x³+x+1, d_min = 18, corrects 8-hole bursts, "Reed-Solomon equivalent". Every distance below comes from enumerating all codewords over GF(2).

| Reading | Code | d_min |
|---|---|---|
| g(x) = x³+x+1 as **generator** (what the repo says) | (56,53) | **2**, because x³+x+1 divides x⁷+1, so a weight-2 codeword exists |
| x³+x+1 as **check** polynomial | (56,3) | **32** |
| x³+x²+1 as check polynomial | (56,3) | 32 |
| (x+1)³ as check polynomial | (56,3) | 28 |

None of these gives 18. A Reed-Solomon code needs symbols from a field larger than its length, so a binary length-56 code is not RS. And the Sun/Moon/Node markers are counters moving around a ring, not data symbols of a codeword. **Verdict: the coding-theory description is wrong.**

## 4. Physics

- **Piezoelectricity.**
  - Muscovite is space group C2/c (point group 2/m). That group is centrosymmetric, so muscovite **cannot be piezoelectric**.
  - Quartz is piezoelectric, and the sarsens are **99.7 wt% SiO₂** (Nash et al. 2021, PLoS ONE). The repo's table says sarsen piezo = NONE and Altar Stone (muscovite) = STRONG, which is backwards.
  - d₁₄ is a shear coefficient, so a normal palm press does not drive it.
  - In a sandstone, randomly oriented grains largely cancel each other's response.
- **Acoustic exclusion of builders at 2.5 km.**
  - Speech at 60 dB (1 m) arrives at 2,500 m at **−16.5 dB SPL** (inverse-square law plus ISO 9613-1 air absorption, midwinter conditions).
  - That is far below the 0 dB threshold of hearing. Distance alone excludes them; the "5 dB shadow" does nothing.
- **Avenue "cutoff" c/2W = 8.6 Hz matches the 8.1 Hz mode.**
  - In a duct, c/2W is where the *first cross-mode* begins. The fundamental mode propagates at every frequency, so there is no low-frequency cutoff to "match".
  - Low earth banks cannot guide a 41 m wavelength.
  - At 3.5 °C, c = 333 m/s, not 343 m/s.

## 5. Astronomy (2500 BC, latitude 51.1789° N)

- **Inputs.**
  - Obliquity is **23.974°** (Laskar 1986), so the major-standstill lunar declination is **29.119°**.
  - Refraction uses Bennett (1982). Azimuths are for first gleam, at horizon altitudes 0–0.9°, which are not measured here.

| Quantity | Computed | Comparison |
|---|---|---|
| Midsummer sunrise azimuth | **48.2–50.0°** | Measured axis 49°34′–50°12′ (Lockyer 1901): **consistent** for a horizon of 0.6–0.9° |
| Midwinter sunset azimuth | **229.3–231.0°** | Same axis reversed: **consistent** |
| Station rectangle angle at Stonehenge (sunrise ⟂ southern major moonrise?) | **91.3°** (simple geometry) to **93.4°** (first gleam, refraction, parallax) | Not 90° |
| Latitude of an exact right angle | **49.9–50.7° N** | South of Stonehenge, not "ONLY at 51.18° N" |
| Sensitivity | 2.7° of angle per 1° of latitude | A 0.5°-accurate rectangle fits a **~41 km** band, about 4% of Britain's span |

**Verdict.**
- The solstitial axis matches the computed sunrise and sunset within the measured range, so it is **supported**.
- The Station Stone right angle is a loose geometric coincidence, and it is sensitive to conventions. It is **not** a latitude lock with p ≈ 0.5%.

## 6. Sacred Rod: the look-elsewhere test

- **Repo's claim:** p(random match) = 0.0002.
- **Setup:** draw random rod lengths (log-uniform, 0.5–2 m). Count how often one matches *any* of 8 Earth lengths divided by a round number, to Heath's 0.0062% accuracy. The 8 lengths are the polar, equatorial and mean radii, the meridian quadrant, the two circumferences, a meridian degree and the nautical mile.

| Round divisors allowed | Targets in 0.5–2 m | p(match this good) |
|---|---|---|
| 1–9 × 10ⁿ | 48 | **0.0042** (21× the repo's figure) |
| 1–99 × 10ⁿ | 485 | **0.040** (200× the repo's figure) |

The rod (3.4757 ft) is Heath's reconstruction, not a measured stone, and it was compared with the target after both were chosen. **Verdict: not anomalous.**

## 7. Contradictions inside the repo

| One doc says | Another says |
|---|---|
| Cox sweep: adding bluestones **+0.03 s** (01_MUSIC) | Adding bluestones **−0.02 to −0.03 s** (BLUESTONE_REMOVAL) |
| Stage 4 (2200 BC) T30 = **0.61 s** | Cox 2020 modelled the **c. 2200 BC** layout: **0.64 s** |
| `bluestones_gone == 0` | "BLUESTONES (43 SURVIVING)" |
| Sarsen piezo NONE (99.7% quartz) | Altar Stone piezo STRONG (muscovite) |
| Altar Stone = horizontal contact platform | Darvill 2012: "a former standing stone lying prone" |
| Stage 5 labour "local only (Madgwick 2019)" | Madgwick 2019 analysed Late Neolithic pigs (c. 2500 BC) |
| Drift +0.049 yr (docs) | `DRIFT = 18.618 − 56/3 = −0.049` (code) |

## Bottom line for the stranger

- **Real and checkable:**
  - The solstitial axis.
  - The 30 Y holes and 29 Z holes.
  - The Altar Stone lying under the great trilithon.
  - Cox's reverberation figures.
  - A sound leap-hole counting rule.
- **What fails on its own math:** the "machine" layer. That covers the piezo read head, the error-correcting code, the energy budget, the latitude lock, the geodetic rod and the crash-report geometry.

## Sources

- Wikipedia, *Stonehenge* (coordinates 51°10′44″N; 43 bluestones) and *Y and Z Holes* (counts, ~54 m / ~39 m circuits, fills, finds)
- Darvill et al. 2012, *Antiquity* 86: 1021–1040
- Nash et al. 2021, *PLoS ONE* — Stone 58 core, 99.7 wt% SiO₂
- *Nature* 65: 128 (1901) — Lockyer's axis 49°34′18″, alternative 50°12′
- Muscovite C2/c (*Handbook of Mineralogy*, Wikipedia); centrosymmetry tested by second-harmonic generation in *American Mineralogist* 64: 1052 (1979)
- Laskar 1986 (obliquity); Bennett 1982 (refraction); ISO 9613-1:1993 (air absorption)
