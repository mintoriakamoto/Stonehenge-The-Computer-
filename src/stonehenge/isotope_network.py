import numpy as np, json, networkx as nx
from dataclasses import dataclass

@dataclass
class Site:
    name: str; pigs: int
    sr_range: tuple; s34_range: tuple; o18_range: tuple; c13_range: tuple; n15_range: tuple

SITES = {
    'Durrington_Walls': Site('Durrington Walls', 50, (0.7080,0.7172), (-5,15), (-7,-3), (-22,-18), (6,10)),
    'Marden': Site('Marden', 30, (0.7086,0.7166), (-5,10), (-7,-4), (-22,-19), (5,9)),
    'West_Kennet': Site('West Kennet', 25, (0.7082,0.7133), (-3,12), (-6,-3), (-21,-18), (6,10)),
    'Mount_Pleasant': Site('Mount Pleasant', 26, (0.7082,0.7113), (-2,8), (-5,-2), (-20,-17), (7,11)),
}

def range_overlap(r1, r2):
    lo, hi = max(r1[0],r2[0]), min(r1[1],r2[1])
    return 0 if lo>=hi else (hi-lo)/(max(r1[1],r2[1])-min(r1[0],r2[0]))

def build_network(threshold=0.15):
    G = nx.Graph()
    for name, site in SITES.items():
        G.add_node(name, pigs=site.pigs)
    names = list(SITES.keys())
    iso_keys = ['sr_range','s34_range','o18_range','c13_range','n15_range']
    iso_names = ['Sr','S','O','C','N']
    weights = {'Sr':0.4,'S':0.2,'O':0.15,'C':0.15,'N':0.1}
    for i, n1 in enumerate(names):
        for n2 in names[i+1:]:
            overlaps = {iso_names[i]: range_overlap(getattr(SITES[n1], iso_keys[i]), getattr(SITES[n2], iso_keys[i])) for i in range(5)}
            comp = sum(overlaps[k]*weights[k] for k in weights)
            if comp > threshold:
                G.add_edge(n1, n2, weight=comp, **overlaps)
    return G

def range_overlap(r1, r2):
    lo, hi = max(r1[0],r2[0]), min(r1[1],r2[1])
    return 0 if lo>=hi else (hi-lo)/(max(r1[1],r2[1])-min(r1[0],r2[0]))

def analyze(G):
    return {
        'degree': nx.degree_centrality(G),
        'betweenness': nx.betweenness_centrality(G, weight='weight'),
        'eigenvector': nx.eigenvector_centrality_numpy(G, weight='weight'),
        'communities': [list(c) for c in nx.community.greedy_modularity_communities(G, weight='weight')],
        'modularity': nx.community.modularity(G, nx.community.greedy_modularity_communities(G, weight='weight'), weight='weight'),
        'avg_path': nx.average_shortest_path_length(G, weight='weight'),
        'edges': [(u,v,d['weight']) for u,v,d in G.edges(data=True)]
    }

def simulate_feasting(G, years=100):
    knowledge = {n: 1.0 for n in G.nodes()}
    diff_rate, decay_rate = 0.1, 0.02
    ext_input = {'Durrington_Walls': 0.5}
    history = {n: [] for n in G.nodes()}
    for _ in range(years):
        new_k = {}
        for n in G.nodes():
            k = knowledge[n] * (1 - decay_rate) + ext_input.get(n, 0)
            for nb in G.neighbors(n):
                k += 0.1 * G[n][nb]['weight'] * (knowledge[nb] - knowledge[n])
            new_k[n] = max(0, k)
        knowledge = new_k
        for n in G.nodes(): history[n].append(knowledge[n])
    return {'final': knowledge, 'history': history, 'equilibrium': {k: np.mean(v[-10:]) for k,v in history.items()}}

if __name__ == "__main__":
    G = build_network()
    analysis = {'degree': nx.degree_centrality(G), 'betweenness': nx.betweenness_centrality(G, weight='weight'),
                'eigenvector': nx.eigenvector_centrality_numpy(G, weight='weight'),
                'communities': [list(c) for c in nx.community.greedy_modularity_communities(G, weight='weight')],
                'modularity': nx.community.modularity(G, nx.community.greedy_modularity_communities(G, weight='weight'), weight='weight'),
                'avg_path': nx.average_shortest_path_length(G, weight='weight'),
                'edges': [(u,v,d['weight']) for u,v,d in G.edges(data=True)]}
    diff = simulate_feasting(G, 100)
    out = {'network': analysis, 'diffusion': diff}
    with open('isotope_network_analysis.json', 'w') as f: json.dump(out, f, indent=2, default=str)
    print("Centrality leaders:", {k: max(v, key=v.get) for k,v in {'deg':analysis['degree'], 'btw':analysis['betweenness'], 'eig':analysis['eigenvector']}.items()})
    print("Communities:", analysis['communities'])
    print("Equilibrium:", diff['equilibrium'])
