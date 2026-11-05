"""Opt-in network acceptance probes executed inside a real customer container."""

import ipaddress
import json
import os
import socket
import struct
import urllib.request
from urllib.parse import urlsplit

os.environ.setdefault("RES_OPTIONS", "timeout:1 attempts:1")


def tcp_connect(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.5):
            return True
    except OSError:
        return False


def alternate_dns() -> bool:
    labels = b"".join(bytes([len(part)]) + part.encode() for part in "pypi.org".split("."))
    query = struct.pack("!HHHHHH", 12345, 0x100, 1, 0, 0, 0) + labels + b"\x00\x00\x01\x00\x01"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1.5)
            sock.sendto(query, ("8.8.8.8", 53))
            return bool(sock.recv(2048))
    except OSError:
        return False


def probe_network(
    mode: str,
    peer_ip: str | None = None,
    *,
    internal_api_ip: str | None = None,
    kubernetes_api_ip: str | None = None,
    node_ip: str | None = None,
    require_tracking: bool = False,
) -> None:
    if require_tracking and any(
        value is None for value in (peer_ip, internal_api_ip, kubernetes_api_ip, node_ip)
    ):
        raise ValueError(
            "Tracking isolation requires explicit peer, internal API, Kubernetes API, and node IPs with positive controls"
        )
    for address in (peer_ip, internal_api_ip, kubernetes_api_ip, node_ip):
        if address is not None:
            ipaddress.ip_address(address)
    tracking_url = os.environ.get("HYPEROPTIMIZER_TRACKING_URL")
    tracking = None
    if tracking_url is not None:
        target = urlsplit(tracking_url)
        if (
            target.scheme not in {"http", "https"}
            or target.hostname is None
            or target.username
            or target.password
        ):
            raise ValueError("Invalid platform tracking URL")
        tracking = tcp_connect(
            target.hostname, target.port or (443 if target.scheme == "https" else 80)
        )
    if require_tracking and tracking is not True:
        raise RuntimeError("The dedicated tracking service is unreachable")
    try:
        socket.getaddrinfo("pypi.org", 443)
        dns = True
    except OSError:
        dns = False
    https = False
    if dns:
        try:
            with urllib.request.urlopen("https://pypi.org/simple/pip/", timeout=3) as response:
                https = response.status == 200
        except OSError:
            pass
    blocked = {
        "alternate_dns": alternate_dns(),
        "direct_public_ip": tcp_connect("1.1.1.1", 443),
        "alternate_port": tcp_connect("1.1.1.1", 80),
        "metadata": tcp_connect("169.254.169.254", 80),
        "kubernetes_api": tcp_connect(
            kubernetes_api_ip or os.environ.get("KUBERNETES_SERVICE_HOST", "10.96.0.1"), 443
        ),
        "node": tcp_connect(node_ip or "172.18.0.5", 10250),
        "public_ipv6": tcp_connect("2606:4700:4700::1111", 443),
    }
    if internal_api_ip is not None:
        blocked["internal_api"] = tcp_connect(internal_api_ip, 3002)
    if peer_ip is not None:
        blocked["other_workspace_peer"] = tcp_connect(peer_ip, 8080)
    print(
        "network_probe="
        + json.dumps({"mode": mode, "dns": dns, "https": https, "tracking": tracking, **blocked}),
        flush=True,
    )
    print(f"hpo.metrics.network_internet={int(https)}", flush=True)
    print(f"hpo.metrics.network_private_leaks={sum(blocked.values())}", flush=True)
    if any(blocked.values()):
        raise RuntimeError("A forbidden network destination was reachable")
    if mode == "offline" and (dns or https):
        raise RuntimeError("Trial internet access was unexpectedly available")
    if mode == "paid" and not (dns and https):
        raise RuntimeError("Paid allowlisted internet access was unavailable")
