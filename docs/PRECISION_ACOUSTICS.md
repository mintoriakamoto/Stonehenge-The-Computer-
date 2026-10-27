# Precision Acoustics — Sarsen Circle

Source: `src/stonehenge/acoustics_precision.py` (run `stonehenge-acoustics`).
Output: `data/processed/acoustics_precision.json`. Tests: `tests/test_acoustics_precision.py`.

Every input carries an uncertainty, and 200,000 Monte Carlo draws (seed 20200801) push it through each calculation.
Results are given as **median [95% interval]**. A dB value is only as precise as its interval. The decimal places
show what the arithmetic resolves; whether a difference matters is judged against the ~1 dB
just-noticeable difference (JND) for speech level.

## Labels

| Label | Meaning |
|-------|---------|
| PUBLISHED | Measured value from a cited source |
| STANDARD | Computed with a published standard (ISO 9613-1) or textbook formula |
| MODEL | Computed here from assumptions; approximate |
| ASSUMPTION | Input chosen here; see `INPUTS` in the module |

## Inputs

| Input | Distribution | Basis |
|-------|--------------|-------|
| Air temperature | N(3.5, 2.5) °C | Midwinter evening — ASSUMPTION |
| Relative humidity | U(80, 95) % | ASSUMPTION |
| Pressure | N(100.1, 1.5) kPa | ~100 m altitude — ASSUMPTION |
| Circle inner radius | N(14.785, 0.05) m | Inner diameter 97.0 ft (Thom) |
| Enclosure height | N(4.9, 0.3) m | Upright + lintel |
| Gaps | 30 × U(0.8, 1.2) m | Between uprights |
| Ground absorption | U(0.05, 0.30) | ASSUMPTION |
| Stone absorption | U(0.01, 0.03) | ASSUMPTION |
| T30 | N(0.64, 0.03) s | Cox et al. 2020 — PUBLISHED |
| Speech gain | N(4.3, 0.9) dB | Cox et al. 2020 — PUBLISHED |

## Results

### Reverberation (MODEL vs PUBLISHED)

| Quantity | Value |
|----------|-------|
| Speed of sound | 333.411 [330.443, 336.357] m/s |
| Volume | 3364.5 [2958.4, 3774.8] m³ |
| Sabine T60 | 0.591 [0.511, 0.682] s |
| Eyring T60 | 0.422 [0.352, 0.506] s |
| Cox 2020 T30 | 0.640 [0.581, 0.699] s |

Cox's 0.64 s lies **inside** the Sabine interval. With the sky and the gaps treated as open (fully absorbing), simple
room acoustics reproduces the measured reverberation. Nothing special is needed to explain it.

### The 114 Hz claim — refuted

| Quantity | Value |
|----------|-------|
| Schroeder frequency | 27.58 [25.59, 29.81] Hz |
| Modal density at 114 Hz | 14.83 [13.00, 16.69] modes/Hz |
| Modal bandwidth (2.2/T60) | 3.44 [3.15, 3.78] Hz |
| Modes overlapping in one bandwidth | 51.0 [43.5, 59.3] |
| Cylinder (20,20,0) mode | 322.2 Hz (not 114 Hz) |

Above the Schroeder frequency, modes overlap and the response is diffuse. At 114 Hz about 51 modes sit inside
each modal bandwidth, so no individual "114 Hz chest resonance" can stand out. The repo's "(20,20) mode = 114 Hz"
label is also wrong: (20,20,0) is 322 Hz.

### The 8.1 Hz claim — refuted

| Quantity | Value |
|----------|-------|
| Wavelength at 8.1 Hz | 41.16 [40.80, 41.53] m |
| Circle diameter | 29.57 [29.37, 29.77] m |
| Cylinder (1,1,0) mode | 18.25 Hz |
| Lowest vertical (quarter-wave) mode | 17.01 Hz |

The 8.1 Hz wavelength is longer than the structure. Its lowest modes sit near 17–18 Hz, and an open top lets
low-frequency energy escape anyway.

### Speech gain (MODEL vs PUBLISHED)

Barron & Lee (1988) revised theory, level over free field:

| Distance | Gain |
|----------|------|
| 2 m | 0.83 [0.71, 0.96] dB |
| 5 m | 3.19 [2.82, 3.59] dB |
| 10 m | 6.21 [5.58, 6.85] dB |
| 14 m | 7.67 [6.91, 8.42] dB |
| Cox 2020 measured | 4.30 [2.54, 6.06] dB |

Cox's +4.3 dB falls between the 5 m and 10 m model values. That is consistent with ordinary reflections from the
stones. Barron's theory assumes an enclosed hall, so read this as a consistency check only.

### Air absorption (STANDARD — ISO 9613-1)

| Frequency | dB/km | dB across the circle (29.6 m) | ≥ 1 dB JND? |
|-----------|-------|-------------------------------|-------------|
| 8.1 Hz | 0.0022 [0.0018, 0.0027] | 0.00006 [0.00005, 0.00008] | No |
| 114 Hz | 0.3234 [0.3015, 0.3386] | 0.00956 [0.00891, 0.01002] | No |
| 500 Hz | 1.5552 [1.4327, 1.8630] | 0.04598 [0.04235, 0.05509] | No |
| 1000 Hz | 3.4284 [3.2600, 4.0422] | 0.10137 [0.09634, 0.11949] | No |
| 2000 Hz | 10.3446 [8.4564, 13.9122] | 0.30592 [0.25008, 0.41119] | No |
| 4000 Hz | 36.8612 [28.0779, 49.1697] | 1.09003 [0.83016, 1.45341] | Borderline |

Inside the circle, air absorption is inaudible below 4 kHz. The implementation matches the ISO reference values to
within 1% (4.98 dB/km at 1 kHz, 20 °C, 70% RH).

### Aubrey arithmetic

| Quantity | Value |
|----------|-------|
| Lunar nodal period (6798.38 d) | 18.61335 tropical years |
| 3 × nodal period | 55.84 years |
| 56 / 3 | 18.66667 years |
| Drift per 3-hole step | −0.05332 years (repo said +0.049) |
| Error in repo constant 18.618 | +0.00465 years |

## What this changes

- **Supported:** T30 ≈ 0.64 s and a speech gain of about +4 dB. Both are reproduced by standard theory.
- **Refuted:** discrete 114 Hz and 8.1 Hz resonances.
- **Untested:** every neural-coupling claim that depends on those two frequencies now has no acoustic basis.
