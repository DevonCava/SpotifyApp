# Deployment Checklist
This project is set up for a conservative Apache deployment path. Use this checklist before merging to `main` and before going live. For local testing, use `dev.sh`; for deployment, keep secrets in the server environment and leave the Django code unchanged.
## Pre-deployment checklist
### Security review
- [ ] Set a strong `SECRET_KEY` in the server environment; do not commit it to `.env`
- [ ] Keep `DEBUG=False` for production by setting the environment variable, not by editing `settings.py`
- [ ] Set `ALLOWED_HOSTS` to the real domain(s) only
- [ ] Set `CSRF_TRUSTED_ORIGINS` to the HTTPS domain(s)
- [ ] Confirm HTTPS is enabled before using `SECURE_SSL_REDIRECT=True`
- [ ] Keep `TokenCaches/` restricted to the app user only (`chmod 700`)
- [ ] Verify Spotify `CLIENTID` and `CLIENTSECRET` are only present in the server environment
- [ ] Review `ADMIN_EMAIL` / `SERVER_EMAIL` for error notifications
- [ ] Confirm `db.sqlite3` is acceptable for the current deployment model, or switch to a server database before production
### Repository safety
- [ ] Confirm `.env`, `db.sqlite3`, `TokenCaches/.cache-*`, and other local-only files are ignored and not committed
- [ ] Confirm no OAuth token cache file contains live access or refresh tokens
### Runtime / deployment readiness
- [ ] Install Python dependencies from `requirements.txt`
- [ ] Run `python manage.py check`
- [ ] Run `python manage.py check --deploy`
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Confirm Apache serves `staticfiles/`
- [ ] Confirm the Spotify OAuth redirect URI matches the production URL
- [ ] Confirm the app can read the token cache directory on the server
- [ ] If Apache terminates TLS, keep the `https://` redirect settings enabled and serve the site on HTTPS; the sample vhost is a starting point, not a full TLS configuration
## Recommended server variables
Set these in your production environment or in the Apache/mod_wsgi environment block:
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=yourdomain.example,www.yourdomain.example`
- `CSRF_TRUSTED_ORIGINS=https://yourdomain.example,https://www.yourdomain.example`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `ADMIN_NAME=Ops`
- `ADMIN_EMAIL=ops@yourdomain.example`
- `SERVER_EMAIL=server@yourdomain.example`
- `CLIENTID=...`
- `CLIENTSECRET=...`
- `SPOTIFY_REDIRECT_URI=https://yourdomain.example/callback`
- `SPOTIFY_USERNAME=your-spotify-username`
- `TOKEN_CACHE_DIR=/srv/spotifyapp/SpotifyApp/TokenCaches`
- `SPOTIFY_OAUTH_OPEN_BROWSER=False`
## Apache deployment steps
### 1) Install dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip apache2 libapache2-mod-wsgi-py3
```
### 2) Put the app in a stable server path
Example:
```bash
/srv/spotifyapp/SpotifyApp
```
### 3) Create and activate a virtual environment
```bash
python3 -m venv /srv/spotifyapp/venv
source /srv/spotifyapp/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
### 4) Configure environment variables
Copy `.env.example` to your server environment, then fill in production values.
If you are using Apache + mod_wsgi, make sure those values are available to the Apache process itself. On Debian, the simplest approach is to add the required `export ...` lines to `/etc/apache2/envvars` (or to a root-owned systemd drop-in for the Apache service) and then restart Apache. The vhost uses `PassEnv` so the variables will flow into the WSGI process. Do not store production secrets inside the repository or inside `settings.py`.
### 5) Run Django checks and database/static prep
```bash
source /srv/spotifyapp/venv/bin/activate
cd /srv/spotifyapp/SpotifyApp
python manage.py check
python manage.py check --deploy
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```
### 6) Restrict token cache permissions
```bash
chmod 700 /srv/spotifyapp/SpotifyApp/TokenCaches
```
### 7) Install the Apache vhost
Use `deploy/apache/spotifyapp.conf` as a starting point, then enable the site and reload Apache.
If Apache is also terminating TLS, copy this vhost pattern to your `:443` configuration, install certificates, and keep `SECURE_SSL_REDIRECT=True`. If you are only doing a temporary internal HTTP deployment, keep the site behind a trusted network and adjust the redirect setting only for that environment.
After updating the vhost, run:
```bash
sudo a2ensite spotifyapp
sudo systemctl reload apache2
```
## Merge-to-main checklist
- [ ] No secrets committed to the repository, including `.env` values or OAuth token caches
- [ ] `python manage.py check` passes
- [ ] `python manage.py check --deploy` passes with production env vars set
- [ ] Static files are collected successfully
- [ ] Apache config has been validated on the server
- [ ] OAuth callback URL matches the production domain
- [ ] `main` branch is ready to deploy without further code changes
