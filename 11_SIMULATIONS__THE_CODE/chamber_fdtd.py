#!/usr/bin/env python3
"""
CHAMBER_FDTD.py
k-Wave FDTD setup for full Stonehenge acoustic simulation.
Generates medium grids (ρ, c, α) for CUDA-accelerated simulation.
Default grid: 200³ = 8M voxels at 0.5 m (100 m domain).
"""

import numpy as np
import json
import os

def generate_stonehenge_geometry():
    """Generate complete stone positions for FDTD simulation."""
    stones = {
        'sarsen_circle': [],
        'trilithons': [],
        'bluestone_outer': [],
        'bluestone_inner': [],
        'altar_stone': [],
        'heel_stone': [],
        'station_stones': [],
        'aubrey_holes': []
    }
    
    # Sarsen Circle: 30 uprights on a ~30.7 m (100.8 ft) circle; sources give 30-33 m
    R = 15.36  # meters
    for i in range(30):
        angle = 2 * np.pi * i / 30
        stones['sarsen_circle'].append({
            'id': f'S{i+1}',
            'type': 'sarsen_upright',
            'x': R * np.cos(angle),
            'y': R * np.sin(angle),
            'z': 0,
            'height': 4.1,
            'width': 2.0,
            'depth': 1.1,
            'material': 'silcrete'
        })
    
    # Sarsen Lintels: 30 lintels on top
    for i in range(30):
        angle = 2 * np.pi * i / 30
        stones['sarsen_circle'].append({
            'id': f'L{i+1}',
            'type': 'sarsen_lintel',
            'x': R * np.cos(angle),
            'y': R * np.sin(angle),
            'z': 4.1,
            'length': 3.2,
            'width': 1.0,
            'depth': 0.8,
            'material': 'silcrete'
        })
    
    # Trilithons: 5 horseshoe pairs + lintels
    horseshoe_R = 7.5  # meters
    horseshoe_angles = [-2*np.pi/5, -np.pi/5, 0, np.pi/5, 2*np.pi/5]
    for j, angle in enumerate(horseshoe_angles):
        # Upright 1
        stones['trilithons'].append({
            'id': f'T{j*2+1}',
            'type': 'trilithon_upright',
            'x': horseshoe_R * np.cos(angle - 0.1),
            'y': horseshoe_R * np.sin(angle - 0.1),
            'z': 0,
            'height': 6.7,
            'width': 2.0,
            'depth': 1.2,
            'material': 'silcrete'
        })
        # Upright 2
        stones['trilithons'].append({
            'id': f'T{j*2+2}',
            'type': 'trilithon_upright',
            'x': horseshoe_R * np.cos(angle + 0.1),
            'y': horseshoe_R * np.sin(angle + 0.1),
            'z': 0,
            'height': 6.7,
            'width': 2.0,
            'depth': 1.2,
            'material': 'silcrete'
        })
        # Lintel
        stones['trilithons'].append({
            'id': f'TL{j+1}',
            'type': 'trilithon_lintel',
            'x': horseshoe_R * np.cos(angle),
            'y': horseshoe_R * np.sin(angle),
            'z': 6.7,
            'length': 4.2,
            'width': 1.0,
            'depth': 0.8,
            'material': 'silcrete'
        })
    
    # Bluestone Outer Circle: ~60 stones at 15m radius
    for i in range(60):
        angle = 2 * np.pi * i / 60
        R_outer = 11.5  # ~23 m (75 ft) bluestone circle
        stones['bluestone_outer'].append({
            'id': f'BO{i+1}',
            'type': 'bluestone',
            'x': R_outer * np.cos(angle),
            'y': R_outer * np.sin(angle),
            'z': 0,
            'height': 2.5,
            'width': 1.0,
            'depth': 0.7,
            'material': 'dolerite'
        })
    
    # Bluestone Inner Oval: 19 stones
    for i in range(19):
        angle = 2 * np.pi * i / 19
        R_inner = 8.0
        stones['bluestone_inner'].append({
            'id': f'BI{i+1}',
            'type': 'bluestone',
            'x': R_inner * np.cos(angle),
            'y': R_inner * np.sin(angle),
            'z': 0,
            'height': 2.0,
            'width': 0.8,
            'depth': 0.6,
            'material': 'dolerite'
        })
    
    # Altar Stone (recumbent at center)
    stones['altar_stone'].append({
        'id': 'ALTAR',
        'type': 'altar_stone',
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'length': 4.9,
        'width': 1.0,
        'depth': 0.5,
        'material': 'micaceous_sandstone',
        'piezoelectric': True,
        'd14': 0.7e-12  # C/N; quartz single-crystal |d14|, upper bound for bulk sandstone
    })
    
    # Heel Stone
    stones['heel_stone'].append({
        'id': 'HEEL',
        'type': 'sarsen_heel',
        'x': 80.0,
        'y': 0.0,
        'z': 0,
        'height': 4.7,
        'width': 2.5,
        'depth': 2.0,
        'material': 'silcrete'
    })
    
    # Station Stones
    station_pos = [
        (-33, -33), (33, -33), (-33, 33), (33, 33)
    ]
    for i, (x, y) in enumerate(station_pos):
        stones['station_stones'].append({
            'id': f'ST{i+1}',
            'type': 'station_stone',
            'x': x,
            'y': y,
            'z': 0,
            'height': 2.5,
            'width': 1.5,
            'depth': 0.8,
            'material': 'silcrete'
        })
    
    # Aubrey Holes: 56 holes at 44m radius
    for i in range(56):
        angle = 2 * np.pi * i / 56
        R_aubrey = 44.0
        stones['aubrey_holes'].append({
            'id': f'AH{i+1}',
            'type': 'aubrey_hole',
            'x': R_aubrey * np.cos(angle),
            'y': R_aubrey * np.sin(angle),
            'z': 0,
            'diameter': 1.0,
            'depth': 1.2
        })
    
    return stones

def create_medium_grid(stones, grid_size=200, voxel_size=0.5):
    """
    Create k-Wave medium grids.
    
    Args:
        stones: dict from generate_stonehenge_geometry()
        grid_size: number of voxels per dimension
        voxel_size: meters per voxel
    
    Returns:
        dict with 'rho', 'c', 'alpha' arrays
    """
    # Physical bounds
    extent = grid_size * voxel_size
    x = np.linspace(-extent/2, extent/2, grid_size)
    y = np.linspace(-extent/2, extent/2, grid_size)
    z = np.linspace(0, extent/2, grid_size//2)  # half space (ground)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Initialize with chalk properties (background)
    rho = np.full_like(X, 1800.0)  # kg/m³
    c = np.full_like(X, 2000.0)    # m/s
    alpha = np.full_like(X, 2.0)   # dB/MHz/cm
    
    # Material properties
    materials = {
        'silcrete': {'rho': 2600, 'c': 5800, 'alpha': 0.5},
        'dolerite': {'rho': 2900, 'c': 6200, 'alpha': 0.3},
        'micaceous_sandstone': {'rho': 2400, 'c': 4500, 'alpha': 0.8},
        'chalk': {'rho': 1800, 'c': 2000, 'alpha': 2.0}
    }
    
    # Place stones in grid
    for category, stone_list in stones.items():
        for stone in stone_list:
            # Aubrey holes are chalk-filled pits: no material contrast against the
            # chalk background, so they are not placed in the medium.
            if 'material' not in stone:
                continue
            mat = materials[stone['material']]
            
            # Create bounding box for stone
            if stone['type'] in ['sarsen_upright', 'trilithon_upright', 'sarsen_heel', 'station_stone']:
                hx, hy, hz = stone['width']/2, stone['depth']/2, stone['height']/2
                cx, cy, cz = stone['x'], stone['y'], stone['z'] + stone['height']/2
            elif stone['type'] in ['sarsen_lintel', 'trilithon_lintel']:
                hx, hy, hz = stone['length']/2, stone['width']/2, stone['depth']/2
                cx, cy, cz = stone['x'], stone['y'], stone['z'] + stone['depth']/2
            elif stone['type'] == 'bluestone':
                hx, hy, hz = stone['width']/2, stone['depth']/2, stone['height']/2
                cx, cy, cz = stone['x'], stone['y'], stone['z'] + stone['height']/2
            elif stone['type'] == 'altar_stone':
                hx, hy, hz = stone['length']/2, stone['width']/2, stone['depth']/2
                cx, cy, cz = stone['x'], stone['y'], stone['depth']/2
            else:
                continue
            
            mask = (np.abs(X - cx) < hx) & (np.abs(Y - cy) < hy) & (np.abs(Z - cz) < hz)
            rho[mask] = mat['rho']
            c[mask] = mat['c']
            alpha[mask] = mat['alpha']
    
    return {'rho': rho, 'c': c, 'alpha': alpha, 'voxel_size': voxel_size, 'grid_size': grid_size}

def save_medium(medium, filename='stonehenge_medium.npz'):
    """Save medium grids to NPZ file."""
    np.savez_compressed(
        filename,
        rho=medium['rho'].astype(np.float32),
        c=medium['c'].astype(np.float32),
        alpha=medium['alpha'].astype(np.float32),
        voxel_size=np.array([medium['voxel_size']], dtype=np.float32),
        grid_size=np.array([medium['grid_size']], dtype=np.int32)
    )
    print(f"Saved medium to {filename}")
    print(f"  Shape: {medium['rho'].shape}")
    print(f"  Voxels: {medium['rho'].size:,}")
    print(f"  Memory: {medium['rho'].nbytes * 3 / 1e9:.2f} GB")

def save_geometry_json(stones, filename='stonehenge_geometry.json'):
    """Save stone geometry to JSON."""
    # Convert numpy types to native Python
    def convert(obj):
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj
    
    with open(filename, 'w') as f:
        json.dump(convert(stones), f, indent=2)
    print(f"Saved geometry to {filename}")

if __name__ == "__main__":
    print("="*60)
    print("STONEHENGE FDTD MEDIUM GENERATOR")
    print("="*60)
    
    print("\nGenerating stone geometry...")
    stones = generate_stonehenge_geometry()
    total_stones = sum(len(v) for v in stones.values())
    print(f"Total stones: {total_stones}")
    for cat, lst in stones.items():
        print(f"  {cat}: {len(lst)}")
    
    print("\nCreating medium grids (200³ = 8M voxels, half-space = 4M)...")
    medium = create_medium_grid(stones, grid_size=200, voxel_size=0.5)
    
    print("\nSaving outputs...")
    save_geometry_json(stones)
    save_medium(medium, 'stonehenge_medium.npz')
    
    print("\n" + "="*60)
    print("READY FOR k-WAVE FDTD SIMULATION")
    print("="*60)
    print("Next steps:")
    print("  1. Load stonehenge_medium.npz in k-Wave (MATLAB/Python)")
    print("  2. Define source at Altar Stone position (0,0,0)")
    print("  3. Define sensors at 29 positions (Cox 2020 config)")
    print("  4. Run FDTD at 500-1000 Hz")
    print("  5. Extract T30, speech gain, modal frequencies")
    print("\nGPU: NVIDIA CMP 170HX (42 GB HBM2e) recommended")