import numpy as np, json

materials = {'sarsen': {'rho':2650, 'c':5500, 'alpha':0.01},
             'bluestone': {'rho':2900, 'c':6000, 'alpha':0.005},
             'chalk': {'rho':1800, 'c':2000, 'alpha':0.1},
             'air': {'rho':1.2, 'c':343, 'alpha':0.0}}

def generate_stonehenge_geometry():
    stones = []
    # Trilithons (5 horseshoe)
    for i in range(5):
        r = 4.5 - i*0.9
        stones.append({'name':f'Upright_55_{i}', 'mat':'sarsen', 'pos':[-r, -r, 0], 'dim':[2.0,1.0,7.0-i*0.3]})
        stones.append({'name':f'Upright_56_{i}', 'mat':'sarsen', 'pos':[r, r, 0], 'dim':[2.0,1.0,7.0-i*0.3]})
        stones.append({'name':f'Lintel_{i}', 'mat':'sarsen', 'pos':[0, 0, 7.0-i*0.3], 'dim':[4.5-i*0.4, 1.0, 0.5]})
    # Sarsen Circle (30)
    for i in range(30):
        a = 2*np.pi*i/30 - np.pi/2
        x, y = 15*np.cos(a), 15*np.sin(a)
        stones.append({'name':f'Circle_Upright_{i}', 'mat':'sarsen', 'pos':[x,y,0], 'dim':[1.5,1.0,4.5]})
        stones.append({'name':f'Circle_Lintel_{i}', 'mat':'sarsen', 'pos':[x,y,4.5], 'dim':[3.2,1.0,0.5]})
    # Bluestone Horseshoe (19)
    for i in range(19):
        a = 2*np.pi*i/19 - np.pi/2
        stones.append({'name':f'BH_{i}', 'mat':'bluestone', 'pos':[6*np.cos(a), 6*np.sin(a), 0], 'dim':[0.8,0.5,2.5]})
    # Outer Bluestone Circle (50)
    for i in range(50):
        a = 2*np.pi*i/50 - np.pi/2
        stones.append({'name':f'BO_{i}', 'mat':'bluestone', 'pos':[12*np.cos(a), 12*np.sin(a), 0], 'dim':[0.6,0.4,2.0]})
    # Altar Stone
    stones.append({'name':'Altar_Stone', 'mat':'bluestone', 'pos':[0,0,0], 'dim':[5.0,1.0,0.5]})
    # Heel Stone
    stones.append({'name':'Heel_Stone', 'mat':'sarsen', 'pos':[80,0,0], 'dim':[2.5,1.5,5.0]})
    return stones

def create_medium(stones, dx=0.1):
    all_pos = np.array([s['pos'] for s in stones])
    all_dim = np.array([s['dim'] for s in stones])
    min_c = np.min(all_pos - all_dim/2, axis=0) - 5
    max_c = np.max(all_pos + all_dim/2, axis=0) + 5
    Nx, Ny, Nz = [int((max_c[i]-min_c[i])/dx)+1 for i in range(3)]
    
    rho = np.full((Nx,Ny,Nz), 1.2); c = np.full((Nx,Ny,Nz), 343); alpha = np.full((Nx,Ny,Nz), 0.0)
    gz = int((0 - (min_c[2]))/dx)
    rho[:,:,:gz] = 1800; c[:,:,:gz] = 2000; alpha[:,:,:gz] = 0.1
    
    for s in stones:
        m = materials[s['mat']]
        x0 = int((s['pos'][0]-s['dim'][0]/2 - min_c[0])/dx)
        y0 = int((s['pos'][1]-s['dim'][1]/2 - min_c[1])/dx)
        z0 = int((s['pos'][2]-s['dim'][2]/2 - min_c[2])/dx)
        nx, ny, nz = int(s['dim'][0]/dx), int(s['dim'][1]/dx), int(s['dim'][2]/dx)
        x1, y1, z1 = min(x0+nx, rho.shape[0]), min(y0+ny, rho.shape[1]), min(z0+nz, rho.shape[2])
        if x1>x0 and y1>y0 and z1>z0:
            rho[x0:x1, y0:y1, z0:z1] = m['rho']
            c[x0:x1, y0:y1, z0:z1] = m['c']
            alpha[x0:x1, y0:y1, z0:z1] = m['alpha']
    
    return (rho, c, alpha), {'dx':dx, 'Nx':Nx, 'Ny':Ny, 'Nz':Nz, 'min_c':min_c.tolist()}

def main():
    stones = []
    # Trilithons
    for i in range(5):
        r = 4.5 - i*0.9
        stones.append({'name':f'Upright_55_{i}', 'mat':'sarsen', 'pos':[-r, -r, 0], 'dim':[2.0,1.0,7.0-i*0.3]})
        stones.append({'name':f'Upright_56_{i}', 'mat':'sarsen', 'pos':[r, r, 0], 'dim':[2.0,1.0,7.0-i*0.3]})
        stones.append({'name':f'Lintel_{i}', 'mat':'sarsen', 'pos':[0, 0, 7.0-i*0.3], 'dim':[4.5-i*0.4, 1.0, 0.5]})
    for i in range(30):
        a = 2*np.pi*i/30 - np.pi/2
        x, y = 15*np.cos(a), 15*np.sin(a)
        stones.append({'name':f'Circle_Upright_{i}', 'mat':'sarsen', 'pos':[x,y,0], 'dim':[1.5,1.0,4.5]})
        stones.append({'name':f'Circle_Lintel_{i}', 'mat':'sarsen', 'pos':[x,y,4.5], 'dim':[3.2,1.0,0.5]})
    for i in range(19):
        a = 2*np.pi*i/19 - np.pi/2
        stones.append({'name':f'BH_{i}', 'mat':'bluestone', 'pos':[6*np.cos(a), 6*np.sin(a), 0], 'dim':[0.8,0.5,2.5]})
    for i in range(50):
        a = 2*np.pi*i/50 - np.pi/2
        stones.append({'name':f'BO_{i}', 'mat':'bluestone', 'pos':[12*np.cos(a), 12*np.sin(a), 0], 'dim':[0.6,0.4,2.0]})
    stones.append({'name':'Altar_Stone', 'mat':'bluestone', 'pos':[0,0,0], 'dim':[5.0,1.0,0.5]})
    stones.append({'name':'Heel_Stone', 'mat':'sarsen', 'pos':[80,0,0], 'dim':[2.5,1.5,5.0]})
    
    medium, grid = create_medium(stones, 0.1)
    np.savez('stonehenge_medium.npz', rho=medium[0], c=medium[1], alpha=medium[2], grid_info=grid)
    with open('stonehenge_geometry.json', 'w') as f: json.dump(stones, f, indent=2)
    print(f"Grid: {grid['Nx']}x{grid['Ny']}x{grid['Nz']} = {grid['Nx']*grid['Ny']*grid['Nz']:,} voxels")
    print("Saved stonehenge_medium.npz and stonehenge_geometry.json")


if __name__ == '__main__':
    main()
