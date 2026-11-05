FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY trial.py ./
COPY dataset/ ./dataset/
USER 1000:1000
ENTRYPOINT ["python", "/app/trial.py"]
