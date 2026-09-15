FROM node:16-alpine AS build
ENV NODE_ENV=development
ENV NODE_OPTIONS=--max-old-space-size=2048
RUN apk add --no-cache python3 make gcc g++
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --network-timeout 120000
COPY . .
RUN yarn build

FROM node:16-alpine
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=8080
WORKDIR /app
COPY --from=build --chown=node:node /app /app
USER node
