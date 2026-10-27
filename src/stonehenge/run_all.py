import subprocess, sys, os

scripts = [
    ('Aubrey Register', 'AUBREY_REGISTER_FULL.py'),
    ('Knowledge Decay', 'KNOWLEDGE_DECAY_IT.py'),
    ('Isotope Network', 'ISOTOPE_NETWORK.py'),
    ('Sacred Rod Audit', 'SACRED_ROD_AUDIT.py'),
    ('Altar Stone Predictions', 'ALTAR_STONE_PREDICTIONS.py'),
    ('Chamber Geometry', 'CHAMBER_FDTD.py'),
    ('Master Report', 'MASTER_REPORT.py'),
]

print("Running all analyses...")
for name, script in scripts:
    if os.path.exists(script):
        print(f"\n{'='*50}\nRUNNING: {name}\n{'='*50}")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=120)
        print(result.stdout)
        if result.stderr: print(f"STDERR: {result.stderr}")
    else:
        print(f"SKIP: {script} not found")

print("\nGenerated files:")
for f in os.listdir('.'):
    if f.endswith(('.json', '.md', '.npz')):
        print(f"  {f} ({os.path.getsize(f)} bytes)")
