FROM node:26-alpine
WORKDIR /app
COPY workload.mjs ./
USER node
ENTRYPOINT ["node", "/app/workload.mjs"]
