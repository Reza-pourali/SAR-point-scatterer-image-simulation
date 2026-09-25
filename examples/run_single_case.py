"""Run one configurable SAR point-scatterer simulation."""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sar_scatterer_sim.model import CASES, image_statistics, simulate_image
from sar_scatterer_sim.plotting import save_image_pair


def parse_args():
    p = argparse.ArgumentParser(description="Run one SAR simulation case.")
    p.add_argument("--case", choices=sorted(CASES), default="case1")
    p.add_argument("--amplitude", choices=["fixed", "random"], default="fixed")
    p.add_argument("--rows", type=int, default=300)
    p.add_argument("--cols", type=int, default=300)
    p.add_argument("--scatterers", type=int, default=100)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output-dir", default="outputs")
    return p.parse_args()


def main():
    args = parse_args()
    amplitude, phase = simulate_image(
        case=args.case,
        amplitude_mode=args.amplitude,
        rows=args.rows,
        cols=args.cols,
        n_scatterers=args.scatterers,
        seed=args.seed,
    )
    cfg = CASES[args.case]
    prefix = f"{args.case}_{args.amplitude}"
    save_image_pair(
        amplitude,
        phase,
        args.output_dir,
        prefix,
        f"{cfg.name} | {args.amplitude.capitalize()} scatterer amplitude",
    )
    print(image_statistics(amplitude, phase))


if __name__ == "__main__":
    main()
