# Minimal HyperOptimizer trial image (smoke test).
# Contract: CLI --hpo-<slug>=...  →  stdout hpo.metrics.<name>=...
FROM python:3.15-slim
WORKDIR /app
COPY trial.py network_probe.py ./
USER 1000:1000
ENTRYPOINT ["python", "/app/trial.py"]
