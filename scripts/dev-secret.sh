#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && { echo ".env já existe; nada foi alterado"; exit 0; }
SECRET=$(openssl rand -base64 48 2>/dev/null || python3 -c 'import secrets; print(secrets.token_urlsafe(48))')
printf 'APP_JWT_SECRET=%s\n' "$SECRET" > .env
chmod 600 .env