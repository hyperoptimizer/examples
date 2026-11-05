# Portable test fixtures

* `trial-smoke`: dependency-free Python objective and bounded network probes.
* `python-tracking`: Python SDK reporting using the public pinned package. `--help` checks installation offline; full reporting requires the platform.
* `normal`: a bounded Rosenbrock objective that emits numeric loss metrics.

Run `node --test fixtures/workload.test.mjs`. Build normal using `node fixtures/build-images.mjs`. The Python fixtures use their own directory as the Docker build context; normal uses `fixtures/`.

Database, billing and Kubernetes acceptance orchestration lives in the private services repository. Public tests do not establish cluster isolation.
