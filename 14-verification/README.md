# VERIFICATION MATRIX

Every claim below has been checked against a source or recomputed, or it is marked as unchecked. Status labels:

- **SOURCE CHECKED**: read in the primary source (or an author's open copy).
- **SECONDARY**: seen only in a summary, abstract or secondary account.
- **COMPUTED**: reproduced by calculation; the inputs are stated.
- **NOT CHECKED**: no source was read for it.
- **NOT IN SOURCE**: the cited source was read and does not contain the claim.
- **CONTRADICTED**: a source that was read says otherwise.

The full source register is in [`EVIDENCE.md`](../EVIDENCE.md).

## Matrix

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | Five-stage chronology, 3000–1520 cal BC | Darvill et al. 2012, Table 1 (open author PDF) | SOURCE CHECKED |
| 1a | The model used 62 radiocarbon dates | Darvill et al. 2012 abstract, via search summary | SECONDARY |
| 2 | Aubrey Holes held bluestones | Darvill et al. 2012: "possibly to hold bluestones and/or posts"; Parker Pearson 2009: AH32 cremation in chalk packing for a standing stone | SOURCE CHECKED (probable, not certain) |
| 3 | Waun Mawn was a proto-Stonehenge | Parker Pearson 2021 (OSL), via summary; disputed | SECONDARY |
| 4 | Sarsens from West Woods | Nash et al. 2020: 49 of 52 in the main group, 3 outliers | SECONDARY |
| 5 | Quarry closure matches Stage 1 cremations | — | NOT CHECKED |
| 6 | Monument on a SW–NE solstitial axis | Darvill et al. 2012 ("midwinter sunset/midsummer sunrise") | SOURCE CHECKED |
| 6a | The axis matches the 2500 BC Sun to within ~1° | Obliquity 23.974° (Laskar); latitude 51.179° N; midsummer sunrise 49.1–50.1° | COMPUTED (axis azimuth from Lockyer 1906: 49° 34′ 18″) |
| 7 | Station Stones mark the lunar standstills | Ruggles 1997 cited; not read; contested in the literature | NOT CHECKED |
| 8 | 56 ≈ 3 × nodal cycle | 3 × 18.600 = 55.80, 0.36% from 56 | COMPUTED (arithmetic true) |
| 8a | The Aubrey Holes were used as a lunar counter | Hawkins 1965 / Hoyle; the holes probably held stones (row 2) | NOT SUPPORTED |
| 9 | Landscape plots the Winter Hexagon | Burley 2016 cited; not read | NOT CHECKED |
| 10 | T30 = 0.64 ± 0.03 s; speech gain +4.3 ± 0.9 dB (1:12 model) | Cox et al. 2020 (open access) | SOURCE CHECKED |
| 10a | A "5 dB exclusion" for listeners outside | Cox et al. 2020 | NOT IN SOURCE |
| 11 | Acoustics peaked at Stage 2/3 | Cox et al. 2020: the largest change was adding the outer sarsens; later bluestone changes were inaudible | PARTLY SUPPORTED |
| 12 | "100% intelligibility inside vs 33% outside" | Cox et al. 2020 reports ~90% syllable intelligibility (D50 mean 0.77, 28 of 29 positions) | NOT IN SOURCE |
| 12a | Sound was the design purpose | Cox et al. 2020: "improbable that sound was a primary driver in the design" | CONTRADICTED |
| 13 | Bluestone rearrangements were inaudible | Cox et al. 2020 | SOURCE CHECKED |
| 14 | Bluestones are "ringing rocks" | Darvill & Wainwright 2014 cited; not read | NOT CHECKED |
| 15 | Durrington Walls housed several thousand people | Craig et al. ("Feeding Stonehenge", open PDF): "probably numbered several thousands"; settlement used 0–55 years | SOURCE CHECKED |
| 15a | A figure of exactly 4,000 builders | — | NOT CHECKED |
| 16 | Pigs brought from across Britain, killed mostly in midwinter | Madgwick et al. 2019 Table 1; Craig et al. | SOURCE CHECKED |
| 17 | Altar Stone from the Orcadian Basin, NE Scotland | Clarke et al. 2024, via summary; mainland Orkney origin disputed | SECONDARY |
| 18 | Heath's rod (1.059393 m) is within 0.006% of polar radius / 6×10⁶ | 6,356,752.3 / 6×10⁶ = 1.0594587 m | COMPUTED (arithmetic true) |
| 18a | The match shows designed geodetic metrology | The Bayes factor runs from 1.28 to 10²⁷⁰ depending on the chosen σ; the repo's own 100.8 ft / 30 = 1.0241 m disagrees with Heath by 3.4% | NOT SUPPORTED |
| 19 | Site latitude 51.18° N | Standard | SOURCE CHECKED |
| 20 | Dolerite Q factor of 1,000–5,000 | — | NOT CHECKED |
| 21 | Erecting the bluestones stopped them ringing | Gibbons 1970 cited; not read | NOT CHECKED |

**Totals (28 rows):** 8 source-checked, 3 computed, 4 secondary, 7 not checked, 2 not in source, 1 contradicted, 2 not supported, 1 partly supported. The earlier banner "12/12 verified, zero contradictions" was not correct.

---

## Claims in the earlier "refutation matrix", rechecked

| Earlier claim | What the sources show | Status |
|---|---|---|
| Built in a single unified campaign | Darvill et al. 2012: five stages over ~1,480 years | CONTRADICTED |
| Heel Stone has West Woods chemistry | — | NOT CHECKED |
| Builders had geodetic knowledge (Sacred Rod) | Row 18a | NOT SUPPORTED |
| Peak acoustics came from stone density | Cox et al. 2020: outer sarsens dominate; bluestones inaudible | CONTRADICTED |
| Aubrey Holes encode 3 × 18.618 | Nodal period is 18.600 yr; the holes probably held stones | CONTRADICTED |
| Station Stone long sides mark the standstill | — | NOT CHECKED |

---

## Stranger test (corrected constants)

```python
def stranger_test(measurements):
    checks = {
        'aubrey_count_56': measurements['aubrey_hole_count'] == 56,
        'aubrey_near_3x_nodal': abs(56 - 3 * 18.600) < 0.25,   # 0.20 holes off: true arithmetic, not evidence of use
        'heel_on_axis': measurements['heel_on_solstice_axis'],  # Heel Stone distance (80 m in repo) is unsourced
    }
    return checks
```

---

## What the evidence supports

A Neolithic monument built in five stages from about 3000 to 1520 cal BC, aligned on the midsummer-sunrise/midwinter-sunset axis, built from local sarsens and from stones brought from Wales and NE Scotland. Several thousand people, fed by feasts with animals brought from across Britain, took part in Stage 2. The stones gave a modest acoustic effect within the circle. The neurostimulation, knowledge-transfer and geodetic-ruler claims are not supported by any source checked.

---

## Sources and access

| Source | Access | Used for |
|---|---|---|
| Darvill, Marshall, Parker Pearson & Wainwright 2012, *Antiquity* 86 | Open author PDF, Bournemouth University repository | Stages, Aubrey Holes, Avenue 2.8 km |
| Cox, Fazenda & Greaney 2020, *J. Archaeol. Sci.* 122:105218 | Open access (CC BY-NC-ND) | Acoustics |
| Craig et al., "Feeding Stonehenge" | Open author PDF, White Rose repository | Durrington population and feasting |
| Madgwick et al. 2019, *Sci. Adv.* | Open access (PMC6415963) | Pig isotopes and counts |
| Bronk Ramsey & Bayliss, "Dating Stonehenge" | Open PDF, British Academy | Early radiocarbon dates |
| Lockyer 1906 | Public domain (Project Gutenberg #62342) | Axis azimuth, history of the dating method |
| Nash et al. 2020; Clarke et al. 2024; Parker Pearson 2021 | Summaries only | Stone sources |
| Marshall et al. 2012 (English Heritage radiocarbon report) | Not reached | Full lab-code table |
