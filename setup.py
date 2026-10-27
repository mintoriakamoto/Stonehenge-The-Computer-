from setuptools import setup, find_packages

setup(
    name='stonehenge',
    version='1.0.0',
    description='Stonehenge reverse engineering: neurostimulation knowledge-transfer machine analysis',
    author='V3R1T4S',
    python_requires='>=3.8',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'networkx>=2.6',
        'scikit-learn>=1.0',
        'pandas>=1.3.0',
    ],
    entry_points={
        'console_scripts': [
            'stonehenge-aubrey=stonehenge.aubrey_register:main',
            'stonehenge-decay=stonehenge.knowledge_decay:main',
            'stonehenge-isotope=stonehenge.isotope_network:main',
            'stonehenge-rod=stonehenge.sacred_rod_audit:main',
            'stonehenge-altar=stonehenge.altar_stone_predictions:main',
            'stonehenge-fdtd=stonehenge.chamber_fdtD:main',
            'stonehenge-report=stonehenge.master_report:main',
            'stonehenge-acoustics=stonehenge.acoustics_precision:main',
            'stonehenge-chronology=stonehenge.chronology_crosscheck:main',
            'stonehenge-all=stonehenge.run_all:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
    ],
)
