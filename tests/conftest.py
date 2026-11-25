import pytest
from fastapi.testclient import TestClient

from lab_gid_authn_authz.main import app

@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c

def get_token(client: TestClient, username: str, password: str) -> str:
    response = client.post("/api/login", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def token_teacher(client: TestClient) -> str:
    return get_token(client, "dalton", "senha789")

@pytest.fixture
def token_grad(client: TestClient) -> str:
    return get_token(client, "alana", "senha123")
