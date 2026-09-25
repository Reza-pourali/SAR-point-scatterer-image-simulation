"""Plotting helpers for simulated SAR amplitude and phase images."""

from pathlib import Path
import matplotlib.pyplot as plt


def save_image_pair(amplitude, phase, output_dir, prefix, title):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    amp_path = output_dir / f"{prefix}_amplitude.png"
    phase_path = output_dir / f"{prefix}_phase.png"

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(amplitude, cmap="gray")
    ax.set_title(f"{title} - Amplitude")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    fig.colorbar(im, ax=ax, label="Amplitude")
    fig.tight_layout()
    fig.savefig(amp_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(phase, cmap="twilight", vmin=-3.141592653589793, vmax=3.141592653589793)
    ax.set_title(f"{title} - Phase")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    fig.colorbar(im, ax=ax, label="Phase (rad)")
    fig.tight_layout()
    fig.savefig(phase_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return amp_path, phase_path
