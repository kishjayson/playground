# Fleet MCP

Fleet MCP gives ChatGPT access to Fleet through Fleet's official MCP server. Tailscale provides network access to Fleet, and an OpenAI Secure MCP Tunnel carries the MCP connection to ChatGPT.

## Setup

### 1. Prepare

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/fleet-mcp
cp .env.example .env
```

### 2. Add Fleet connection

Add your Fleet URL and an API-only user token to `.env`:

```dotenv
FLEET_BASE_URL=https://fleet.example.com
FLEET_API_KEY=<fleet-api-only-user-token>
```

Create the API-only user in Fleet under **Settings → Users → Create user**. Use Observer for read-only inventory. Use Observer Plus if you want live queries. See [Fleet API-only users](https://fleetdm.com/guides/fleetctl#using-fleetctl-with-an-api-only-user) and [Fleet MCP configuration](https://github.com/fleetdm/fleet/tree/main/cmd/fleet-mcp#configuration).

Fleet MCP also requires a startup token. Generate one:

```sh
openssl rand -hex 32
```

Then add it to `.env`:

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

Create a tunnel at [OpenAI Platform → Tunnels](https://platform.openai.com/settings/organization/tunnels) and associate it with the Platform organization and ChatGPT workspace that will use it.

Add the tunnel ID to `.env`:

```dotenv
CONTROL_PLANE_TUNNEL_ID=<tunnel-id>
```

The tunnel also needs an OpenAI API key with **Tunnels Read + Use**. Create one at [OpenAI Platform → API keys](https://platform.openai.com/api-keys), then add it:

```dotenv
CONTROL_PLANE_API_KEY=<openai-runtime-api-key>
```

See [OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels).

The upstream Fleet MCP server and tunnel client are pinned in this repository. You normally don't need to change `FLEET_MCP_REF` or `TUNNEL_CLIENT_REF`.

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

To check that the tunnel is ready:

```sh
docker compose exec fleet-mcp wget -qO- http://127.0.0.1:8080/readyz
```

You should see:

```text
ready
```

### 7. Add to ChatGPT

Open [ChatGPT Plugins](https://chatgpt.com/plugins) and create a developer-mode app. See [Developer mode and MCP apps in ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt).

Use these settings:

```text
Connection:     Tunnel
Tunnel:         Fleet MCP
Authentication: No Auth
```

To verify the connection, ask:

```text
fleet-mcp How many systems are enrolled in Fleet?
```
