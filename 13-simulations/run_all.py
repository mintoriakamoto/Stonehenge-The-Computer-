#!/usr/bin/env python3
"""
RUN_ALL.py
Executes all analyses in sequence, saves all outputs.
"""

import subprocess
import sys
import os

scripts = [
    ('Aubrey Register Simulation', 'aubrey_register.py'),
    ('Knowledge Decay Model', 'knowledge_decay.py'),
    ('Isotope Network Analysis', 'isotope_network.py'),
    ('Sacred Rod Audit', 'sacred_rod_audit.py'),
]

print("="*60)
print("EXECUTING COMPLETE STONEHENGE ANALYSIS SUITE")
print("="*60)

for name, script in scripts:
    if os.path.exists(script):
        print(f"\n{'='*60}")
        print(f"RUNNING: {name}")
        print(f"{'='*60}")
        try:
            result = subprocess.run([sys.executable, script],
                                  capture_output=True, text=True, timeout=300)
            print(result.stdout)
            if result.stderr:
                print(f"STDERR: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT: {name} exceeded 5 minutes")
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        print(f"\nSKIP: {script} not found")

print("\n" + "="*60)
print("ALL ANALYSES COMPLETE")
print("="*60)
print("Generated files:")
for f in os.listdir('.'):
    if f.endswith('.json') or f.endswith('.npz') or f.endswith('.py'):
        print(f"  {f}")

if __name__ == "__main__":
    print("="*60)
    print("EXECUTING COMPLETE STONEHENGE ANALYSIS SUITE")
    print("="*60)

    for name, script in scripts:
        if os.path.exists(script):
            print(f"\n{'='*60}")
            print(f"RUNNING: {name}")
            print(f"{'='*60}")
            try:
                result = subprocess.run([sys.executable, script],
                                      capture_output=True, text=True, timeout=300)
                print(result.stdout)
                if result.stderr:
                    print(f"STDERR: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"TIMEOUT: {name} exceeded 5 minutes")
            except Exception as e:
                print(f"ERROR: {e}")
        else:
            print(f"\nSKIP: {script} not found")

    print("\n" + "="*60)
    print("ALL ANALYSES COMPLETE")
    print("="*60)
    print("Generated files:")
    for f in os.listdir('.'):
        if f.endswith('.json') or f.endswith('.npz') or f.endswith('.py'):
            print(f"  {f}")

if __name__ == '__main__':
    pass
