FROM golang:1.26.5-alpine AS tunnel-client-build

RUN apk add --no-cache ca-certificates git

ARG TUNNEL_CLIENT_REF=105e17a79a36e4e5c897fd698ed2b8dbf935b144

WORKDIR /src/tunnel-client

RUN git init \
    && git remote add origin https://github.com/openai/tunnel-client.git \
    && git fetch --depth 1 origin "${TUNNEL_CLIENT_REF}" \
    && git checkout --detach FETCH_HEAD

RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/tunnel-client ./cmd/client

FROM python:3.13-alpine

RUN apk add --no-cache ca-certificates

WORKDIR /app

COPY pyproject.toml README.md ./
COPY simplemdm_mcp ./simplemdm_mcp

RUN pip install --no-cache-dir .

COPY --from=tunnel-client-build /out/tunnel-client /usr/local/bin/tunnel-client

ENTRYPOINT ["/usr/local/bin/tunnel-client", "run"]
