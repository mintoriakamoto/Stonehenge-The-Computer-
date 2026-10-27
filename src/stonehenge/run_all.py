import importlib, os, sys

MODULES = [
    ('Aubrey Register', 'aubrey_register'),
    ('Knowledge Decay', 'knowledge_decay'),
    ('Isotope Network', 'isotope_network'),
    ('Sacred Rod Audit', 'sacred_rod_audit'),
    ('Altar Stone Predictions', 'altar_stone_predictions'),
    ('Precision Acoustics', 'acoustics_precision'),
    ('Master Report', 'master_report'),
]
# chamber_fdtD allocates ~2.2 GB of voxel arrays; run it on its own with stonehenge-fdtd.


def main():
    failed = []
    for name, module in MODULES:
        print(f"\n{'='*50}\nRUNNING: {name}\n{'='*50}")
        try:
            importlib.import_module(f'stonehenge.{module}').main()
        except Exception as e:
            print(f"FAILED: {name}: {e!r}")
            failed.append(name)
    print("\nGenerated files:")
    for f in sorted(os.listdir('.')):
        if f.endswith(('.json', '.md', '.npz')):
            print(f"  {f} ({os.path.getsize(f)} bytes)")
    if failed:
        sys.exit(f"{len(failed)} module(s) failed: {', '.join(failed)}")


if __name__ == '__main__':
    main()
