"""Run externally with project/experiment configuration, or as an SDK-managed trial."""

import argparse
import os

from hyperoptimizer import Run
from hyperoptimizer.types import Histogram

parser = argparse.ArgumentParser()
parser.add_argument("--hpo-network-probe", choices=["offline", "paid", "observe"])
parser.add_argument("--hpo-network-peer")
parser.add_argument("--hpo-network-internal-api")
parser.add_argument("--hpo-network-kubernetes-api")
parser.add_argument("--hpo-network-node")
args, _assigned_parameters = parser.parse_known_args()

kwargs = (
    {}
    if os.environ.get("HYPEROPTIMIZER_TRACKING_URL")
    else {"experiment_name": "python-tracking-demo"}
)
with Run(**kwargs) as run:
    if args.hpo_network_probe is not None:
        from network_probe import probe_network

        probe_network(
            args.hpo_network_probe,
            args.hpo_network_peer,
            internal_api_ip=args.hpo_network_internal_api,
            kubernetes_api_ip=args.hpo_network_kubernetes_api,
            node_ip=args.hpo_network_node,
            require_tracking=True,
        )
    run.log_configs({"dataset/version": "v1"})
    for step in range(5):
        run.log_metrics({"score": step / 5, "metrics/loss": 1 / (step + 1)}, step=step)
        run.log_histograms({"layers/1/activations": Histogram([0, 1, 2], [step + 1, 5])}, step=step)
    run.add_tags(["smoke-test"])
    run.add_tags(["python-demo"], group_tags=True)
    print(run.get_run_url())
