#!/usr/bin/env python3
"""
COMPLETE_SIMULATION.py
1500-year full system trajectory with all domains integrated.
"""

import numpy as np
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any

@dataclass
class TrajectoryPoint:
    year_bc: int
    stage: int
    chamber_t30: float
    engineering_fidelity: float
    astronomy_fidelity: float
    genealogy_fidelity: float
    motor_fidelity: float
    acoustic_energy: float
    knowledge_bits: float
    initiate_pool: int
    bluestone_count: int
    altar_stone_aligned: bool
    trilithon_intact: bool

class CompleteSimulation:
    def __init__(self):
        self.results: List[TrajectoryPoint] = []
        
    def stage_from_year(self, year_bc: int) -> int:
        if year_bc >= 2620: return 2
        elif year_bc >= 2480: return 3
        elif year_bc >= 2280: return 4
        elif year_bc >= 2020: return 5
        else: return 5
    
    def chamber_t30(self, year_bc: int) -> float:
        stage = self.stage_from_year(year_bc)
        # Cox 2020 config sweep + degradation
        base_t30 = {2: 0.64, 3: 0.62, 4: 0.61, 5: 0.61}
        # Bluestone fragmentation after 2000 BC
        if year_bc < 2000:
            frag_factor = max(0.0, (year_bc - 1520) / (2000 - 1520))
            return base_t30[stage] * frag_factor + 0.15 * (1 - frag_factor)
        return base_t30[stage]
    
    def knowledge_fidelities(self, year_bc: int) -> Dict[str, float]:
        # Half-lives from knowledge_decay.py
        half_lives = {
            'engineering': 350,
            'astronomy': 50,
            'genealogy': 75,
            'motor': 575
        }
        t = 2620 - year_bc
        chamber = self.chamber_t30(year_bc)
        # Chamber fidelity modulates transfer
        fidelities = {}
        for domain, hl in half_lives.items():
            substrate_decay = np.exp(-t / hl)
            chamber_mod = chamber / 0.64  # normalized to peak
            fidelities[domain] = substrate_decay * chamber_mod
        return fidelities
    
    def initiate_pool(self, year_bc: int) -> int:
        # 1.7-gen half-life = 42.5 yr
        # Start: ~50 initiates at peak
        t = 2620 - year_bc
        pool = 50 * np.exp(-t * np.log(2) / 42.5)
        return max(0, int(pool))
    
    def bluestone_count(self, year_bc: int) -> int:
        stage = self.stage_from_year(year_bc)
        counts = {2: 80, 3: 25, 4: 69, 5: 69}
        base = counts.get(stage, 0)
        if year_bc < 2000:
            frag = max(0.0, (year_bc - 1520) / (2000 - 1520))
            return int(base * frag)
        return base
    
    def altar_aligned(self, year_bc: int) -> bool:
        return year_bc > 2000  # Trilithon falls ~2000 BC
    
    def trilithon_intact(self, year_bc: int) -> bool:
        return year_bc > 2000
    
    def acoustic_energy(self, year_bc: int) -> float:
        # Proportional to T30 * stone_count
        return self.chamber_t30(year_bc) * self.bluestone_count(year_bc)
    
    def total_knowledge_bits(self, year_bc: int) -> float:
        fids = self.knowledge_fidelities(year_bc)
        initial = {'engineering': 5000, 'astronomy': 2000, 
                   'genealogy': 3000, 'motor': 4000}
        return sum(fids[d] * initial[d] for d in fids) * 50  # 50 initiates
    
    def simulate(self, start_year: int = 3000, end_year: int = 1520):
        print(f"Simulating complete trajectory: {start_year} BC to {end_year} BC")
        for year in range(start_year, end_year - 1, -1):
            stage = self.stage_from_year(year)
            t30 = self.chamber_t30(year)
            fids = self.knowledge_fidelities(year)
            tp = TrajectoryPoint(
                year_bc=year,
                stage=stage,
                chamber_t30=t30,
                engineering_fidelity=fids['engineering'],
                astronomy_fidelity=fids['astronomy'],
                genealogy_fidelity=fids['genealogy'],
                motor_fidelity=fids['motor'],
                acoustic_energy=self.acoustic_energy(year),
                knowledge_bits=self.total_knowledge_bits(year),
                initiate_pool=self.initiate_pool(year),
                bluestone_count=self.bluestone_count(year),
                altar_stone_aligned=self.altar_aligned(year),
                trilithon_intact=self.trilithon_intact(year)
            )
            self.results.append(tp)
    
    def save_json(self, filename: str = 'complete_simulation.json'):
        data = [asdict(tp) for tp in self.results]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} trajectory points to {filename}")
    
    def print_summary(self):
        print("\n" + "="*60)
        print("COMPLETE SIMULATION SUMMARY")
        print("="*60)
        key_years = [2620, 2480, 2280, 2020, 1800, 1650, 1520]
        for tp in self.results:
            if tp.year_bc in key_years:
                print(f"\n{tp.year_bc} BC (Stage {tp.stage}):")
                print(f"  T30: {tp.chamber_t30:.3f}s")
                print(f"  Eng: {tp.engineering_fidelity:.2f}  Astro: {tp.astronomy_fidelity:.2f}  Gene: {tp.genealogy_fidelity:.2f}  Motor: {tp.motor_fidelity:.2f}")
                print(f"  Initiates: {tp.initiate_pool}  Bluestones: {tp.bluestone_count}")
                print(f"  Altar aligned: {tp.altar_stone_aligned}  Trilithons intact: {tp.trilithon_intact}")
                print(f"  Knowledge: {tp.knowledge_bits:.0f} bits")

if __name__ == "__main__":
    sim = CompleteSimulation()
    sim.simulate(3000, 1520)
    sim.print_summary()
    sim.save_json()
    
    print("\n" + "="*60)
    print("KEY TRANSITION POINTS")
    print("="*60)
    for tp in sim.results:
        if tp.year_bc == 2620:
            print("2620 BC: PEAK SYSTEM — Stage 2 complete, T30=0.64s, 50 initiates")
        if tp.year_bc == 2000:
            print("2000 BC: TRILITHON COLLAPSE — Read head destroyed")
        if tp.year_bc == 1630:
            print("1630 BC: Y/Z HOLES — Crash dump written")
        if tp.year_bc == 1520:
            print("1520 BC: SYSTEM HALT — Windblown fill, zero initiates")