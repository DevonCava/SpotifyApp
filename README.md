# SpotifyApp
A Django app that shows Spotify listening stats and top tracks/artists for the authenticated user.
## What’s included
- Django project: `SpotifyDjangoConfig`
- App logic and views: `spotifyStuff`
- Spotify OAuth helpers: `userMethods.py`
- Deployment guide: `DEPLOY.md`
- Apache vhost example: `deploy/apache/spotifyapp.conf`
## Public release hygiene
The repository is intended to be public-safe as long as runtime secrets stay local:
- keep real values in `.env` and never commit it
- keep `db.sqlite3` local-only unless you intentionally want to ship a throwaway dev database
- keep `TokenCaches/.cache-*` private, because Spotify OAuth tokens can be stored there
- use `cp .env.example .env` as the starting point for local setup
## Local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
## Local testing without HTTPS
If `runserver` is redirecting you to HTTPS, try opening the local link in an incognito browser to avoid the browser from auto-redirecting to HTTPS. Or, your environment is still using production-style security settings. For local testing, set these values in `.env` before starting the server:
```env
DEBUG=True
ALLOW_DEVELOPMENT_FALLBACK=True
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
ALLOWED_HOSTS=127.0.0.1,localhost
```
Then run:
```bash
source .venv/bin/activate
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```
Or use the helper script, which forces safe local defaults even if your shell still has production variables exported:
```bash
bash ./dev.sh
```
If you want to test Spotify login locally too, make sure your Spotify app has a redirect URI that matches `SPOTIFY_REDIRECT_URI` in `.env`. The local helper defaults are designed for `runserver` on `127.0.0.1:8000` with Spotify OAuth callbacks on `http://127.0.0.1:8080/callback`.
## Deployment notes
Before merging to `main` and deploying, review `DEPLOY.md` and make sure the required environment variables are set in the server environment, not in the repository. The app is configured to work with Apache + mod_wsgi and to serve collected static files from `staticfiles/`.
