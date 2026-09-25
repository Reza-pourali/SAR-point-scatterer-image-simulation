"""Generate all six fixed/random-amplitude SAR simulation cases."""

from pathlib import Path
import argparse
import csv
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sar_scatterer_sim.model import CASES, image_statistics, simulate_image
from sar_scatterer_sim.plotting import save_image_pair


def parse_args():
    p = argparse.ArgumentParser(description="Simulate all SAR point-scatterer cases.")
    p.add_argument("--rows", type=int, default=300)
    p.add_argument("--cols", type=int, default=300)
    p.add_argument("--scatterers", type=int, default=100)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output-dir", default="outputs")
    return p.parse_args()


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []

    for case_key, cfg in CASES.items():
        for amplitude_mode in ("fixed", "random"):
            # Distinct deterministic seeds keep every case reproducible while
            # avoiding identical random streams across configurations.
            local_seed = args.seed + 100 * int(case_key[-1]) + (1 if amplitude_mode == "random" else 0)
            amplitude, phase = simulate_image(
                case=case_key,
                amplitude_mode=amplitude_mode,
                rows=args.rows,
                cols=args.cols,
                n_scatterers=args.scatterers,
                seed=local_seed,
            )
            prefix = f"{case_key}_{amplitude_mode}_amplitude"
            title = f"{cfg.name} | {amplitude_mode.capitalize()} scatterer amplitude"
            save_image_pair(amplitude, phase, output_dir, prefix, title)

            stats = image_statistics(amplitude, phase)
            rows.append({
                "case": case_key,
                "amplitude_mode": amplitude_mode,
                "phase_half_range_rad": cfg.phase_half_range,
                **stats,
            })

    with (output_dir / "simulation_statistics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} reproducible configurations in {output_dir}")


if __name__ == "__main__":
    main()
