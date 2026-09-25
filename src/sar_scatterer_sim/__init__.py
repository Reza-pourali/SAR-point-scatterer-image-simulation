"""Point-scatterer SAR image formation simulation."""

from .model import CaseConfig, CASES, simulate_image, theoretical_coherent_component

__all__ = [
    "CaseConfig",
    "CASES",
    "simulate_image",
    "theoretical_coherent_component",
]
