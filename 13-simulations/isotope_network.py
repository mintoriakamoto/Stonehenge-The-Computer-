#!/usr/bin/env python3
"""
ISOTOPE_NETWORK.py
Graph analysis of Madgwick 2019 pig isotope data (131 pigs, 5 isotopes).
Reconstructs Neolithic social/political network.
"""

import numpy as np
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple
import networkx as nx

@dataclass
class Site:
    name: str
    pigs: int
    sr_range: Tuple[float, float]
    s34_range: Tuple[float, float]
    o18_range: Tuple[float, float]
    c13_range: Tuple[float, float]
    n15_range: Tuple[float, float]

# Madgwick et al. 2019, Sci. Adv., Table 1 (PMC6415963): per-site n and min-max ranges.
SITES = {
    'Durrington_Walls': Site('Durrington Walls', 89, (0.7080, 0.7172), (-1.6, 19.6), (23.6, 27.7), (-21.3, -19.7), (5.2, 8.0)),
    'Marden': Site('Marden', 8, (0.7086, 0.7166), (6.5, 13.0), (23.2, 27.4), (-22.0, -20.3), (5.1, 6.8)),
    'West_Kennet': Site('West Kennet Palisades', 16, (0.7082, 0.7133), (6.9, 17.5), (24.4, 27.6), (-22.4, -20.6), (3.4, 7.2)),
    'Mount_Pleasant': Site('Mount Pleasant', 18, (0.7082, 0.7113), (2.8, 18.8), (23.2, 28.9), (-23.1, -20.9), (4.5, 9.1)),
}

def compute_isotope_overlap(site1: Site, site2: Site) -> Dict[str, float]:
    def range_overlap(r1, r2):
        lo = max(r1[0], r2[0])
        hi = min(r1[1], r2[1])
        if lo >= hi: return 0.0
        intersection = hi - lo
        union = max(r1[1], r2[1]) - min(r1[0], r2[0])
        return intersection / union
    overlaps = {}
    for iso_name, r1, r2 in [
        ('Sr', site1.sr_range, site2.sr_range),
        ('S', site1.s34_range, site2.s34_range),
        ('O', site1.o18_range, site2.o18_range),
        ('C', site1.c13_range, site2.c13_range),
        ('N', site1.n15_range, site2.n15_range),
    ]:
        overlaps[iso_name] = range_overlap(r1, r2)
    weights = {'Sr': 0.4, 'S': 0.2, 'O': 0.15, 'C': 0.15, 'N': 0.1}
    composite = sum(overlaps[k] * weights[k] for k in weights)
    return {'composite': composite, **overlaps}

def build_network(sites: Dict[str, Site], threshold: float = 0.15) -> nx.Graph:
    G = nx.Graph()
    for name, site in sites.items():
        G.add_node(name, pigs=site.pigs, **{
            'sr_range': site.sr_range, 's34_range': site.s34_range,
            'o18_range': site.o18_range, 'c13_range': site.c13_range,
            'n15_range': site.n15_range
        })
    names = list(sites.keys())
    for i, name1 in enumerate(names):
        for name2 in names[i+1:]:
            overlaps = compute_isotope_overlap(sites[name1], sites[name2])
            if overlaps['composite'] > threshold:
                G.add_edge(name1, name2, weight=overlaps['composite'],
                       distance=1.0 / overlaps['composite'], **overlaps)
    return G

def analyze_network(G: nx.Graph) -> Dict:
    communities = nx.community.greedy_modularity_communities(G, weight='weight')
    return {
        'nodes': list(G.nodes()),
        'edges': [(u, v, d['weight']) for u, v, d in G.edges(data=True)],
        'degree_centrality': nx.degree_centrality(G),
        'betweenness_centrality': nx.betweenness_centrality(G, weight='distance'),
        'eigenvector_centrality': nx.eigenvector_centrality_numpy(G, weight='weight'),
        'communities': [list(c) for c in communities],
        'modularity': nx.community.modularity(G, communities, weight='weight'),
        'density': nx.density(G),
        'avg_clustering': nx.average_clustering(G, weight='weight'),
    }

if __name__ == "__main__":
    print("="*60)
    print("ISOTOPE NETWORK ANALYSIS — MADGWICK 2019 DATA")
    print("="*60)
    G = build_network(SITES, threshold=0.15)
    print(f"Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    analysis = analyze_network(G)
    print(f"\nNetwork Properties:")
    print(f"  Density: {analysis['density']:.3f}")
    print(f"  Modularity: {analysis['modularity']:.3f}")
    print(f"  Clustering: {analysis['avg_clustering']:.3f}")
    print(f"\nCentrality Rankings:")
    for metric_name, metric in [
        ('Degree', analysis['degree_centrality']),
        ('Betweenness', analysis['betweenness_centrality']),
        ('Eigenvector', analysis['eigenvector_centrality']),
    ]:
        sorted_nodes = sorted(metric.items(), key=lambda x: x[1], reverse=True)
        print(f"  {metric_name}:")
        for node, val in sorted_nodes:
            print(f"    {node}: {val:.3f}")
    print(f"\nCommunities (Modularity: {analysis['modularity']:.3f}):")
    for i, comm in enumerate(analysis['communities']):
        print(f"  Community {i+1}: {comm}")
    with open('isotope_network_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    print("\nFull analysis saved to isotope_network_analysis.json")
