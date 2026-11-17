FROM node:24.11.1-bookworm-slim
WORKDIR /app
COPY package*.json ./
COPY packages ./packages
COPY infra ./infra
RUN npm ci --ignore-scripts
CMD ["node", "infra/plc.mjs"]
