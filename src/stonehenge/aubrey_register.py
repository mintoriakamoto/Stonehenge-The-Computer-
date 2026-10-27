# AUBREY_REGISTER_FULL.py
# Complete executable model of the Aubrey 56 as cyclic register with error correction

import numpy as np
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum

class Marker(Enum):
    SUN = "Sun"
    MOON = "Moon"
    NODE = "Node"

@dataclass
class LineagePacket:
    hole_id: int
    title: str
    engineering: Dict[str, str]
    astronomy: Dict[str, str]
    genealogy: str
    motor_engrams: List[str]

class AubreyRegister:
    def __init__(self):
        self.N_HOLES = 56
        self.NODE_STEP = 3
        self.NODE_PERIOD = 18.618
        self.DRIFT_PER_STEP = self.NODE_PERIOD - self.N_HOLES/self.NODE_STEP
        self.LEAP_HOLE_INTERVAL = 6
        self.standstill_count = 0
        self.markers = {Marker.SUN: 0, Marker.MOON: 0, Marker.NODE: 0}
        self.lineages = self._initialize_lineages()
        self.drift_history = []
        self.correction_history = []
        self.transfer_fidelity = []
    
    def _initialize_lineages(self):
        lineages = []
        engineering_specs = {
            0: ("Latitude determination", "Gnomon + circumpolar obs at 51.18°"),
            1: ("56 = 3×18.618 derivation", "Leap-hole every 6 standstills"),
            2: ("Mortise depth 60mm", "Three finger-widths, thumb knuckle gauge"),
            3: ("Tenon height 40mm", "Two finger-widths, index finger gauge"),
            4: ("Chalk packing 7 tamps", "95% Proctor, feel the lock"),
            5: ("Joint gap <5mm", "Fingertip probe, 2mm acuity"),
            6: ("Lintel level 3cm/30m", "Water tube, meniscus align"),
            7: ("Sarsen dressing", "1800 mauls, stone sings when true"),
        }
        astronomy_corrections = {i: (f"Node +{i*3} mod 56", f"Standstill drift: {i*0.049:.3f} yr = {i*18:.0f} days") for i in range(56)}
        genealogies = [
            "The Surveyor — Set the rod at 51.18°", "The Counter — Three holes per year",
            "The Mason — Three fingers deep, seven tamps", "The Joiner — Two fingers high, feel the release",
            "The Packer — Seven tamps, feel the lock", "The Fitter — Feel the gap, two millimeters",
            "The Leveller — Water finds level", "The Dresser — Stone sings when true",
            "The Archer — Brought bluestones from Preseli", "The Midwife — Delivered the Surveyor's son",
            "The Stone-Cutter — Shaped the Altar Stone", "The Transporter — Water route from Preseli",
            "The Astronomer — Counted the standstills", "The Feaster — Fed four thousand at Durrington",
            "The Surveyor's Son — Inherited the rod", "The Counter's Daughter — Kept the count",
            "The Mason's Apprentice — Learned the knuckle gauge", "The Elder — Held the master copy",
            "The Initiate — Received the whisper", "The Last — Knew the knowledge halves",
        ] + [f"Lineage {i} — Knowledge fragment {i}" for i in range(20, 56)]
        
        for i in range(56):
            eng = engineering_specs.get(i, (f"Spec {i}", "Oral tradition"))
            astro = astronomy_corrections[i]
            gene = genealogies[i] if i < len(genealogies) else f"Lineage {i}"
            lineages.append(type('LineagePacket', (), {
                'hole_id': i, 'title': f"Lineage {i}",
                'engineering': {"spec": eng[0], "method": eng[1]},
                'astronomy': {"marker": astro[0], "drift": astro[1]},
                'genealogy': gene,
                'motor_engrams': ["Mortise: thumb knuckle at 60mm", "Tenon: index finger at 40mm", 
                                 "Chalk: 7-count breath rhythm", "Joint: fingertip gap probe", "Level: water tube meniscus"]
            })())
        return lineages
    
    def advance_year(self):
        self.markers[Marker.NODE] = (self.markers[Marker.NODE] + self.NODE_STEP) % self.N_HOLES
        self.markers[Marker.SUN] = (self.markers[Marker.SUN] + 1) % self.N_HOLES
        self.markers[Marker.MOON] = (self.markers[Marker.MOON] + 13) % self.N_HOLES
    
    def standstill_event(self, observed_hole: int):
        predicted = self.markers[Marker.NODE]
        error = (observed_hole - predicted) % self.N_HOLES
        if error > self.N_HOLES/2: error -= self.N_HOLES
        self.markers[Marker.NODE] = observed_hole
        self.standstill_count += 1
        leap_applied = False
        if self.standstill_count % self.LEAP_HOLE_INTERVAL == 0:
            self.markers[Marker.NODE] = (self.markers[Marker.NODE] + 1) % self.N_HOLES
            leap_applied = True
            self.correction_history.append({'standstill': self.standstill_count, 'correction': '+1 hole'})
        self.drift_history.append({'standstill': self.standstill_count, 'predicted': predicted, 
                                   'observed': observed_hole, 'error_holes': error, 'leap_applied': leap_applied})
        return {'error_corrected': error, 'leap_applied': leap_applied}
    
    def transfer_cycle(self, year: int):
        hole = self.markers[Marker.NODE]
        lineage = self.lineages[hole]
        stage = self._get_stage(year)
        fidelity = self._fidelity_for_stage(stage)
        transferred = {'engineering': fidelity > 0.7, 'astronomy': fidelity > 0.5, 
                       'genealogy': fidelity > 0.3, 'motor': fidelity > 0.8}
        self.transfer_fidelity.append({'year': year, 'hole': hole, 'stage': stage, 
                                       'fidelity': fidelity, 'transferred': transferred})
        return transferred
    
    def _get_stage(self, year_bc): 
        if year_bc >= 2620: return 2
        elif year_bc >= 2480: return 3
        elif year_bc >= 2280: return 4
        else: return 5
    
    def _fidelity_for_stage(self, stage): return {2: 1.0, 3: 0.9, 4: 0.6, 5: 0.2}.get(stage, 0.1)
    
    def simulate(self, start_year=2620, end_year=1520):
        for year in range(start_year, end_year - 1, -1):
            self.advance_year()
            self.transfer_cycle(year)
            if (start_year - year) % 19 == 0:
                true_node = (self.markers[Marker.NODE] + int(self.standstill_count * 0.049 * 3 / 18.618)) % 56
                self.standstill_event(true_node)
        return self.generate_report()
    
    def generate_report(self):
        total = len(self.transfer_fidelity)
        return {
            'total_transfer_cycles': len(self.transfer_fidelity),
            'standstills_recorded': len(self.drift_history),
            'leap_holes_applied': len(self.correction_history),
            'engineering_lost': sum(1 for t in self.transfer_fidelity if not t['transferred']['engineering']),
            'astronomy_lost': sum(1 for t in self.transfer_fidelity if not t['transferred']['astronomy']),
            'genealogy_lost': sum(1 for t in self.transfer_fidelity if not t['transferred']['genealogy']),
            'motor_lost': sum(1 for t in self.transfer_fidelity if not t['transferred']['motor']),
            'drift_history': self.drift_history[-5:],
            'final_markers': {k.value: v for k,v in self.markers.items()},
        }

if __name__ == "__main__":
    reg = AubreyRegister()
    report = reg.simulate(2620, 1520)
    print(json.dumps(report, indent=2))
    with open('aubrey_register_report.json', 'w') as f: json.dump(report, f, indent=2)
