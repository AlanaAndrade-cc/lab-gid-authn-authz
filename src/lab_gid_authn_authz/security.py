
"""Segurança e autenticação usando JWT e bcrypt."""

import jwt
import time
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from lab_gid_authn_authz.config import ROLES, SECRET, ALGORITHM, TTL_SEC

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def password_to_hash(password: str) -> str:
    """Hash a senha usando bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def check_password(password: str, hash_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    try: return bcrypt.checkpw(password.encode(), hash_password.encode())
    except ValueError: return False


def payload_to_token(sub: str, role: str, name: str, email: str) -> str:
    """Codifica os dados fornecidos e retorna o token JWT."""
    payload = { "sub": sub, "role": role, 
               "name": name, "email": email,
                "exp": int(time.time()) + TTL_SEC }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def token_to_payload(token: str) -> dict:
    """Decodifica o token JWT e retorna o payload."""
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM], options={"require": ["sub", "role", "exp"]})
        if payload.get("role") not in ROLES: raise HTTPException(status_code=401, detail="Credenciais inválidas")
        return payload
    except jwt.PyJWTError: raise HTTPException(status_code=401, detail="Credenciais inválidas")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Recupera o usuário a partir do token JWT fornecido no cabeçalho de autorização."""
    return token_to_payload(token)


def require_teacher(payload: dict = Depends(get_current_user)) -> dict:
    """Verifica se o usuário tem a role 'docente'."""
    if payload.get("role") != "docente": raise HTTPException(status_code=403, detail="Acesso negado")
    return payload
