# Fleet MCP

Docker Compose deployment of Fleet's official `cmd/fleet-mcp` connected to ChatGPT through OpenAI Secure MCP Tunnel.

The deployment keeps Fleet MCP private. `tunnel-client` maintains an outbound HTTPS connection to OpenAI and launches Fleet MCP locally over stdio. A Tailscale sidecar remains present so Fleet MCP can reach the Fleet server over the tailnet.

```text
ChatGPT
  ↓
OpenAI Secure MCP Tunnel
  ↓ outbound HTTPS
`tunnel-client`
  ↓ stdio
Fleet MCP
  ↓ Tailscale
Fleet
```

## Configure

Copy `.env.example` to `.env` and provide:

- `CONTROL_PLANE_TUNNEL_ID`: the tunnel ID from OpenAI Platform > Tunnels.
- `CONTROL_PLANE_API_KEY`: a runtime API key with Tunnels Read + Use.
- `FLEET_API_KEY`: token for a Fleet API-only user.
- `MCP_AUTH_TOKEN`: required by Fleet MCP at startup even in stdio mode.
- `TS_AUTHKEY`: auth key for the independent `fleet-mcp` Tailscale node.

`FLEET_BASE_URL` defaults to the existing Fleet tailnet URL.

The OpenAI runtime key and the Fleet API key are separate credentials with separate responsibilities. An OpenAI admin key is not required by this deployment.

## Build

While testing `FLEET_MCP_REF=main`, rebuild without cache when you want to pick up new upstream Fleet changes:

```sh
docker compose build --pull --no-cache
```

The runtime image is based on OpenAI's published `ghcr.io/openai/tunnel-client` image. `TUNNEL_CLIENT_VERSION` defaults to the current pinned stable version in `.env.example`.

## Migrate from the Funnel prototype

The earlier test deployment exposed Fleet MCP through Tailscale Serve/Funnel. Tailscale service configuration can persist in the node state, so clear it explicitly before recreating the updated deployment:

```sh
docker compose exec tailscale tailscale funnel reset
docker compose exec tailscale tailscale serve reset
```

These are native Tailscale reset commands. The updated Compose file does not configure Serve or Funnel.

## Run

```sh
docker compose up -d --force-recreate
```

## Inspect

```sh
docker compose ps
docker compose logs -f tunnel-client
```

`tunnel-client` exposes its operator health surface only inside the shared container network namespace. Check readiness with:

```sh
docker compose exec tunnel-client \
  wget -qO- http://127.0.0.1:8080/readyz
```

A successful readiness response means the tunnel runtime and its configured MCP binding are ready for connector traffic.

## ChatGPT

In ChatGPT Developer mode, create the plugin using:

```text
Connection:     Tunnel
Tunnel:         fleet-mcp
Authentication: No Auth
```

`No Auth` here means there is no additional end-user OAuth layer on the MCP server. The tunnel daemon authenticates to OpenAI with `CONTROL_PLANE_API_KEY`, while Fleet MCP authenticates to Fleet with `FLEET_API_KEY`.

Fleet MCP runs as:

```text
/usr/local/bin/fleet-mcp -transport stdio
```

The OpenAI tunnel client launches that command directly and communicates with it over stdin/stdout. Fleet MCP's HTTP bearer middleware is therefore not part of this path, although Fleet MCP still requires `MCP_AUTH_TOKEN` to be present at startup.

## Source

The Dockerfile fetches Fleet's official repository and builds `cmd/fleet-mcp` directly. No Fleet MCP source is copied into this directory.

`FLEET_MCP_REF` controls the upstream Fleet revision used for the build. Once testing is complete, pin it to the upstream revision you want to preserve.
