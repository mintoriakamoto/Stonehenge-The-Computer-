# Chronology Cross-check — Radiocarbon vs the Repository's Claims

Source: `src/stonehenge/chronology_crosscheck.py` (run `stonehenge-chronology`).
Data: `data/radiocarbon/stonehenge_dates.csv` (49 measurements) and `data/radiocarbon/intcal20.14c`; provenance is in `data/radiocarbon/SOURCES.md`.
Output: `data/processed/chronology_crosscheck.json`. Tests: `tests/test_chronology_crosscheck.py`.

## Method

- **Data.** Every radiocarbon age was transcribed from a primary source. Bayliss et al. 1997 Table 1 was checked against rendered page images, Willis et al. 2016 Table 2 against the journal PDF text. No value was estimated.
- **Calibration.** Each age is calibrated against IntCal20 on a 1-year grid. Ranges are 95.4% highest-density ranges, rounded outward to 5 years. Year convention: 1950 BP = 1 BC.
- **Same-age test.** Ward & Wilson (1978) T′ against χ² at 5%.
- **Calendar gaps.** 400,000 paired draws from two independent calibrations. No stratigraphic ordering is imposed, so these are wider than a full Bayesian model would give.
- **Validation.**
  - Combining SUERC-30410 and OxA-27086 gives 4365.5±24.0 BP with T′ = 4.58. Willis et al. 2016 publish 4366±25 BP with T′ = 4.6.
  - Across all 47 published ranges, 32 agree with IntCal20 to within 25 years at both ends. The other bounds moved because the curve was revised (see the last section).

## What the dates say about the repository's claims

| Repo claim | Evidence | Verdict |
|---|---|---|
| "System worked ~140 years (Stage 2, 2620–2480 BC)" | 2620–2480 BC first appears in Parker Pearson et al. 2007 as the date of the sarsen **construction** phase (abstract: "re-dating of this important phase (Phase 3ii) to 2620-2480 BC"). It is not an operating period. Darvill et al. 2012 reuse it as *suggested* dates (Table 3). Their *modelled* Stage 2 runs from 2760–2510 to 2470–2300 cal BC. Simple arithmetic on those ranges allows **40 to 460 years**. | **Not supported.** 140 years is a rounded table bracket, not a measured lifetime |
| "Single unified campaign (antler picks 2585–2475)" — attributed to Darvill 2012 | Two antler dates (UB-3821, OxA-4840) pass the same-age test (T′ = 0.59 < 3.84). The 95% range for their calendar gap, however, runs from the **circle 197 years older to the trilithon 106 years older**. Darvill et al. give two equally likely scenarios, one with the circle added "years, decades, or centuries" later (p. 1033). Their conclusion calls it "a long-term process of alteration" (p. 1038). | **Misattributed.** The data cannot tell one campaign from a century-long one |
| Sarsen structure date | Only **two** dates are accepted. With all four Phase 3 sarsen dates, T′ = 17.44 > 7.81, so they cannot be one event. Parker Pearson et al. 2007 moved OxA-4839 and BM-46 to a later pit. | Combined IntCal20 range: **2575–2470 cal BC**, resting on n = 2 |
| "Trilithon collapse (~2000 BC) displaced the Altar Stone; broke when the hard drive was crushed" | Darvill et al. 2012 p. 1033: the great trilithon fell after the Stage 4 bluestone oval (2205–1925 cal BC) but before the 17th-century AD plans, so the Altar Stone "could have been laid in its current position at any point between the Neolithic and the early modern era". | **No evidence.** The window is about 3,700 years wide |
| Aubrey 56 as a lunar register running from 2620 BC | A cremation in Aubrey Hole 32's primary fill (OxA-18036) is **328–543 years older** (95%) than the sarsen circle antler. Darvill et al. 2012 suggest stones in the Aubrey holes may have been *moved into the centre* in Stage 2. | **Contradicted on timing.** The holes predate the "machine" by about four centuries and may have been emptied when it was built |
| Aubrey Holes = bluestone sockets (VERIFIED) | Darvill et al. 2012 Table 3: "possibly to hold bluestones and/or posts". | **Contested**, not verified |
| Y/Z holes = "crash report" at 1630 BC | The three Y Hole 30 antlers fail the same-age test (T′ = 24.07 > 5.99), so at least one was old or intrusive. The single Z Hole 29 antler is 98–425 years older than UB-3822. | Y/Z timing rests on **mutually inconsistent** antlers. The "crash report" is interpretation |

## Literature cross-checks (beyond radiocarbon)

| Repo claim | What the source says | Verdict |
|---|---|---|
| Altar Stone = **Orkney** (Clarke et al. 2024 Nature) | Clarke et al. 2024 match it to the **Orcadian Basin**, NE Scotland. Bevins et al. 2024 (*J. Archaeol. Sci.*) found its mineralogy (little K-feldspar, the clay mineral tosudite present) differs from Mainland Orkney samples, so it was "not sourced from Mainland Orkney". | **Wrong as stated.** Use "Orcadian Basin, NE Scotland" |
| Waun Mawn = proto-Stonehenge (VERIFIED) | Parker Pearson et al. 2021 propose it. Darvill 2022 (*Antiquity* 96: 1515–1529) argues for smaller, separate stone settings, and Parker Pearson et al. replied. | **Disputed** in the literature |
| T30 = 0.64 s, +4.3 dB (Cox 2020) as a **Stage 2** machine | Cox et al. 2020 modelled the monument **c. 2200 BC (157 stones, Stage 4)** and measured 100–5,000 Hz. They found bluestone rearrangements caused inaudible changes, so sound is unlikely to have motivated the layouts. | The numbers are correct. They describe Stage 4, not Stage 2. **8 Hz was never measured.** The repo's "bluestones = precision tuning" contradicts the source |
| "Peak acoustic at Stage 2/3" (VERIFIED) | Cox modelled a single configuration (c. 2200 BC) in the summary I could access. | **Unverified.** I could not access the full paper to check the repo's configuration table (0.30/0.50/0.55/0.58/0.61 s) |
| 50/52 sarsens from West Woods (Nash 2020) | Confirmed. Stones 26 and 160 are of unknown origin. | **Supported** |
| "Heel Stone = West Woods chemistry" | No source I found says the Heel Stone was sampled. | **Unverified** |

## Large curve revisions (IntCal20 vs published)

These are not errors in the sources: the calibration curve was revised after they were published. They matter where the repo leans on a single date.

| Lab code | Context | Published 95% | IntCal20 95% | Shift |
|---|---|---|---|---|
| **OxA-4840** | Trilithon 53/54 (the only trilithon date) | 2850–2400 | **2625–2345** | Old bound 225 years younger |
| C-602 | Aubrey Hole 32 charcoal (±275) | 3020–1520 | 2920–1505 | Old bound 100 years younger |
| OxA-26962 | AH7 cremation | 2920–2870 | 3010–2780 | Small tails added at both ends |
| OxA-27078 | AH7 cremation | 2920–2790 | 2920–2700 | Young bound 90 years younger |
| OxA-4884 | Avenue, Stonehenge terminal | 2580–2300 | 2575–2235 | Young bound 65 years younger |
| UB-3823 | Y Hole 30 | 1675–1520 | 1615–1515 | Old bound 60 years younger |

## Not verified here

These remain unchecked against a primary source in this pass:
- Durrington Walls at 4,000 people
- The Carn Goedog quarry dates and "shutdown"
- Station Stones at 51.18°N
- Dolerite Q values and "erection kills ringing"
- Cox's 100%/33% intelligibility and 5 dB exclusion figures
- The Winter Hexagon

They should be treated as **UNVERIFIED** until checked.

## Sources

- Bayliss, Bronk Ramsey & McCormac 1997. Dating Stonehenge. *Proc. British Academy* 92: 39–59 — https://www.thebritishacademy.ac.uk/documents/3914/92p039.pdf
- Darvill, Marshall, Parker Pearson & Wainwright 2012. Stonehenge remodelled. *Antiquity* 86: 1021–1040 — https://doi.org/10.1017/S0003598X00048225
- Parker Pearson et al. 2007. The age of Stonehenge. *Antiquity* 81: 617–639 — https://nora.nerc.ac.uk/id/eprint/9174/
- Willis et al. 2016. The dead of Stonehenge. *Antiquity* 90: 337–356 — https://discovery.ucl.ac.uk/1474049/
- Reimer et al. 2020. IntCal20. *Radiocarbon* 62 — https://doi.org/10.1017/RDC.2020.41
- Cox, Fazenda & Greaney 2020. *J. Archaeol. Sci.* 122: 105218; summary in *Physics Today* — https://physicstoday.aip.org/quick-study/modeling-sound-at-stonehenge
- Nash et al. 2020. *Science Advances* 6: eabc0133 — https://www.ucl.ac.uk/news/2020/jul/new-research-reveals-origin-stonehenges-great-sarsen-stones
- Clarke et al. 2024 *Nature* (Altar Stone, Orcadian Basin) — https://www.sciencenews.org/article/stonehenge-altar-stone-scotland-roots
- Bevins et al. 2024. Was the Stonehenge Altar Stone from Orkney? — https://www.aber.ac.uk/en/news/archive/2024/09/title-275266-en.html
- Darvill 2022. Mythical rings? Waun Mawn and Stonehenge Stage 1. *Antiquity* 96: 1515–1529 — https://eprints.bournemouth.ac.uk/37757/
