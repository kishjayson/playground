# Fleet MCP

Runs Fleet's official MCP server through an OpenAI Secure MCP Tunnel. Tailscale provides network access to Fleet.

## Setup

### 1. Prepare

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/fleet-mcp
cp .env.example .env
```

### 2. Add Fleet connection

Add the Fleet URL and API-only user token to `.env`:

```dotenv
FLEET_BASE_URL=https://fleet.example.com
FLEET_API_KEY=<fleet-api-only-user-token>
```

Create the API-only user in Fleet under **Settings → Users → Create user**. Use Observer for read-only inventory or Observer Plus when live queries are required. See [Fleet API-only users](https://fleetdm.com/guides/fleetctl#using-fleetctl-with-an-api-only-user) and [Fleet MCP configuration](https://github.com/fleetdm/fleet/tree/main/cmd/fleet-mcp#configuration).

Generate the required Fleet MCP startup token:

```sh
openssl rand -hex 32
```

Add the result to `.env`:

```dotenv
MCP_AUTH_TOKEN=<generated-token>
```

### 3. Add Tailscale

Create an auth key at [Tailscale Admin Console → Keys](https://console.tailscale.com/admin/settings/keys), then add it to `.env`:

```dotenv
TS_AUTHKEY=<tailscale-auth-key>
TS_HOSTNAME=fleet-mcp
```

See [Tailscale auth keys](https://tailscale.com/docs/features/access-control/auth-keys).

### 4. Add Secure MCP Tunnel

Create the tunnel at [OpenAI Platform → Tunnels](https://platform.openai.com/settings/organization/tunnels). Associate it with the Platform organization and ChatGPT workspace that will use it.

Add the tunnel ID to `.env`:

```dotenv
CONTROL_PLANE_TUNNEL_ID=<tunnel-id>
```

Create a runtime API key at [OpenAI Platform → API keys](https://platform.openai.com/api-keys) with **Tunnels Read + Use**, then add it:

```dotenv
CONTROL_PLANE_API_KEY=<openai-runtime-api-key>
```

See [OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels).

Leave `FLEET_MCP_REF` and `TUNNEL_CLIENT_REF` at the committed values unless intentionally upgrading either upstream component.

### 5. Build and start

```sh
docker compose build --pull --no-cache
docker compose up -d --force-recreate --remove-orphans
```

### 6. Check

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

### 7. Add to ChatGPT

Open [ChatGPT Plugins](https://chatgpt.com/plugins) and create a developer-mode app. See [Developer mode and MCP apps in ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt).

Use:

```text
Connection:     Tunnel
Tunnel:         fleet-mcp
Authentication: No Auth
```

Verification prompt:

```text
fleet-mcp How many systems are enrolled in Fleet?
```
