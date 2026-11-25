"""FastAPI e endpoints"""

from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from lab_gid_authn_authz.users import search_by_username, list_teachers
from lab_gid_authn_authz.config import API_DESCRIPTION, API_NAME, API_VERSION
from lab_gid_authn_authz.security import check_password, get_current_user, payload_to_token, require_teacher

app = FastAPI(title="GID Auth API", version="1.0.0")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800


class InfoResponse(BaseModel):
    name: str
    version: str
    description: str


class PerfilResponse(BaseModel):
    sub: str
    role: str
    name: str
    email: str


class DocenteResponse(BaseModel):
    sub: str
    name: str
    email: str


@app.post("/api/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user = search_by_username(form.username)
    if not user or not check_password(form.password, user.hash_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return TokenResponse(access_token=payload_to_token(user.username, user.role, user.name, user.email))


@app.get("/api/info", response_model=InfoResponse)
def info() -> InfoResponse:
    return InfoResponse(name=API_NAME, version=API_VERSION, description=API_DESCRIPTION)


@app.get("/api/perfil", response_model=PerfilResponse)
def perfil(payload: dict = Depends(get_current_user)) -> PerfilResponse:
    return PerfilResponse(sub=payload["sub"], role=payload["role"], name=payload["name"], email=payload["email"])


@app.get("/api/docentes", response_model=list[DocenteResponse])
def docentes(payload: dict = Depends(require_teacher)) -> list[DocenteResponse]:
    return [DocenteResponse(sub=u.username, name=u.name, email=u.email) for u in list_teachers()]
