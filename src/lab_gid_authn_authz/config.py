"""Configurações do sistema."""

import os
from dotenv import load_dotenv


def load_secret() -> str:
    load_dotenv()
    secret = os.environ.get("APP_JWT_SECRET", "")
    if not secret: raise RuntimeError("Segredo JWT não foi definido.")
    return secret


SECRET: str = load_secret()
ALGORITHM: str = "HS256"
TTL_SEC: int = 1800
ROLES: frozenset[str] = frozenset({"graduacao", "pos-graduacao", "docente"})

API_NAME = "GID Auth API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API toy de autenticação para o sistema GID"
