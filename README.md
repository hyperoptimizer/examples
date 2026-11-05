# Hyperoptimizer examples

Public Docker workloads for [Hyperoptimizer](https://hyperoptimizer.com).

Start with [image compression](image-compression/README.md): optimize real WebP output sizes while enforcing a measured image-quality floor. [Test fixtures](fixtures/README.md) are separate from this tutorial.

## CI and releases

Pull requests build and run every container offline as a non-root user. Releases repeat those checks before publishing linux/amd64 images to `ghcr.io/hyperoptimizer/examples/<name>:<version>` and `:sha-<full-commit>`. Download digest artifacts from the workflow; consumers must record `image@sha256:...`, not mutable tags. Public repository visibility does not automatically make GHCR packages public: set each package's visibility to Public after its first release and verify anonymous pulls.

The tracking image installs the public `hyperoptimizer==0.1.0` package from PyPI; no private SDK checkout is used in public CI.

Code: MIT. Bundled photographs retain their individual public-domain/CC0 terms; see the dataset manifest and attribution.

Release v0.1.0 was published successfully. Immutable references are in [images.lock.json](images.lock.json). Each GHCR package needs Public visibility for anonymous pulls; building from public source and installing the public SDK work independently.
