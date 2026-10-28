import numpy as np, json
from dataclasses import dataclass


NODAL_PERIOD_YR = 18.600  # 19 yr is the Metonic cycle, not the nodal cycle

@dataclass
class KnowledgeDomain:
    name: str; initial_bits: float; storage_substrate: str
    decay_rate: float; transfer_efficiency: float

class KnowledgeDecayModel:
    def __init__(self):
        self.domains = {
            'engineering_tolerances': KnowledgeDomain('Engineering Tolerances', 5000, 'cerebellar', 0.05, 0.95),
            'astronomical_cycles': KnowledgeDomain('Astronomical Cycles', 2000, 'hippocampal', 0.35, 0.75),
            'genealogical_registry': KnowledgeDomain('Genealogical Registry', 3000, 'hippocampal+amygdala', 0.25, 0.8),
            'motor_programs': KnowledgeDomain('Motor Programs', 4000, 'cerebellar', 0.03, 0.98),
            'lunar_correction_algo': KnowledgeDomain('Lunar Correction Algorithm', 1000, 'hippocampal+procedural', 0.20, 0.85),
        }
        self.chamber_fidelity = {2620: 1.0, 2480: 0.95, 2280: 0.75, 2020: 0.4, 1520: 0.05}
    
    def _interp_fidelity(self, year):
        years = sorted(self.chamber_fidelity.keys())
        fids = [self.chamber_fidelity[y] for y in years]
        return np.interp(year, years, fids)
    
    def simulate_decay(self, start_year=2620, end_year=1520):
        current_bits = {n: d.initial_bits for n, d in self.domains.items()}
        results = {'years': [], 'domains': {n: [] for n in self.domains}, 'total_knowledge': [], 'half_lives': {}}
        for year in range(start_year, end_year - 1, -1):
            fid = self._interp_fidelity(year)
            for name, domain in self.domains.items():
                elapsed = start_year - year
                current_bits[name] = domain.initial_bits * np.exp(-domain.decay_rate * elapsed)
                loss = domain.initial_bits * (1 - domain.transfer_efficiency * fid)
                current_bits[name] -= loss * 0.1
            if (2620 - year) and int((2620 - year) // NODAL_PERIOD_YR) > int((2620 - year - 1) // NODAL_PERIOD_YR):
                for name in ['astronomical_cycles', 'lunar_correction_algo']:
                    current_bits[name] *= 1.1
            results['years'].append(year)
            for n in self.domains: results['domains'][n].append(current_bits[n])
            results['total_knowledge'].append(sum(current_bits.values()))
            for name, domain in self.domains.items():
                if current_bits[name] < domain.initial_bits / 2 and name not in results['half_lives']:
                    results['half_lives'][name] = 2620 - year
        return results
    
    def rate_distortion_analysis(self):
        total_source = sum(d.initial_bits for d in self.domains.values()) * 4000
        avg_ret = np.mean([d.transfer_efficiency for d in self.domains.values()])
        avg_fid = np.mean(list(self.chamber_fidelity.values()))
        channel_cap = 50 * sum(d.initial_bits for d in self.domains.values()) * avg_ret * np.mean(list(self.chamber_fidelity.values()))
        return {'source_entropy_bits': total_source, 'channel_capacity_bits': channel_cap,
                'compression_ratio': 80, 'distortion': 1 - channel_cap/total_source,
                'builder_initiate_ratio': 80}
    
    def mutual_information_network(self):
        domains = list(self.domains.keys())
        corr = np.array([[1.0,0.3,0.2,0.7,0.2],[0.3,1.0,0.4,0.2,0.8],[0.2,0.4,1.0,0.1,0.3],[0.7,0.2,0.1,1.0,0.2],[0.2,0.8,0.3,0.2,1.0]])
        mi_pairs = {}
        for i, d1 in enumerate(self.domains):
            for j, d2 in enumerate(self.domains):
                if i < j:
                    rho = corr[i,j]
                    if abs(rho) < 1:
                        mi = -0.5 * np.log2(1 - rho**2)
                        mi_pairs[f"{d1}<->{d2}"] = mi
        return {'correlation_matrix': corr.tolist(), 'domains': list(self.domains.keys()), 'pairwise_mi_bits': mi_pairs}

if __name__ == "__main__":
    import numpy as np, json
    model = KnowledgeDecayModel()
    decay = model.simulate_decay(2620, 1520)
    rd = model.rate_distortion_analysis()
    mi = model.mutual_information_network()
    out = {'decay': decay, 'rate_distortion': rd, 'mutual_info': mi}
    with open('knowledge_decay_analysis.json', 'w') as f: json.dump(out, f, indent=2, default=str)
    print("Half-lives:", decay['half_lives'])
    print("Rate-distortion:", rd)
    print("MI pairs:", mi['pairwise_mi_bits'])
