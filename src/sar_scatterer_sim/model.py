"""Core point-scatterer SAR simulation model.

Each image pixel is modeled as the coherent sum of N complex point
scatterers:

    S = sum_i A_i exp(j phi_i)

The output amplitude is |S| and the output phase is arg(S).
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class CaseConfig:
    name: str
    phase_half_range: float
    description: str


CASES = {
    "case1": CaseConfig(
        name="Case 1 - Full phase range",
        phase_half_range=float(np.pi),
        description="Uniform phase in [-pi, pi].",
    ),
    "case2": CaseConfig(
        name="Case 2 - Narrow phase range",
        phase_half_range=float(np.pi / 5.0),
        description="Uniform phase in [-pi/5, pi/5].",
    ),
    "case3": CaseConfig(
        name="Case 3 - Medium phase range",
        phase_half_range=float(2.0 * np.pi / 5.0),
        description="Uniform phase in [-2pi/5, 2pi/5].",
    ),
}


def _validate(rows, cols, n_scatterers, amplitude_mode, chunk_rows):
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive integers.")
    if n_scatterers <= 0:
        raise ValueError("n_scatterers must be positive.")
    if amplitude_mode not in {"fixed", "random"}:
        raise ValueError("amplitude_mode must be 'fixed' or 'random'.")
    if chunk_rows <= 0:
        raise ValueError("chunk_rows must be positive.")


def simulate_image(
    case="case1",
    amplitude_mode="fixed",
    rows=300,
    cols=300,
    n_scatterers=100,
    seed=42,
    chunk_rows=25,
):
    """Simulate amplitude and phase images from independent point scatterers.

    The implementation is vectorized in row chunks. This keeps the original
    300 x 300 x 100 model while avoiding slow Python loops over every pixel.

    Parameters
    ----------
    case:
        One of ``case1``, ``case2``, or ``case3``.
    amplitude_mode:
        ``fixed`` uses A_i = 1. ``random`` uses A_i ~ Uniform(0, 1).
    seed:
        NumPy random seed for exact reproducibility.
    """
    if case not in CASES:
        raise ValueError(f"Unknown case: {case}. Expected one of {sorted(CASES)}")
    _validate(rows, cols, n_scatterers, amplitude_mode, chunk_rows)

    cfg = CASES[case]
    rng = np.random.default_rng(seed)
    amplitude = np.empty((rows, cols), dtype=np.float64)
    phase = np.empty((rows, cols), dtype=np.float64)

    for start in range(0, rows, chunk_rows):
        stop = min(start + chunk_rows, rows)
        shape = (stop - start, cols, n_scatterers)

        phases = rng.uniform(
            -cfg.phase_half_range,
            cfg.phase_half_range,
            size=shape,
        )

        if amplitude_mode == "fixed":
            amplitudes = 1.0
        else:
            amplitudes = rng.uniform(0.0, 1.0, size=shape)

        scatterers = amplitudes * np.exp(1j * phases)
        signal = np.sum(scatterers, axis=-1)
        amplitude[start:stop] = np.abs(signal)
        phase[start:stop] = np.angle(signal)

    return amplitude, phase


def theoretical_coherent_component(case="case1", amplitude_mode="fixed", n_scatterers=100):
    """Return the magnitude of the mean coherent complex component.

    For phi ~ Uniform(-a, a), E[exp(j phi)] = sin(a) / a.
    This quantity is not the same as E[|S|], especially in the fully random
    phase case, but it explains why narrower phase ranges produce larger
    coherent amplitudes.
    """
    if case not in CASES:
        raise ValueError(f"Unknown case: {case}")
    if amplitude_mode not in {"fixed", "random"}:
        raise ValueError("amplitude_mode must be 'fixed' or 'random'.")

    a = CASES[case].phase_half_range
    phase_mean = 1.0 if a == 0 else np.sin(a) / a
    amp_mean = 1.0 if amplitude_mode == "fixed" else 0.5
    return float(abs(n_scatterers * amp_mean * phase_mean))


def image_statistics(amplitude, phase):
    """Return compact numerical summaries for one simulated image pair."""
    amplitude = np.asarray(amplitude, dtype=np.float64)
    phase = np.asarray(phase, dtype=np.float64)
    if amplitude.shape != phase.shape:
        raise ValueError("amplitude and phase images must have matching shapes.")

    phase_resultant = abs(np.mean(np.exp(1j * phase)))
    return {
        "amplitude_mean": float(amplitude.mean()),
        "amplitude_std": float(amplitude.std()),
        "amplitude_min": float(amplitude.min()),
        "amplitude_max": float(amplitude.max()),
        "phase_mean_resultant_length": float(phase_resultant),
    }
