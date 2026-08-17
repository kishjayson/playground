# Fleet

Fleet runs here with MySQL, Redis, and Tailscale using Docker Compose.

## Setup

### 1. Prepare

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/fleet
cp .env.example .env
```

### 2. Add environment values

Start by adding a Tailscale auth key to `.env`:

```dotenv
TS_AUTHKEY=<tailscale-auth-key>
TS_HOSTNAME=fleet
```

You can create an auth key at [Tailscale Admin Console → Keys](https://console.tailscale.com/admin/settings/keys). See [Tailscale auth keys](https://tailscale.com/docs/features/access-control/auth-keys).

If you use Fleet Premium, add the license key as well:

```dotenv
FLEET_LICENSE_KEY=<fleet-license-key>
```

Otherwise, leave it blank. See [Fleet on Docker Compose](https://fleetdm.com/guides/deploy-fleet-on-docker-compose).

`FLEET_VERSION` and `TAILSCALE_VERSION` default to `latest`.

### 3. Configure HTTPS exposure

The included configuration exposes Fleet at:

```text
fleet.tail2bebc3.ts.net
```

If Fleet uses a different Tailscale DNS name, update `config/serve.json`.

The committed configuration uses Tailscale Funnel. If you only want Fleet available inside the tailnet, remove `AllowFunnel` and use Tailscale Serve instead.

See [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel) and [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve).

### 4. Start

```sh
docker compose up -d --pull=always --force-recreate --remove-orphans
```

### 5. Check

```sh
docker compose ps
docker compose logs -f fleet
```

Open Fleet at:

```text
https://fleet.tail2bebc3.ts.net
```
