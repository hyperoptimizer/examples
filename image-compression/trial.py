"""One offline WebP evaluation; the optimizer lives outside this container."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity

FLOOR = 0.95


def objective(output_bytes: int, source_bytes: int, minimum_ssim: float) -> float:
    if minimum_ssim < FLOOR:
        return 1 + FLOOR - minimum_ssim
    return output_bytes / (output_bytes + source_bytes)


def evaluate(quality: int, method: int, split: str = "tuning", output: Path | None = None) -> dict:
    if not 50 <= quality <= 100 or not 0 <= method <= 6:
        raise ValueError("quality must be 50..100 and method 0..6")
    root = Path(__file__).parent / "dataset"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    records = [entry for entry in manifest if entry["split"] == split]
    if not records:
        raise ValueError("empty or unknown dataset split")
    if output is not None:
        output.mkdir(parents=True, exist_ok=True)
    rows = []
    for entry in records:
        path = root / entry["file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"dataset checksum mismatch: {path.name}")
        with Image.open(path) as source:
            image = source.convert("RGB")
        pixels = np.asarray(image)
        encoded = io.BytesIO()
        start = time.perf_counter()
        image.save(encoded, format="WEBP", quality=quality, method=method)
        seconds = time.perf_counter() - start
        with Image.open(io.BytesIO(encoded.getvalue())) as decoded:
            restored = decoded.convert("RGB")
            similarity = float(structural_similarity(pixels, np.asarray(restored), data_range=255, channel_axis=2))
            if output is not None:
                (output / f"{path.stem}.webp").write_bytes(encoded.getvalue())
                comparison = Image.new("RGB", (image.width * 2, image.height))
                comparison.paste(image, (0, 0))
                comparison.paste(restored, (image.width, 0))
                comparison.save(output / f"{path.stem}-comparison.png")
        rows.append({"file": path.name, "ssim": similarity, "bytes": len(encoded.getvalue()), "source_rgb_bytes": pixels.nbytes, "encoding_seconds": seconds})
    minimum = min(row["ssim"] for row in rows)
    size = sum(row["bytes"] for row in rows)
    raw = sum(row["source_rgb_bytes"] for row in rows)
    return {"quality": quality, "method": method, "split": split, "compression_loss": objective(size, raw, minimum), "total_bytes": size, "minimum_ssim": minimum, "mean_ssim": sum(row["ssim"] for row in rows) / len(rows), "encoding_seconds": sum(row["encoding_seconds"] for row in rows), "quality_pass": minimum >= FLOOR, "images": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hpo-quality", type=int, default=80)
    parser.add_argument("--hpo-method", type=int, default=4)
    parser.add_argument("--split", choices=["tuning", "holdout"], default="tuning")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate(args.hpo_quality, args.hpo_method, args.split, args.output)
    for name in ["total_bytes", "minimum_ssim", "mean_ssim", "encoding_seconds", "quality_pass", "compression_loss"]:
        print(f"hpo.metrics.{name}={json.dumps(report[name], allow_nan=False)}", flush=True)
    if args.output is not None:
        (args.output / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")


if __name__ == "__main__":
    main()
