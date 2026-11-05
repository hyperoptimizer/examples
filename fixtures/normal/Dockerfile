FROM node:22-alpine
WORKDIR /app
COPY workload.mjs ./
ENV ABUSE_FIXTURE_MODE=normal
USER node
ENTRYPOINT ["node", "/app/workload.mjs"]
