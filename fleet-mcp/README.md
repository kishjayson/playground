# Fleet MCP

```sh
cp .env.example .env
docker compose build --pull --no-cache
docker compose up -d --force-recreate --remove-orphans
```

```sh
docker compose ps
docker compose logs -f fleet-mcp
```

Check tunnel readiness:

```sh
docker compose exec fleet-mcp wget -qO- http://127.0.0.1:8080/readyz
```

Expected response:

```text
ready
```

ChatGPT plugin configuration:

```text
Connection:     Tunnel
Tunnel:         fleet-mcp
Authentication: No Auth
```

The Dockerfile builds Fleet's official `cmd/fleet-mcp` and OpenAI's `tunnel-client` directly from the revisions pinned in `.env.example`. The tunnel client launches Fleet MCP over stdio; the Tailscale sidecar provides Fleet-side tailnet reachability.
