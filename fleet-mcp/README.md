# Fleet MCP

Local Docker Compose deployment of Fleet's official `cmd/fleet-mcp` service with its own Tailscale identity.

## Configure

Copy `.env.example` to `.env` and provide:

- `FLEET_API_KEY`: token for a Fleet API-only user.
- `MCP_AUTH_TOKEN`: bearer token used by MCP clients.
- `TS_AUTHKEY`: auth key for the independent `fleet-mcp` Tailscale node.

`FLEET_BASE_URL` defaults to the existing Fleet tailnet URL.

## Build

While testing `FLEET_MCP_REF=main`, rebuild without cache when you want to pick up new upstream Fleet changes:

```sh
docker compose build --pull --no-cache
```

## Run

```sh
docker compose up -d --force-recreate
```

## Inspect

```sh
docker compose ps
docker compose logs -f fleet-mcp
```

Fleet MCP is exposed over the tailnet at:

```text
https://fleet-mcp.tail2bebc3.ts.net/sse
```

The deployment does not enable Tailscale Funnel.

## Source

The Dockerfile fetches Fleet's official repository and builds `cmd/fleet-mcp` directly.

`FLEET_MCP_REF` controls the upstream revision used for the build. No Fleet MCP source is copied into this directory.

Once testing is complete, pin `FLEET_MCP_REF` to the upstream revision you want to preserve.
