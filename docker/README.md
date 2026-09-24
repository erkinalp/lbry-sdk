### How to run with docker-compose
1. Edit config file and after that fix permissions with
```
sudo chown -R 999:999 webconf.yaml
```
2. Start SDK with
```
docker-compose up -d
```

### Security
The JSON-RPC API (`api`, port 5279) has no authentication: anyone who can reach it can
export the wallet and send funds. `webconf.yaml` therefore binds the API and the streaming
server to `localhost`, and `docker-compose.yml` uses host networking so they are only
reachable from the host itself.

If remote access is required, keep the daemon on `localhost` and put it behind an
authenticating reverse proxy (mTLS, API token or password). If browsers need to call the
API, set `allowed_origin` to the exact origin of your app. The daemon refuses to start
with `allowed_origin: "*"` when `api` is bound to a non-loopback address.
