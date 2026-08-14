# Fleet

This is the Fleet server the rest of the playground points at. It runs Fleet, MySQL, Redis, and a Tailscale sidecar with Docker Compose.

If you already know these pieces, the setup is short. If you don't, the links below take you to the place where you create the value or to the documentation that explains it.

## 1. Clone the repository

```sh
git clone https://github.com/kishjayson/playground.git
cd playground/fleet
cp .env.example .env
```

Keep real credentials in `.env`. The example file is only the configuration shape.

## 2. Give Fleet a Tailscale identity

Create an auth key from [Tailscale Admin Console → Keys](https://console.tailscale.com/admin/settings/keys), then add it to `.env`:

```dotenv
TS_AUTHKEY=<tailscale-auth-key>
TS_HOSTNAME=fleet
```

If you don't remember what the auth-key options mean, use Tailscale's [auth key documentation](https://tailscale.com/docs/features/access-control/auth-keys). The Compose file persists Tailscale state, so the node keeps the same identity across container recreation.

## 3. Add a Fleet license if you have one

If this instance is using Fleet Premium, add the license key:

```dotenv
FLEET_LICENSE_KEY=<fleet-license-key>
```

Otherwise leave it blank. Fleet's [Docker Compose deployment guide](https://fleetdm.com/guides/deploy-fleet-on-docker-compose) treats the license key as optional as well.

`FLEET_VERSION` and `TAILSCALE_VERSION` default to `latest`. Change them only when you intentionally want to hold one of those images at a specific release.

## 4. Confirm the Tailscale hostname

This repository is currently configured to expose Fleet at:

```text
https://fleet.tail2bebc3.ts.net
```

That hostname appears in `config/serve.json`. If you're using a different tailnet, replace `fleet.tail2bebc3.ts.net` there with the DNS name for your own `fleet` node before you start the stack.

The current configuration uses [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel), which makes Fleet reachable over the public internet through Tailscale's HTTPS endpoint. If you only want Fleet reachable from inside the tailnet, use [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve) instead and remove the Funnel exposure from the service configuration.

## 5. Start Fleet

```sh
docker compose up -d --pull=always --force-recreate --remove-orphans
```

Check what came up:

```sh
docker compose ps
docker compose logs -f fleet
```

The first start can take a little longer because Fleet prepares the database before it starts serving requests.

## 6. Open Fleet

For this deployment, open:

```text
https://fleet.tail2bebc3.ts.net
```

If you changed the Tailscale hostname in the previous step, use that URL instead.

The path is:

```text
Browser / Fleet clients
  ↓
Tailscale Funnel
  ↓
Fleet
  ↓
MySQL + Redis
```
