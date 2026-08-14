ARG TUNNEL_CLIENT_VERSION=v0.0.10

FROM golang:1.26.5-alpine AS fleet-mcp-build

RUN apk add --no-cache ca-certificates git

ARG FLEET_REF=main

WORKDIR /src/fleet

RUN git init \
    && git remote add origin https://github.com/fleetdm/fleet.git \
    && git sparse-checkout init --cone \
    && git sparse-checkout set cmd/fleet-mcp \
    && git fetch --depth 1 origin "${FLEET_REF}" \
    && git checkout --detach FETCH_HEAD

WORKDIR /src/fleet/cmd/fleet-mcp

RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/fleet-mcp .

FROM ghcr.io/openai/tunnel-client:${TUNNEL_CLIENT_VERSION}

COPY --from=fleet-mcp-build /out/fleet-mcp /usr/local/bin/fleet-mcp
