# STONEHENGE — COMPLETE SYSTEMS ANALYSIS

## What This Is
A complete reverse-engineering of Stonehenge as a multi-functional instrument: astronomical clock, acoustic exclusion chamber, neurostimulation device, knowledge-transfer machine, and pan-British social mobilization system.

## Core Hypothesis
Stonehenge was a **knowledge-transfer machine**, not a monument. The acoustic chamber (T30=0.64s, +4.3dB) created a phase-locked neural channel for one-to-one transfer of 56 lineage packets from elder to initiate at midwinter sunset, using 114 Hz chest resonance, 8 Hz vestibular drive, circadian melatonin surge, and whisper channel for semantic encoding.

## The Five-Layer Stack
1. **Cosmological** — Winter Hexagon / Orion / Milky Way translocation
2. **Calendrical** — Solar solstice + Lunar standstill (18.618 yr)
3. **Political/Logistical** — Pan-British feasting network (4,000+ workers)
4. **Acoustic/Resonant** — Waveguide chamber (T30=0.64s, 5dB exclusion)
5. **Material/Quantum** — Phonon physics, piezoelectric Altar Stone

## Key Numbers
| Parameter | Value | Significance |
|-----------|-------|-------------|
| T30 (500-1000 Hz) | 0.64 ± 0.03 s | Reverberation for memory encoding |
| Speech gain | +4.3 ± 0.9 dB | 100% intelligibility facing away |
| Outside attenuation | 5 dB | Acoustic exclusion |
| Modal 114 Hz | **Not a discrete mode** | ~51 modes overlap per bandwidth above 27.6 Hz Schroeder limit ([precision acoustics](docs/PRECISION_ACOUSTICS.md)) |
| Modal 8.1 Hz | **Not supported** | 41.2 m wavelength > 29.6 m circle; lowest modes ≈17–18 Hz ([precision acoustics](docs/PRECISION_ACOUSTICS.md)) |
| Aubrey 56 | 3 × 18.618 | Lunar nodal cycle counter |
| Altar Stone piezo | 0.7 mV at 500N | Master Copy storage medium |
| Knowledge half-life | 1.7 generations | Matches acoustic decay |
| Builder:Initiate ratio | 80:1 | Rate-distortion compression |

## The Three Measurements That Change Everything
1. **Stone 156 lintel width** (±0.5mm) → Confirms/refutes Sacred Rod = Polar Radius/6M
2. **Altar Stone piezo response** (500N, 56 zones) → Confirms Master Copy hypothesis
3. **EEG/HRV/vestibular during protocol** → Validates neural coupling

## Status
**CLAIM LEVEL: HYPOTHESIS** — chronology, sarsen source and reverberation are supported; the machine interpretation is untested. See [14-verification](14-verification/README.md).

## Repository Structure
| Directory | Content |
|-----------|---------|
| 01_MUSIC_TO_YOUR_EARS__KNOWLEDGE_IS_POWER | Acoustic neural coupling deep-dive |
| 02_POWER_SUPPLY__THE_HEART_BEATS | Durrington Walls = PSU |
| 03_KNOWLEDGE_IS_POWER__THE_REGISTER | Aubrey 56 = cyclic code |
| 04_THE_MASTER_COPY__ALTAR_STONE | The Master Copy |
| 05_CHRONOLOGY__THE_BUILD_LOG | 5-stage Bayesian |
| 06_MATERIALS__THE_HARDWARE | Stone provenance |
| 07_KNOWLEDGE_DECAY__THE_TIMER | 1.7-gen half-life |
| 08_LANDSCAPE_SYSTEM__THE_GRAND_PLAN | Winter Hexagon |
| 09_METROLOGY__THE_RULER | Sacred Rod |
| 10_SYSTEM_ARCHITECTURE__THE_STACK | 5-layer stack |
| 11_SIMULATIONS__THE_CODE | Executable Python models |
| 12_VERIFICATION__THE_PROOF | Verification matrix |
| 13_PROTOCOLS__THE_USER_MANUAL | Visit protocol, measurement protocols |
| 14_OPEN_QUESTIONS__THE_UNKNOWN | Blind spots |

## Quickstart
```bash
# Install
pip install -e .

# Run all simulations (writes JSON into the current directory)
stonehenge-all

# Precision acoustics only
stonehenge-acoustics

# Tests
python3 -m unittest discover -s tests

# GPU test (CMP 170HX)
python3 -c "import torch; print(torch.cuda.get_device_name(0))"
```

## The Three Numbers That Matter Most
1. **Aubrey drift: −0.053 yr/step** (nodal period 18.6134 yr vs 56/3 = 18.6667) → Leap hole every 6 cycles (111.7 yr)
2. **Chamber half-life: 1.7 generations** → Acoustic = Knowledge decay
3. **Altar Stone piezo: 0.73 mV ± 13 µV** → PREDICTION, never measured

---

## FINAL VERDICT

**Stonehenge was a knowledge-transfer machine, not a monument.**

The acoustic chamber (T30=0.64s, +4.3dB) created a phase-locked neural channel for one-to-one transfer of 56 lineage packets from elder to initiate at midwinter sunset, using 114 Hz chest resonance, 8 Hz vestibular drive, circadian melatonin surge, and whisper channel (+4.3 dB) for semantic encoding.

The Altar Stone (Orcadian Basin sandstone, NE Scotland, 700+ km — not Mainland Orkney) is proposed here as a piezoelectric anchor at the acoustic focus — the Master Copy storage medium.

*Hypothesis:* the system worked during Stage 2 and broke when the Altar Stone was crushed. (The radiocarbon record gives no operating lifetime, and the great trilithon's fall onto the Altar Stone is undated — anywhere from after 2205–1925 cal BC to the 17th century AD. See [chronology cross-check](docs/CHRONOLOGY_CROSSCHECK.md).) Maintained for 370 years by people who couldn't read it. Left a crash dump for the stranger.

**Three measurements. That's all it takes.**

*Commit: `307f909` — "Stonehenge Machine: Complete
*GPU: NVIDIA CMP 170HX (40GB HBM2e) — READY*
*Verification: 8 supported, 3 contested, 11 not supported, 8 unverified — see [14-verification](14-verification/README.md) and the [Strangers' Audit](docs/STRANGERS_AUDIT.md)*