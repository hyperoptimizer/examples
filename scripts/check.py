"""Build and smoke-test images without platform credentials."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
IMAGES = {"trial-smoke": ("fixtures/trial-smoke", "Dockerfile"), "python-tracking": ("fixtures/python-tracking", "Dockerfile"), "normal": ("fixtures", "normal/Dockerfile"), "image-compression": ("image-compression", "Dockerfile")}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", choices=list(IMAGES))
    args = parser.parse_args()
    run("node", "--test", "fixtures/workload.test.mjs")
    for name, (context, dockerfile) in IMAGES.items():
        if args.image is not None and name != args.image:
            continue
        tag = f"hpo-examples/{name}:check"
        print(run("docker", "build", "--platform", "linux/amd64", "-t", tag, "-f", f"{context}/{dockerfile}", context))
        user = run("docker", "image", "inspect", tag, "--format", "{{.Config.User}}").strip()
        if user in ["", "0", "root", "0:0"]:
            raise RuntimeError(f"root user: {name}")
        run_args = ["--help"] if name == "python-tracking" else (["--hpo-duration-seconds=0.2"] if name == "normal" else ["--hpo-duration-seconds=0.2", "--hpo-x=0.5"] if name == "trial-smoke" else [])
        text = run("docker", "run", "--rm", "--platform", "linux/amd64", "--network=none", "--memory=512m", "--cpus=1", tag, *run_args)
        if name != "python-tracking":
            metrics = {line.split("=", 1)[0]: json.loads(line.split("=", 1)[1]) for line in text.splitlines() if line.startswith("hpo.metrics.")}
            if not metrics:
                raise RuntimeError(f"no metrics: {name}")
        print(text[-2000:])
    if args.image not in [None, "image-compression"]:
        return
    print(run("docker", "run", "--rm", "--platform", "linux/amd64", "--network=none", "--entrypoint", "python", "hpo-examples/image-compression:check", "-c", "from trial import evaluate; assert evaluate(100,6)['minimum_ssim'] > evaluate(50,0)['minimum_ssim']"))


if __name__ == "__main__":
    main()
