# SimpleMDM MCP

SimpleMDM MCP gives ChatGPT read-only access to SimpleMDM. Tailscale gives the service its own tailnet identity, and an OpenAI Secure MCP Tunnel carries the MCP connection to ChatGPT.

## Setup

### 1. Prepare

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/simplemdm-mcp
cp .env.example .env
```

### 2. Add SimpleMDM connection

Add your SimpleMDM API key to `.env`:

```dotenv
SIMPLEMDM_BASE_URL=https://a.simplemdm.com/api/v1
SIMPLEMDM_API_KEY=<simplemdm-api-key>
```

You can create an API key in SimpleMDM under **Settings → API**. See [SimpleMDM API](https://api.simplemdm.com/v1).

### 3. Add Tailscale

Create an auth key at [Tailscale Admin Console → Keys](https://console.tailscale.com/admin/settings/keys), then add it to `.env`:

```dotenv
TS_AUTHKEY=<tailscale-auth-key>
TS_HOSTNAME=simplemdm-mcp
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

The tunnel client is pinned in this repository. You normally don't need to change `TUNNEL_CLIENT_REF`.

### 5. Build and start

```sh
docker compose build --pull --no-cache
docker compose up -d --force-recreate --remove-orphans
```

### 6. Check

```sh
docker compose ps
docker compose logs -f simplemdm-mcp
```

To check that the tunnel is ready:

```sh
docker compose exec simplemdm-mcp wget -qO- http://127.0.0.1:8080/readyz
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
Tunnel:         SimpleMDM MCP
Authentication: No Auth
```

To verify the connection, ask:

```text
simplemdm-mcp How many devices are enrolled in SimpleMDM?
```
