# Smaller website images with a quality floor

A single container evaluates quality (50–100) and method (0–6), then prints finite stdout metrics and exits. It needs no SDK or runtime network access. The fixed RGB PNG sources contain no retained metadata. SSIM is measured against the same pixels at unchanged dimensions, per RGB channel, with data_range=255. Require minimum SSIM >= 0.95 across all images.

`compression_loss` is bytes/(bytes+source RGB bytes) when quality passes, otherwise 1+(0.95-minimum SSIM). Every passing configuration ranks before every violation. A quality violation is a valid measurement; corrupt input or execution failure exits nonzero without a score.

## Local baseline

```sh
docker build --platform linux/amd64 -t hpo-compression:local image-compression
docker run --rm --network=none --memory=512m --cpus=1 hpo-compression:local --hpo-quality=80 --hpo-method=4
```

## Managed optimization

Install and authenticate the HPO CLI, select a project with compute allowance, then run from this repository:

```sh
hpo --config image-compression/hpo.toml optimize --project YOUR_PROJECT_ID --detach
```

The build block builds and pushes into your workspace registry. Starter/Pro should use this route rather than assume public GHCR images are selectable. The configuration uses Bayesian TPE, 32 trials, seed 42, one concurrent trial, Nano and a 180-second timeout. Verify runtime and memory suitability on one managed trial before the full search. No managed performance claim is made by local tests.

## Reproduce local search and export comparisons

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r image-compression/requirements-dev.lock
cd image-compression
../.venv/bin/python benchmark.py
```

The 32-trial local Optuna TPE search tunes on astronaut, coffee, cat and rocket images, then evaluates the selected settings once on the fresh held-out camera photograph. It writes `results/benchmark.json`, encoded files, and comparisons (source left, reconstruction right). `trial.py --split holdout --hpo-quality=VALUE --hpo-method=VALUE --output results/replay` reproduces a selected configuration without optimizing again.

The baseline is quality=80/method=4. Check its quality-pass flag before calling byte reductions equivalent-quality savings. This tiny corpus illustrates the workflow; test your own representative website imagery before applying the result. Compare the images visually as well as inspecting SSIM. Timing is diagnostic and is not optimized. Local evidence records no managed run ID or published image digest until one actually exists.

The exploratory benchmark used rocket as a holdout and failed its quality floor. It is preserved in `exploratory-benchmark.json`. The final split includes rocket in tuning and uses a fresh camera image for holdout; this is a small demonstration, not a generalization guarantee.
