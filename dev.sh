#!/usr/bin/env bash
set -euo pipefail

# Local development defaults for testing on plain HTTP.
# These values intentionally override any exported production vars.
export DEBUG=True
export ALLOW_DEVELOPMENT_FALLBACK=True
export SECURE_SSL_REDIRECT=False
export SESSION_COOKIE_SECURE=False
export CSRF_COOKIE_SECURE=False
export ALLOWED_HOSTS=127.0.0.1,localhost
export CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
export SPOTIFY_REDIRECT_URI=http://127.0.0.1:8080/callback
export SPOTIFY_OAUTH_OPEN_BROWSER=True

python manage.py runserver 127.0.0.1:8000

