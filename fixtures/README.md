# Portable test fixtures

These workloads preserve the Hyperoptimizer services trial contract. They are not production applications.

* `trial-smoke`: dependency-free Python objective and bounded network probes.
* `python-tracking`: SDK reporting example; requires public `hyperoptimizer==0.1.0`. `--help` checks installation offline; a complete tracking run requires the platform.
* `normal` and `flood`: Rosenbrock objective with bounded runtime/output. Run `node --test fixtures/workload.test.mjs`. Build both with `node fixtures/build-images.mjs`.

Database, billing, Hatchet and Kubernetes acceptance drivers stay in the private services repository. Network probes test actual cluster policy only when run in that environment with verified positive controls. Public offline smoke tests do not establish tenant isolation.

Container build contexts: each Python fixture directory separately; `fixtures/` for normal/flood. The matching hpo.toml files support CLI builds into a workspace registry. Never run flood fixtures in customer workspaces.
