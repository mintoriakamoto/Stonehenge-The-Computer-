# V3R1T4S VERIFICATION — THE COMPLETE MATRIX

Re-checked 2026-10-27 against primary sources and recalibrated radiocarbon. Details and quotations are in
[docs/CHRONOLOGY_CROSSCHECK.md](../docs/CHRONOLOGY_CROSSCHECK.md) and [docs/PRECISION_ACOUSTICS.md](../docs/PRECISION_ACOUSTICS.md).

**Status key**
- **SUPPORTED**: the source says it.
- **CONTESTED**: the source hedges, or it is debated in the literature.
- **NOT SUPPORTED**: the source or the data say otherwise.
- **UNVERIFIED**: not yet checked against a primary source.

## VERIFICATION MATRIX

| # | Claim | Evidence Source | Status | Note |
|---|-------|-----------------|--------|------|
| 1 | 5-stage Bayesian chronology | Darvill et al. 2012 | SUPPORTED | Modelled stages are broad. Stage 2 is 2760–2510 to 2470–2300 cal BC |
| 2 | Aubrey Holes = bluestone sockets | Parker Pearson 2009; Darvill 2012 | CONTESTED | Darvill 2012: "possibly to hold bluestones and/or posts" |
| 3 | Waun Mawn = proto-Stonehenge | Parker Pearson 2021 | CONTESTED | Disputed by Darvill 2022, *Antiquity* 96: 1515–1529 |
| 4 | Sarsens = West Woods (50/52) | Nash 2020 | SUPPORTED | Stones 26 and 160 of unknown origin |
| 5 | Quarry shutdown = Stage 1 cremation | Parker Pearson 2015/2019 | UNVERIFIED | |
| 6 | Solstitial axis (midwinter primary) | Darvill 2012 | SUPPORTED | As interpretation: "strongly suggests" |
| 7 | Station Stones = lunar standstill | Darvill 2012; Ruggles 1997 | SUPPORTED | "Aligned approximately" on major moonrise/moonset |
| 8 | Aubrey 56 = 3 × nodal cycle | Hawkins 1965; Hoyle 1977 | CONTESTED | 3 × 18.613 = 55.84. Holes are ~330–540 yr older than the sarsen circle (IntCal20) |
| 9 | Winter Hexagon translocation | Burley 2016 | UNVERIFIED | |
| 10 | T₃₀ = 0.64 s, +4.3 dB | Cox 2020 | SUPPORTED | For the c. 2200 BC (Stage 4) layout. Reproduced by Sabine theory |
| 10b | 5 dB exclusion | Cox 2020 | UNVERIFIED | Full paper not accessed |
| 11 | Peak acoustic at Stage 2/3 | Cox 2020 | NOT SUPPORTED | Cox modelled c. 2200 BC |
| 12 | 100% inside vs 33% outside | Cox §3.2 | UNVERIFIED | Full paper not accessed |
| 13 | Bluestone rearrangements inaudible | Cox 2020 | SUPPORTED | Contradicts "precision acoustic tuning" elsewhere in this repo |
| 14 | Bluestone = ringing rock | Darvill & Wainwright 2014 | UNVERIFIED | |
| 15 | Durrington = 4,000 seasonal | Parker Pearson 2019 | UNVERIFIED | |
| 16 | 114 Hz / 8.1 Hz chamber modes | — | NOT SUPPORTED | 114 Hz is in the diffuse field; 8.1 Hz is below the lowest mode. Cox measured 100–5,000 Hz |
| 17 | Altar Stone from Orkney | Clarke 2024 | NOT SUPPORTED | Orcadian Basin, NE Scotland; not Mainland Orkney (Bevins et al. 2024) |
| 18 | Sacred Rod = Polar Radius/6M | Heath/Thom | NOT SUPPORTED | Reconstructed rod, hard-coded p. A look-elsewhere test gives p = 0.004–0.04, not 0.0002 |
| 19 | Station Stones ⟂ only at 51.18°N | Ruggles 1997 | NOT SUPPORTED | Computed angle at Stonehenge 91.3–93.4°; exact 90° at 49.9–50.7°N; a 0.5° rectangle fits a ~41 km band ([audit](../docs/STRANGERS_AUDIT.md)) |
| 20 | Dolerite Q = 1000–5000 | — | UNVERIFIED | No source given |
| 21 | Erection kills ringing | Gibbons 1970 | UNVERIFIED | |
| 22 | Altar Stone crushed ~2000 BC | Darvill & Wainwright 2009 | NOT SUPPORTED | Darvill 2012 p. 1033: could have fallen any time from the Neolithic to the early modern era |
| 23 | Sarsen phase lasted ~140 years | — | NOT SUPPORTED | 2620–2480 BC dates construction (Parker Pearson 2007). Published ranges allow 40–460 yr |
| 24 | Solstitial axis matches 2500 BC sunrise/sunset | Lockyer 1901; computed | SUPPORTED | Computed 48.2–50.0° vs measured 49.6–50.2° |
| 25 | Altar Stone piezo 0.73 mV via muscovite | — | NOT SUPPORTED | Muscovite is centrosymmetric (not piezoelectric). F × d is a charge (7×10⁻¹⁰ C), not a voltage |
| 26 | Aubrey (56,3) cyclic code, d = 18 | — | NOT SUPPORTED | g = x³+x+1 gives d = 2 (as generator) or d = 32 (as check polynomial), never 18 |
| 27 | Leap-hole rule (+1 hole per 6 revolutions) | computed | SUPPORTED | As arithmetic: within 0.43 hole after 1,100 yr. Use in prehistory untested |
| 28 | Energy budget (02, REVERSE_ENGINEERING) | — | NOT SUPPORTED | Off ×1000 and ×42; the two docs contradict each other |
| 29 | Strangers' Test `verify_crash_report()` = TRUE | — | NOT SUPPORTED | 3 PASS, 5 FAIL, 1 undetermined, 1 untestable |

**Totals:** 8 SUPPORTED, 3 CONTESTED, 11 NOT SUPPORTED, 8 UNVERIFIED (30 rows).

---

## REFUTATION MATRIX (re-checked)

| Mainstream Claim | Repo's Refutation | Check |
|------------------|-------------------|-------|
| Built ad hoc over centuries | Single unified campaign (antler picks 2585–2475) | **Fails.** Darvill 2012 does not say this. The two dates cannot separate one campaign from a century-long one |
| Heel Stone local/early | Heel Stone = West Woods chemistry | **Unverified.** No source found that the Heel Stone was sampled |
| No geodetic knowledge | Sacred Rod = Polar Radius/6M | **Fails.** Circular test |
| Bluestones for healing | Ringing killed by erection | **Unverified** |
| Aubrey holes for posts/timber | 56 = 3 × 18.618; cremations in AH32 | **Contested.** Darvill 2012 keeps both bluestones and posts open |
| Lunar alignment speculative | Station Stone long sides = standstill | **Supported** (approximate alignment) |

---

## CLAIM LEVEL

**HYPOTHESIS.** The physical measurements Stonehenge is known for (chronology, sarsen source, reverberation) are supported.
The machine interpretation built on them (lineage packets, piezo storage, neural coupling, a 140-year operating life) has no direct evidence. Some parts of it are contradicted by the dates and the acoustics.

---

## SOURCES
- Darvill et al. 2012 *Antiquity* 86: 1021–1040
- Bayliss, Bronk Ramsey & McCormac 1997 *Proc. British Academy* 92: 39–59
- Parker Pearson et al. 2007 *Antiquity* 81: 617–39
- Willis et al. 2016 *Antiquity* 90: 337–356
- Reimer et al. 2020 IntCal20, *Radiocarbon* 62
- Cox, Fazenda & Greaney 2020 *J. Archaeol. Sci.* 122: 105218
- Nash et al. 2020 *Science Advances* 6: eabc0133
- Clarke et al. 2024 *Nature* — Altar Stone from the Orcadian Basin
- Bevins et al. 2024 — Altar Stone not from Mainland Orkney
- Darvill 2022 *Antiquity* 96: 1515–1529 — Waun Mawn critique
- Madgwick et al. 2019 *Science Advances* — 131 pigs, 4 sites
- Ruggles 1997 *Proc. British Academy* 92 — Station Stones
- Heath/Thom — Sacred Rod metrology (not peer-reviewed for the geodesy claim)
