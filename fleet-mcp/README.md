# Fleet MCP

Run Fleet's official MCP server through an [OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels), with Tailscale providing private reachability from Fleet MCP to the Fleet server.

## 1. Clone the repository

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/fleet-mcp
cp .env.example .env
```

`.env.example` contains pinned upstream revisions and the variables this deployment expects. Put secrets and environment-specific values in `.env`; do not edit the example file with real credentials.

## 2. Connect Fleet MCP to Fleet

Open `.env` and set the URL you use to reach your Fleet instance:

```dotenv
FLEET_BASE_URL=https://fleet.example.com
```

Create a Fleet API-only user in **Fleet → Settings → Users → Create user**, then add its token:

```dotenv
FLEET_API_KEY=<fleet-api-only-user-token>
```

Fleet documents API-only users in the [fleetctl guide](https://fleetdm.com/guides/fleetctl#using-fleetctl-with-an-api-only-user). The upstream [Fleet MCP configuration](https://github.com/fleetdm/fleet/tree/main/cmd/fleet-mcp#configuration) requires an API-only token; use the least-privileged role that covers the tools you intend to expose. Observer is sufficient for read-only inventory; use Observer+ if you intend to run live queries.

Fleet MCP also requires an MCP auth token at startup, even though this deployment connects to it locally over stdio. Generate one:

```sh
openssl rand -hex 32
```

Copy the output into `.env`:

```dotenv
MCP_AUTH_TOKEN=<generated-token>
```

This token is not used to authenticate ChatGPT to the Secure MCP Tunnel; it is retained because Fleet MCP requires it to start. See the upstream [Fleet MCP configuration](https://github.com/fleetdm/fleet/tree/main/cmd/fleet-mcp#configuration).

## 3. Connect the deployment to Tailscale

Create an auth key from the [Tailscale Admin Console → Keys](https://console.tailscale.com/admin/settings/keys), then add it to `.env`:

```dotenv
TS_AUTHKEY=<tailscale-auth-key>
TS_HOSTNAME=fleet-mcp
```

Tailscale's [auth key documentation](https://tailscale.com/docs/features/access-control/auth-keys) explains key options, expiration, tags, and device behavior.

The Tailscale sidecar gives Fleet MCP the same private network path you already use to reach Fleet. `FLEET_BASE_URL` still determines the Fleet address Fleet MCP actually calls.

## 4. Create the OpenAI Secure MCP Tunnel

Open [OpenAI Platform → Tunnels](https://platform.openai.com/settings/organization/tunnels) and create a tunnel. Associate it with the Platform organization and ChatGPT workspace that should be allowed to use it, then copy the tunnel ID into `.env`:

```dotenv
CONTROL_PLANE_TUNNEL_ID=<tunnel-id>
```

Create a runtime key from [OpenAI Platform → API keys](https://platform.openai.com/api-keys) and add it:

```dotenv
CONTROL_PLANE_API_KEY=<openai-runtime-api-key>
```

The identity behind the runtime key needs **Tunnels Read + Use**. Creating or editing tunnels requires **Tunnels Read + Manage**. See [Secure MCP Tunnel → Permissions and access](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels#permissions-and-access) for the distinction.

At this point the environment-specific portion of `.env` should contain values for:

```dotenv
CONTROL_PLANE_TUNNEL_ID=
CONTROL_PLANE_API_KEY=
FLEET_BASE_URL=
FLEET_API_KEY=
MCP_AUTH_TOKEN=
TS_AUTHKEY=
TS_HOSTNAME=fleet-mcp
```

Leave `FLEET_MCP_REF` and `TUNNEL_CLIENT_REF` at the pinned values in `.env.example` unless you intentionally want to build different upstream revisions.

## 5. Build and start

```sh
docker compose build --pull --no-cache
docker compose up -d --force-recreate --remove-orphans
```

Inspect the deployment:

```sh
docker compose ps
docker compose logs -f fleet-mcp
```

## 6. Verify the tunnel

```sh
docker compose exec fleet-mcp \
  wget -qO- http://127.0.0.1:8080/readyz
```

Expected response:

```text
ready
```

`ready` means the tunnel client considers its control-plane connection and local MCP binding ready for traffic. The Secure MCP Tunnel guide documents the tunnel client's [`/healthz`, `/readyz`, `/metrics`, and local `/ui` surfaces](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels#troubleshooting).

## 7. Add Fleet MCP to ChatGPT

Open [ChatGPT Plugins](https://chatgpt.com/plugins). If needed, enable Developer mode first; OpenAI documents the current controls in [Developer mode and MCP apps in ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta).

Create a new plugin/app with:

```text
Connection:     Tunnel
Tunnel:         fleet-mcp
Authentication: No Auth
```

`No Auth` means there is no additional end-user OAuth layer between ChatGPT and Fleet MCP. The tunnel client authenticates to OpenAI with `CONTROL_PLANE_API_KEY`; Fleet MCP authenticates to Fleet with `FLEET_API_KEY`.

Start a new chat with the plugin enabled and ask a harmless read-only question, for example:

```text
fleet-mcp How many systems are enrolled in Fleet?
```

If that returns Fleet data, the complete path is working:

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

The Dockerfile builds Fleet's official `cmd/fleet-mcp` and OpenAI's `tunnel-client` directly from the revisions pinned in `.env.example`; no Fleet MCP application source is copied into this repository.
