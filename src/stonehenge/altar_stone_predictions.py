import numpy as np, json

def generate_altar_stone_predictions():
    preds = [
        {"test": "Mica Wear Topography", "pred": "56 circular zones 80-120mm, 10-100um depth",
         "criterion": ">=50 zones Gaussian depth aligned to horseshoe axis",
         "falsification": "Random wear, <40 zones, no alignment",
         "equipment": "Keyence VK-X3000 confocal, 0.1um res"},
        {"test": "Piezoelectric Response Map", "pred": "56 voltage peaks 0.5-1.2mV at 500N, 12uV separation",
         "criterion": ">=50 peaks >5uV separation correlated to wear zones",
         "falsification": "Uniform response <2uV variation, <30 peaks",
         "equipment": "Kistler 9203 + Keithley 6514 + XY stage"},
        {"test": "Magnetic Stratigraphy (SQUID)", "pred": "560 remanence layers at 18.6yr spacing, 0.1-1uT",
         "criterion": ">=500 layers with 18.6+/-0.5yr periodicity",
         "falsification": "Random/no layering, wrong periodicity",
         "equipment": "2G SQUID, 25mm oriented cores"},
        {"test": "Residual Stress (EBSD)", "pred": "56 compression cones 10-50mm depth, 50-200MPa",
         "criterion": ">=50 cones at wear zones, radial stress orientation",
         "falsification": "Uniform stress, <30 cones, no correlation",
         "equipment": "SEM-EBSD, 5mmx50mm cores"},
        {"test": "Thermoluminescence", "pred": "56 TL peaks at 200-400C from ceremonial fires",
         "criterion": ">=50 peaks with 18.6yr periodicity",
         "falsification": "Broad single peak, <30 peaks, no periodicity",
         "equipment": "Riso TL/OSL-DA-20 reader"},
        {"test": "Lipid Stratigraphy (ToF-SIMS)", "pred": "56 lipid-enriched layers at wear zones",
         "criterion": ">=50 lipid-enriched layers at wear zones, 2x enrichment",
         "falsification": "Uniform lipids, <30 enriched layers",
         "equipment": "ToF-SIMS Bi3+, 100nm depth res"},
        {"test": "Acoustic Impedance (Vibrometry)", "pred": "56 high-damping zones at wear locations Q=50-200 vs 500-1000",
         "criterion": ">=50 high-damping zones correlated to wear",
         "falsification": "Uniform damping, <30 zones",
         "equipment": "Polytec PSV-500, 110Hz excitation"},
    ]
    return preds

def generate_test_matrix(predictions):
    matrix = {'tier_1': [], 'tier_2': [], 'tier_3': [], 'total_predictions': len(predictions)}
    for p in predictions:
        entry = {
            'test': p['test'],
            'predicted': p['pred'],
            'criterion': p['criterion'],
            'falsification': p['falsification'],
            'equipment': p['equipment'],
            'difficulty': 'LOW' if 'confocal' in p['equipment'].lower() or 'vibrometry' in p['equipment'].lower() or 'XRF' in p['equipment']
                         else 'MEDIUM' if 'force sensor' in p['equipment'].lower() or 'electrometer' in p['equipment'].lower()
                         else 'HIGH'
        }
        if entry['difficulty'] == 'LOW':
            tier = 'tier_1'
        elif entry['difficulty'] == 'MEDIUM':
            tier = 'tier_2'
        else:
            tier = 'tier_3'
        entry['tier'] = tier
        if tier == 'tier_1':
            matrix['tier_1'].append(entry)
        elif tier == 'tier_2':
            matrix['tier_2'].append(entry)
        else:
            matrix['tier_3'].append(entry)
    matrix['pass_threshold'] = '5/7 tests must pass for hypothesis confirmation'
    return matrix

if __name__ == '__main__':
    preds = generate_altar_stone_predictions()
    matrix = generate_test_matrix(preds)
    with open('altar_stone_test_matrix.json', 'w') as f:
        json.dump(matrix, f, indent=2)
    print('Predictions:', len(preds))
    print('Tier 1:', len(matrix['tier_1']), 'Tier 2:', len(matrix['tier_2']), 'Tier 3:', len(matrix['tier_3']))
