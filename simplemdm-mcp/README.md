# SimpleMDM MCP

Runs a read-only SimpleMDM MCP server through an OpenAI Secure MCP Tunnel.

## Setup

### 1. Prepare

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/simplemdm-mcp
cp .env.example .env
```

### 2. Add SimpleMDM connection

Add the SimpleMDM API key to `.env`:

```dotenv
SIMPLEMDM_BASE_URL=https://a.simplemdm.com/api/v1
SIMPLEMDM_API_KEY=<simplemdm-api-key>
```

Create the API key in SimpleMDM under **Settings → API**. See [SimpleMDM API](https://api.simplemdm.com/v1).

### 3. Add Secure MCP Tunnel

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

Leave `TUNNEL_CLIENT_REF` at the committed value unless intentionally upgrading the upstream component.

### 4. Build and start

```sh
docker compose build --pull --no-cache
docker compose up -d --force-recreate --remove-orphans
```

### 5. Check

```sh
docker compose ps
docker compose logs -f simplemdm-mcp
```

Check tunnel readiness:

```sh
docker compose exec simplemdm-mcp wget -qO- http://127.0.0.1:8080/readyz
```

Expected response:

```text
ready
```

### 6. Add to ChatGPT

Open [ChatGPT Plugins](https://chatgpt.com/plugins) and create a developer-mode app. See [Developer mode and MCP apps in ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt).

Use:

```text
Connection:     Tunnel
Tunnel:         SimpleMDM MCP
Authentication: No Auth
```

Verification prompt:

```text
simplemdm-mcp How many devices are enrolled in SimpleMDM?
```
