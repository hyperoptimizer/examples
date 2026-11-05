FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir hyperoptimizer==0.1.0
COPY train.py network_probe.py ./
USER 1000:1000
ENTRYPOINT ["python", "/app/train.py"]
