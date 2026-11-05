#!/usr/bin/env python3
"""Smoke-test trial for HyperOptimizer local MVP.

Accepts --hpo-* flags from the k8s worker and prints hpo.metrics.* lines
that Vector (when enabled) or a manual metrics POST can ingest.

Platform-injected env vars: HYPEROPTIMIZER_TRIAL_ID, HYPEROPTIMIZER_EXPERIMENT_ID,
HYPEROPTIMIZER_ORG_ID.
"""

from __future__ import annotations

import argparse
import math
import os
import time


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hpo-x", type=float, required=True)
    parser.add_argument("--hpo-y", type=float, default=0.0)
    parser.add_argument("--hpo-duration-seconds", type=float, default=2.0)
    parser.add_argument("--hpo-report-interval-seconds", type=float, default=5.0)
    parser.add_argument("--hpo-network-probe", choices=["offline", "paid", "observe"])
    parser.add_argument("--hpo-network-peer")
    args, _unknown = parser.parse_known_args()
    if not 0 <= args.hpo_duration_seconds <= 600:
        parser.error("duration must be between 0 and 600 seconds")
    if args.hpo_report_interval_seconds <= 0:
        parser.error("report interval must be positive")

    trial_id = os.environ.get("HYPEROPTIMIZER_TRIAL_ID", "?")
    print(f"trial_id={trial_id} x={args.hpo_x} y={args.hpo_y}", flush=True)

    # Cheap synthetic objective: maximize score around (x,y)=(0.5, 0.25)
    score = 1.0 / (1.0 + (args.hpo_x - 0.5) ** 2 + (args.hpo_y - 0.25) ** 2)
    loss = -math.log(max(score, 1e-9))

    # Emit immediately and periodically so cancellation/exhaustion tests also
    # exercise objective collection before the container terminates.
    deadline = time.monotonic() + args.hpo_duration_seconds
    next_probe = 0.0
    while True:
        print(f"hpo.metrics.score={score:.8f}", flush=True)
        print(f"hpo.metrics.loss={loss:.8f}", flush=True)
        if args.hpo_network_probe is not None and time.monotonic() >= next_probe:
            from network_probe import probe_network

            probe_network(args.hpo_network_probe, args.hpo_network_peer)
            next_probe = time.monotonic() + 30
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(args.hpo_report_interval_seconds, remaining))


if __name__ == "__main__":
    main()
