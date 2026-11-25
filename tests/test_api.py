import jwt
import time
from fastapi.testclient import TestClient

from lab_gid_authn_authz.config import ALGORITHM, SECRET

def test_valid_login(client: TestClient) -> None:
    """Realiza login válido e confere os campos do token."""
    response = client.post("/api/login", data={"username": "dalton", "password": "senha789"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800

def test_wrong_password_login(client: TestClient) -> None:
    """Rejeita login com senha incorreta."""
    response = client.post("/api/login", data={"username": "dalton", "password": "errada"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"

def test_public_info(client: TestClient) -> None:
    """Consulta /api/info sem autenticação."""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "description" in data

def test_profile_without_token(client: TestClient) -> None:
    """Rejeita /api/perfil sem token."""
    response = client.get("/api/perfil")
    assert response.status_code == 401

def test_profile_with_token(client: TestClient, token_grad: str) -> None:
    """Devolve as claims do usuário autenticado em /api/perfil."""
    response = client.get("/api/perfil", headers={"Authorization": f"Bearer {token_grad}"})
    assert response.status_code == 200
    data = response.json()
    assert data["sub"] == "alana"
    assert data["role"] == "graduacao"
    assert data["name"] == "Alana A."
    assert data["email"] == "alana@exemplo.com"

def test_listing_as_teacher(client: TestClient, token_teacher: str) -> None:
    """Lista os docentes do seed para um docente autenticado."""
    response = client.get("/api/docentes", headers={"Authorization": f"Bearer {token_teacher}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    nomes = {docente["name"] for docente in data}
    assert nomes == {"Dalton S.", "Andrey E.", "Patricia D."}

def test_listing_as_student(client: TestClient, token_grad: str) -> None:
    """Nega a listagem de docentes para um aluno autenticado."""
    response = client.get("/api/docentes", headers={"Authorization": f"Bearer {token_grad}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado"

def test_listing_without_token(client: TestClient) -> None:
    """Rejeita a listagem de docentes sem token."""
    response = client.get("/api/docentes")
    assert response.status_code == 401

def test_expired_token(client: TestClient) -> None:
    """Rejeita token com prazo expirado."""
    payload = {"sub": "testuser", "role": "graduacao", "name": "Test User", "email": "testemail@example.com", "exp": int(time.time()) - 1,}
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    response = client.get("/api/perfil", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"
