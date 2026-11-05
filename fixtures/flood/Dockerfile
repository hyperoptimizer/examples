FROM node:22-alpine
WORKDIR /app
COPY workload.mjs ./
ENV ABUSE_FIXTURE_MODE=flood
USER node
ENTRYPOINT ["node", "/app/workload.mjs"]
