# Evidence register

This file lists what in this repository is supported by evidence, what is computed, and what is not supported. Each section README starts with an evidence note that points here.

**Rule:** a number in this repository counts as evidence only if it is (a) found in a source that was read, or (b) reproduced by a stated calculation. Everything else is a hypothesis or an assumption, and is labelled as such.

## 1. Source-checked facts

| Fact | Source |
|---|---|
| Five stages: 3000–2620, 2620–2480, 2480–2280, 2280–2020, 2020–1520 cal BC | Darvill et al. 2012, Table 1 |
| Enclosure 110 m across; 56 Aubrey Holes "possibly to hold bluestones and/or posts" | Darvill et al. 2012 |
| SW–NE solstitial axis (midwinter sunset / midsummer sunrise), Stage 2 | Darvill et al. 2012 |
| Avenue links Stonehenge to the River Avon, 2.8 km away (Stage 3) | Darvill et al. 2012 |
| Stage 4: bluestone oval of c. 25 and outer circle of 40–60 | Darvill et al. 2012 |
| Y and Z Holes dug 1630–1520 cal BC | Darvill et al. 2012 |
| Reverberation T30 0.64 ± 0.03 s; speech gain 4.3 ± 0.9 dB; D50 mean 0.77 (~90% syllable intelligibility); 1:12 scale model | Cox et al. 2020 |
| Bluestone rearrangements made inaudible changes; sound "improbable" as a design driver | Cox et al. 2020 |
| Durrington Walls: settlement began 2535–2475 cal BC, used 0–55 years, "probably numbered several thousands"; feasts peaked in late autumn and winter | Craig et al., "Feeding Stonehenge" |
| ~90% of the animal bones are pig, ~8% cattle; over 38,000 bone fragments | English Heritage; *The Past* (Albarella & Viner-Daniels) |
| Pigs from four sites: n = 89, 8, 16, 18 (131 in total), with isotope ranges | Madgwick et al. 2019, Table 1 |
| Aubrey Hole 32 charcoal C-602: 3798 ± 275 BP (3020–1520 cal BC) | Bronk Ramsey & Bayliss, "Dating Stonehenge" |
| Quartz piezoelectric coefficients: d11 2.3 pC/N, d14 −0.7 pC/N | OSTI 1903910 |

## 2. Computed in this repository

| Result | Inputs |
|---|---|
| Lunar nodal period 18.600 yr (6,793.46 d) | Draconic month 27.212221 d, sidereal month 27.321662 d |
| 3 × 18.600 = 55.80, 0.36% from 56 | — |
| Earth's tilt (obliquity) 23.974° in 2500 BC | Laskar polynomial |
| 2500 BC midsummer sunrise at 49.1–50.1° and midwinter sunset at 229.1–230.1° | Latitude 51.179° N; horizon 0–0.6°; refraction included |
| Polar radius / 6×10⁶ = 1.0594587 m; Heath's rod 1.059393 m (0.006% apart) | WGS84 polar radius |
| Sacred-rod Bayes factor ranges from 1.28 (σ = 0.05) to 10²⁷⁰ (σ = 0.001) | `13-simulations/sacred_rod_audit.py` |
| Isotope network (Madgwick data): all six site pairs linked, betweenness zero | `13-simulations/isotope_network.py` |
| Sarsen haulage: ~1,310 t over 25 km takes 32–64 GJ of mechanical work, 146–292 GJ of food energy | Sledge friction 0.1–0.2; muscle 22% efficient |
| Raising every stone into place takes about 0.05 GJ | m·g·h |
| Hauling one 25–30 t stone needs ~50–200 people pulling | 300–500 N per person |
| Feeding 1,000–4,000 workers for one season takes 3,600–14,400 GJ | 12 MJ per person per day |
| Lockyer's 1906 inputs give a declination of 23.9084°, which with modern obliquity dates to 1851 BC (he gave 1680 BC). Shifting the azimuth by ±0.25° moves the date from 3202 BC to 686 BC | Lockyer 1906, Project Gutenberg #62342, text lines 2098–2125 |

## 3. Claims that are not supported

| Claim | Why |
|---|---|
| Stonehenge was a knowledge-transfer or neurostimulation machine | No artefact, text or measurement supports it; Cox et al. 2020 judges sound unlikely to be a design driver |
| 8.1 Hz and 114 Hz chamber modes | No measurement; the site is open to the sky; Cox et al. 2020 reports no resonances |
| Altar Stone as a piezoelectric "read head" | Bulk sandstone has near-zero net piezoelectricity; the repo's charge-to-voltage chain does not close |
| 1.7-generation knowledge half-life | A typed constant (42.5 yr), not derived from any data |
| 80:1 builder-to-initiate ratio | A typed constant; the code's own calculation gives 146.6 |
| Aubrey Holes as a 56-position counter | The holes probably held stones |
| "100% intelligibility inside vs 33% outside" | Not in Cox et al. 2020 |
| A single construction campaign | Five stages over ~1,480 years |
| Energy budget of 360,000 MJ | The repo's own formula gives 1,834,000 MJ; neither has a source |
| Neural coupling (PAC MI 0.4, HRV 0.8) | Constants in code, with `coupling_verified = True` and no computation |

## 4. Corrections made

| Error | Correction | Where |
|---|---|---|
| Nodal period 18.618 yr | 18.600 yr | code (PR #4) |
| Standstill stepping every 19 yr (Metonic) | Stepping on the 18.6-yr nodal period | code (PR #4) |
| `exp(-t/42.5)` described as a 42.5 yr half-life | `exp(-t·ln2/42.5)` | code (PR #4) |
| Sarsen ring radius 24.3 m; bluestone circle radius 15 m | 15.36 m; 11.5 m | FDTD (PR #4) |
| Altar Stone d14 1.4 pC/N | 0.7 pC/N (upper bound) | code (PR #4) |
| Pig counts 50/30/25/26 and betweenness using similarity as a distance | Madgwick Table 1; distance = 1/overlap | code (PR #2, PR #4) |
| Stage 1 2950–2900 BC | 3000–2620 cal BC | docs, code (PR #4) |
| Avenue 2.5 km | 2.8 km | docs (PR #4) |

Errors made during this review and later corrected (listed so they can be checked):
- nodal period given as 18.613 yr and 0.26%: corrected to 18.600 yr and 0.36%
- obliquity formula sign error (24.07°): corrected to 23.974°
- Avenue "corrected" to 2.5 km: corrected to 2.8 km
- 38,000 bone fragments flagged as unsourced: found in *The Past*
- sarsens described as "50 of 52": the summary gives 49 of 52 in the main group

## 5. The dead at Stonehenge

Source-checked:

| Fact | Source |
|---|---|
| Cremated remains of up to 58 individuals were excavated in 1919–26 | Snoeck et al. 2018, *Sci. Rep.* |
| At least 10 of the 25 cremated individuals analysed did not spend their lives near Stonehenge; strontium links point to west Wales | Snoeck et al. 2018 (abstract) |
| Aubrey Hole 7 reburial: minimum of 27 individuals; 9 male, 14 female, 3 undetermined; mostly adults, some aged 15–24 | Willis et al. 2016, *Antiquity* 90 |
| Adult woman beside Aubrey Hole 7: 3090–2900 cal BC (SUERC-30410, OxA-27086) | Willis et al. 2016 |
| Adult in the primary fill of Aubrey Hole 32: 3030–2880 cal BC (OxA-18036) | Willis et al. 2016, citing Parker Pearson et al. 2009 |
| Ditch dug 2990–2755 cal BC | Marshall et al. 2012, via Willis et al. 2016 |
| Cremations found in 23 of the 56 Aubrey Holes, clustered around AH14–16; only the south-east half was excavated | Willis et al. 2016 |
| Cremations were introduced when bluestones stood in the Aubrey Holes and continued until the stones were removed; one deposit (AH24) postdates removal of its stone | Willis et al. 2016 |
| Hawley (1928): burials "had apparently been brought from a distant place for interment"; his 1920 diary records discarding sieved bone | Willis et al. 2016, quoting Hawley |

Inference (judgment, not proven):
- From the start, Stonehenge was a burial monument for a selected group: 58 individuals over ~500 years is too few for a general cemetery (~85%).
- Some of the dead came with, or were brought to, stones from their homeland in west Wales (~65%).
- Individual stones marked particular groups or lineages (~35%; needs dates and isotopes hole by hole).
- The Aubrey circle was a register of stored knowledge (~5%; no evidence).

## 6. Not reached

- Marshall et al. 2012, English Heritage radiocarbon report (full lab-code table)
- Petrie 1880 full text
- Full texts of Nash et al. 2020 and Clarke et al. 2024
- Raw geophysics data (Stonehenge Hidden Landscapes Project) and the Historic England laser scan
