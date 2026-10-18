FROM golang:1.26.5-alpine AS fleet-mcp-build

RUN apk add --no-cache ca-certificates git

ARG FLEET_REF=f9eb61c4d789d11a8cb08b6ca974e17a7686beb7

WORKDIR /src/fleet

RUN git init \
    && git remote add origin https://github.com/fleetdm/fleet.git \
    && git sparse-checkout init --cone \
    && git sparse-checkout set cmd/fleet-mcp \
    && git fetch --depth 1 origin "${FLEET_REF}" \
    && git checkout --detach FETCH_HEAD

WORKDIR /src/fleet/cmd/fleet-mcp

RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/fleet-mcp .

FROM golang:1.26.5-alpine AS tunnel-client-build

RUN apk add --no-cache ca-certificates git

ARG TUNNEL_CLIENT_REF=105e17a79a36e4e5c897fd698ed2b8dbf935b144

WORKDIR /src/tunnel-client

RUN git init \
    && git remote add origin https://github.com/openai/tunnel-client.git \
    && git fetch --depth 1 origin "${TUNNEL_CLIENT_REF}" \
    && git checkout --detach FETCH_HEAD

RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/tunnel-client ./cmd/client

FROM alpine:3.24

RUN apk add --no-cache ca-certificates

COPY --from=fleet-mcp-build /out/fleet-mcp /usr/local/bin/fleet-mcp
COPY --from=tunnel-client-build /out/tunnel-client /usr/local/bin/tunnel-client

ENTRYPOINT ["/usr/local/bin/tunnel-client", "run"]
