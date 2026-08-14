# Fleet

Docker Compose deployment of Fleet, MySQL, Redis, and Tailscale.

## Procedure

### 1. Prepare

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/fleet
cp .env.example .env
```

### 2. Configure environment

Set the Tailscale identity in `.env`:

```dotenv
TS_AUTHKEY=<tailscale-auth-key>
TS_HOSTNAME=fleet
```

Create auth keys at [Tailscale Admin Console → Keys](https://console.tailscale.com/admin/settings/keys). See [Tailscale auth keys](https://tailscale.com/docs/features/access-control/auth-keys).

Set `FLEET_LICENSE_KEY` when using Fleet Premium:

```dotenv
FLEET_LICENSE_KEY=<fleet-license-key>
```

Leave it blank otherwise. See [Fleet on Docker Compose](https://fleetdm.com/guides/deploy-fleet-on-docker-compose).

`FLEET_VERSION` and `TAILSCALE_VERSION` default to `latest`.

### 3. Configure HTTPS exposure

Edit `config/serve.json` when the Fleet node uses a different Tailscale DNS name.

Current hostname:

```text
fleet.tail2bebc3.ts.net
```

The committed configuration enables Tailscale Funnel. Remove `AllowFunnel` for tailnet-only exposure through Tailscale Serve.

References: [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel), [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve).

### 4. Start

```sh
docker compose up -d --pull=always --force-recreate --remove-orphans
```

### 5. Verify

```sh
docker compose ps
docker compose logs -f fleet
```

Fleet URL:

```text
https://fleet.tail2bebc3.ts.net
```
