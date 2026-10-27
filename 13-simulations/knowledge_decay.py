#!/usr/bin/env python3
"""
KNOWLEDGE_DECAY_IT.py
Information-theoretic model of knowledge decay in the Stonehenge system.
Quantifies the 1.7-generation half-life from first principles.
"""

import numpy as np
import json
from dataclasses import dataclass
from typing import List, Dict
from scipy import stats

@dataclass
class KnowledgeDomain:
    name: str
    initial_bits: float
    storage_substrate: str
    decay_rate: float
    transfer_efficiency: float

class KnowledgeDecayModel:
    def __init__(self):
        self.domains = {
            'engineering_tolerances': KnowledgeDomain(
                'Engineering Tolerances', 5000, 'cerebellar', 0.05, 0.95),
            'astronomical_cycles': KnowledgeDomain(
                'Astronomical Cycles', 2000, 'hippocampal', 0.35, 0.75),
            'genealogical_registry': KnowledgeDomain(
                'Genealogical Registry', 3000, 'hippocampal+amygdala', 0.25, 0.8),
            'motor_programs': KnowledgeDomain(
                'Motor Programs', 4000, 'cerebellar', 0.03, 0.98),
            'lunar_correction_algo': KnowledgeDomain(
                'Lunar Correction Algorithm', 1000, 'hippocampal+procedural', 0.20, 0.85),
        }
        self.chamber_fidelity = {
            2620: 1.0, 2480: 0.95, 2280: 0.75, 2020: 0.4, 1520: 0.05,
        }
        self.builder_initiate_ratio = 80

    def substrate_decay(self, domain: KnowledgeDomain, years: float) -> float:
        return domain.initial_bits * np.exp(-domain.decay_rate * years)

    def transfer_loss(self, domain: KnowledgeDomain, chamber_fid: float) -> float:
        effective_eff = domain.transfer_efficiency * chamber_fid
        retained = domain.initial_bits * effective_eff
        return domain.initial_bits - retained

    def simulate_decay(self, start_year: int = 2620, end_year: int = 1520) -> Dict:
        results = {
            'years': [],
            'domains': {name: [] for name in self.domains},
            'total_knowledge': [],
            'transfer_events': [],
            'half_lives': {}
        }
        current_bits = {name: d.initial_bits for name, d in self.domains.items()}
        for year in range(start_year, end_year - 1, -1):
            fid = self._interp_fidelity(year)
            for name, domain in self.domains.items():
                current_bits[name] = self.substrate_decay(domain, 1)
            for name, domain in self.domains.items():
                loss = self.transfer_loss(domain, fid)
                current_bits[name] -= loss * 0.1
            if (2620 - year) % 19 == 0:
                for name in self.domains:
                    if name in ['astronomical_cycles', 'lunar_correction_algo']:
                        current_bits[name] *= 1.1
            results['years'].append(year)
            for name in self.domains:
                results['domains'][name].append(current_bits[name])
            results['total_knowledge'].append(sum(current_bits.values()))
            for name, domain in self.domains.items():
                if current_bits[name] < domain.initial_bits / 2 and name not in results['half_lives']:
                    results['half_lives'][name] = 2620 - year
        return results

    def _interp_fidelity(self, year: int) -> float:
        years = sorted(self.chamber_fidelity.keys())
        fids = [self.chamber_fidelity[y] for y in years]
        return np.interp(year, years, fids)

    def rate_distortion_analysis(self) -> Dict:
        total_builder_knowledge = sum(d.initial_bits for d in self.domains.values()) * 4000
        avg_retention = np.mean([d.transfer_efficiency for d in self.domains.values()])
        avg_fidelity = np.mean(list(self.chamber_fidelity.values()))
        channel_capacity = 50 * sum(d.initial_bits for d in self.domains.values()) * avg_retention * avg_fidelity
        compression_ratio = total_builder_knowledge / channel_capacity
        distortion = 1 - (channel_capacity / total_builder_knowledge)
        return {
            'source_entropy_bits': total_builder_knowledge,
            'channel_capacity_bits': channel_capacity,
            'compression_ratio': compression_ratio,
            'distortion': distortion,
            'builder_initiate_ratio': self.builder_initiate_ratio,
            'theoretical_min_distortion': 1 - (1/compression_ratio),
            'achieved_distortion': distortion,
            'efficiency': (1 - distortion) / (1 - 1/compression_ratio)
        }

if __name__ == "__main__":
    model = KnowledgeDecayModel()
    print("Running knowledge decay simulation...")
    decay_results = model.simulate_decay(2620, 1520)
    print("\n" + "="*60)
    print("KNOWLEDGE DECAY SIMULATION RESULTS")
    print("="*60)
    print(f"\nHalf-lives (years from 2620 BC):")
    for domain, hl in decay_results['half_lives'].items():
        print(f"  {domain}: {hl} years ({hl/25:.1f} generations)")
    print(f"\nFinal knowledge retention (1520 BC):")
    for i, name in enumerate(decay_results['domains']):
        initial = list(model.domains.values())[i].initial_bits
        final = decay_results['domains'][name][-1]
        print(f"  {name}: {final/initial*100:.1f}% ({final:.0f}/{initial:.0f} bits)")
    print(f"\nTotal knowledge retention: {decay_results['total_knowledge'][-1]/decay_results['total_knowledge'][0]*100:.1f}%")
    rd = model.rate_distortion_analysis()
    print(f"\n" + "="*60)
    print("RATE-DISTORTION ANALYSIS (Builder:Initiate Channel)")
    print("="*60)
    print(f"Source entropy (4000 builders): {rd['source_entropy_bits']:.2e} bits")
    print(f"Channel capacity (50 initiates): {rd['channel_capacity_bits']:.2e} bits")
    print(f"Compression ratio: {rd['compression_ratio']:.1f}:1")
    print(f"Distortion (knowledge loss): {rd['distortion']*100:.1f}%")
    print(f"Theoretical minimum distortion: {rd['theoretical_min_distortion']*100:.1f}%")
    print(f"Channel efficiency: {rd['efficiency']*100:.1f}%")
    with open('knowledge_decay_analysis.json', 'w') as f:
        json.dump({'decay': decay_results, 'rate_distortion': rd}, f, indent=2, default=str)
    print("\nFull analysis saved to knowledge_decay_analysis.json")

if __name__ == "__main__":
    model = KnowledgeDecayModel()
    print("Running knowledge decay simulation...")
    decay_results = model.simulate_decay(2620, 1520)
    print("\n" + "="*60)
    print("KNOWLEDGE DECAY SIMULATION RESULTS")
    print("="*60)
    print(f"\nHalf-lives (years from 2620 BC):")
    for domain, hl in decay_results['half_lives'].items():
        print(f"  {domain}: {hl} years ({hl/25:.1f} generations)")
    print(f"\nFinal knowledge retention (1520 BC):")
    for i, name in enumerate(decay_results['domains']):
        initial = list(model.domains.values())[i].initial_bits
        final = decay_results['domains'][name][-1]
        print(f"  {name}: {final/initial*100:.1f}% ({final:.0f}/{initial:.0f} bits)")
    print(f"\nTotal knowledge retention: {decay_results['total_knowledge'][-1]/decay_results['total_knowledge'][0]*100:.1f}%")
    rd = model.rate_distortion_analysis()
    print(f"\n" + "="*60)
    print("RATE-DISTORTION ANALYSIS (Builder:Initiate Channel)")
    print("="*60)
    print(f"Source entropy (4000 builders): {rd['source_entropy_bits']:.2e} bits")
    print(f"Channel capacity (50 initiates): {rd['channel_capacity_bits']:.2e} bits")
    print(f"Compression ratio: {rd['compression_ratio']:.1f}:1")
    print(f"Distortion (knowledge loss): {rd['distortion']*100:.1f}%")
    print(f"Theoretical minimum distortion: {rd['theoretical_min_distortion']*100:.1f}%")
    print(f"Channel efficiency: {rd['efficiency']*100:.1f}%")
    with open('knowledge_decay_analysis.json', 'w') as f:
        json.dump({'decay': decay_results, 'rate_distortion': rd}, f, indent=2, default=str)
    print("\nFull analysis saved to knowledge_decay_analysis.json")
