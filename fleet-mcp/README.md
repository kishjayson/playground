# Fleet MCP

This is the bridge between ChatGPT and Fleet. It runs Fleet's official MCP server through an [OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels), while Tailscale gives the MCP process a private path back to Fleet.

If you already know what the variables mean, you can mostly fill in `.env` and keep moving. If you don't, the links below take you to the place where you create the value or to the documentation that explains it.

## 1. Clone the repository

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/fleet-mcp
cp .env.example .env
```

Keep real credentials in `.env`. The example file is only the configuration shape and the pinned upstream revisions.

## 2. Point Fleet MCP at Fleet

Set the URL Fleet MCP should use to reach Fleet:

```dotenv
FLEET_BASE_URL=https://fleet.example.com
```

In Fleet, go to **Settings → Users → Create user**, create an API-only user, then put its token in `.env`:

```dotenv
FLEET_API_KEY=<fleet-api-only-user-token>
```

Fleet explains API-only users in the [fleetctl guide](https://fleetdm.com/guides/fleetctl#using-fleetctl-with-an-api-only-user). The upstream [Fleet MCP configuration](https://github.com/fleetdm/fleet/tree/main/cmd/fleet-mcp#configuration) requires an API-only token. Use Observer for read-only inventory; use Observer+ if you want Fleet MCP to run live queries.

Fleet MCP also refuses to start without `MCP_AUTH_TOKEN`, even in stdio mode. Generate one:

```sh
openssl rand -hex 32
```

Then add it:

```dotenv
MCP_AUTH_TOKEN=<generated-token>
```

That token is only satisfying Fleet MCP's startup contract here. ChatGPT reaches Fleet MCP through the Secure MCP Tunnel, not through Fleet MCP's HTTP bearer-auth path.

## 3. Give it a Tailscale identity

Create an auth key from [Tailscale Admin Console → Keys](https://console.tailscale.com/admin/settings/keys), then add it:

```dotenv
TS_AUTHKEY=<tailscale-auth-key>
TS_HOSTNAME=fleet-mcp
```

If you don't remember what the auth-key options mean, use Tailscale's [auth key documentation](https://tailscale.com/docs/features/access-control/auth-keys). The Tailscale sidecar is only here so Fleet MCP can reach the Fleet server over the tailnet.

## 4. Create the Secure MCP Tunnel

Go to [OpenAI Platform → Tunnels](https://platform.openai.com/settings/organization/tunnels), create a tunnel, and associate it with the Platform organization and ChatGPT workspace that should be able to use it.

Put the tunnel ID in `.env`:

```dotenv
CONTROL_PLANE_TUNNEL_ID=<tunnel-id>
```

Then create the runtime API key from [OpenAI Platform → API keys](https://platform.openai.com/api-keys):

```dotenv
CONTROL_PLANE_API_KEY=<openai-runtime-api-key>
```

The runtime identity needs **Tunnels Read + Use**. If you're creating or changing tunnels, that administrative identity needs **Tunnels Read + Manage**. OpenAI documents the distinction under [Secure MCP Tunnel → Permissions and access](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels#permissions-and-access).

At this point the environment-specific part of `.env` should be filled in:

```dotenv
CONTROL_PLANE_TUNNEL_ID=
CONTROL_PLANE_API_KEY=
FLEET_BASE_URL=
FLEET_API_KEY=
MCP_AUTH_TOKEN=
TS_AUTHKEY=
TS_HOSTNAME=fleet-mcp
```

Leave `FLEET_MCP_REF` and `TUNNEL_CLIENT_REF` alone unless you intentionally want to build different upstream revisions.

## 5. Build and start it

```sh
docker compose build --pull --no-cache
docker compose up -d --force-recreate --remove-orphans
```

Check what came up:

```sh
docker compose ps
docker compose logs -f fleet-mcp
```

## 6. Verify the tunnel

```sh
docker compose exec fleet-mcp \
  wget -qO- http://127.0.0.1:8080/readyz
```

You want:

```text
ready
```

That means the tunnel client considers both its OpenAI control-plane connection and the local Fleet MCP binding ready. If it doesn't, OpenAI documents the tunnel client's health surfaces under [Secure MCP Tunnel → Troubleshooting](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels#troubleshooting).

## 7. Add it to ChatGPT

Open [ChatGPT Plugins](https://chatgpt.com/plugins). If Developer mode is not already enabled, OpenAI keeps the current setup instructions in [Developer mode and MCP apps in ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta).

Create the plugin with:

```text
Connection:     Tunnel
Tunnel:         fleet-mcp
Authentication: No Auth
```

Start a new chat with the plugin enabled and ask something harmless first:

```text
fleet-mcp How many systems are enrolled in Fleet?
```

If you get real Fleet data back, the whole path is working:

```text
ChatGPT
  ↓
OpenAI Secure MCP Tunnel
  ↓
tunnel-client
  ↓ stdio
Fleet MCP
  ↓ Tailscale
Fleet
```

The Dockerfile builds Fleet's official `cmd/fleet-mcp` and OpenAI's `tunnel-client` directly from the revisions in `.env.example`; no Fleet MCP application source is copied into this repository.
