"""Stonehenge Reverse Engineering Package"""

from .aubrey_register import AubreyRegister
from .knowledge_decay import KnowledgeDecayModel
from .isotope_network import build_network, analyze, simulate_feasting
from .sacred_rod_audit import sacred_rod_audit
from .altar_stone_predictions import generate_altar_stone_predictions
from .chamber_fdtD import generate_stonehenge_geometry
from .master_report import generate_master_report

__version__ = '1.0.0'
__author__ = 'V3R1T4S'
__all__ = [
    'AubreyRegister',
    'KnowledgeDecayModel',
    'build_network',
    'analyze',
    'simulate_feasting',
    'sacred_rod_audit',
    'generate_altar_stone_predictions',
    'generate_stonehenge_geometry',
    'generate_master_report',
]
