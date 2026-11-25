import jwt
import pytest
from fastapi import HTTPException

from lab_gid_authn_authz.config import ALGORITHM, SECRET
from lab_gid_authn_authz.security import password_to_hash, check_password, payload_to_token, token_to_payload

def test_hash_and_check():
    """Gera o hash bcrypt e verifica senhas correta e incorreta."""
    h = password_to_hash("senha123")
    assert h.startswith("$2b$12$")
    assert check_password("senha123", h) is True
    assert check_password("senha122", h) is False

def test_token_back_and_forth():
    """Codifica e decodifica o token preservando as claims."""
    payload = token_to_payload(payload_to_token("alana","graduacao","Alana A.","alana@exemplo.com"))
    assert payload["sub"] == "alana"
    assert payload["role"] == "graduacao"
    assert payload["name"] == "Alana A."
    assert payload["email"] == "alana@exemplo.com"
    assert isinstance(payload["exp"], int)

def test_token_with_other_secret():
    """Rejeita token assinado com outra chave secreta."""
    token = jwt.encode({"sub": "alana", "role": "graduacao"}, "other-secret", algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc: token_to_payload(token)
    assert exc.value.status_code == 401

def test_token_without_role():
    """Rejeita token sem a claim obrigatória role."""
    token = jwt.encode({"sub": "alana"}, SECRET, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc: token_to_payload(token)
    assert exc.value.status_code == 401
