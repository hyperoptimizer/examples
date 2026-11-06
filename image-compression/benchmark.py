"""Local TPE evidence; does not claim to exercise the managed platform."""

import hashlib
import importlib.metadata
import json
import platform
import uuid
from pathlib import Path

import optuna
from trial import evaluate


def main() -> None:
    output = Path("results")
    output.mkdir(exist_ok=True)
    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=42))

    def score(trial: optuna.Trial) -> float:
        report = evaluate(trial.suggest_int("quality", 50, 100), trial.suggest_int("method", 0, 6))
        trial.set_user_attr("report", report)
        return report["compression_loss"]

    study.optimize(score, n_trials=32)
    best = study.best_params
    reports = {}
    for split in ["tuning", "holdout"]:
        reports[split] = {
            "baseline": evaluate(80, 4, split, output / split / "baseline"),
            "high_quality_reference": evaluate(
                100, 4, split, output / split / "high-quality-reference"
            ),
            "selected": evaluate(
                best["quality"], best["method"], split, output / split / "selected"
            ),
        }
    report = {
        "run_id": str(uuid.uuid4()),
        "execution": "local-python",
        "managed_run_id": None,
        "image_digest": None,
        "python": platform.python_version(),
        "versions": {
            name: importlib.metadata.version(name)
            for name in ["Pillow", "numpy", "scikit-image", "optuna"]
        },
        "seed": 42,
        "trial_count": 32,
        "best_parameters": best,
        "dataset_manifest_sha256": hashlib.sha256(
            (Path(__file__).parent / "dataset/manifest.json").read_bytes()
        ).hexdigest(),
        "reports": reports,
        "trials": [{"number": t.number, "params": t.params, "loss": t.value} for t in study.trials],
    }
    (output / "benchmark.json").write_text(
        json.dumps(report, indent=2, allow_nan=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
