"""Banco de dados em memória do sistema."""

from dataclasses import dataclass

from lab_gid_authn_authz.security import password_to_hash


@dataclass(frozen=True)
class User:
    username: str
    name: str
    email: str
    role: str
    hash_password: str

def _seed() -> dict[str, User]: 
    users = [
        {"username": "alana", "name": "Alana A.", "email": "alana@exemplo.com", "role": "graduacao", "password": "senha123"},
        {"username": "pedro", "name": "Pedro L.", "email": "pedro@exemplo.com", "role": "graduacao", "password": "senha234"},
        {"username": "duda", "name": "Duda M.", "email": "duda@exemplo.com", "role": "graduacao", "password": "senha345"},

        {"username": "arthur", "name": "Arthur F.", "email": "arthur@exemplo.com", "role": "pos-graduacao", "password": "senha456"},
        {"username": "igor", "name": "Igor G.", "email": "igor@exemplo.com", "role": "pos-graduacao", "password": "senha567"},
        {"username": "vitor", "name": "Vitor B.", "email": "vitor@exemplo.com", "role": "pos-graduacao", "password": "senha678"},

        {"username": "dalton", "name": "Dalton S.", "email": "dalton@exemplo.com", "role": "docente", "password": "senha789"},
        {"username": "andrey", "name": "Andrey E.", "email": "andrey@exemplo.com", "role": "docente", "password": "senha890"},
        {"username": "patricia", "name": "Patricia D.", "email": "patricia@exemplo.com", "role": "docente", "password": "senha901"},
    ]
    return {u["username"]: User(u["username"], u["name"], u["email"], u["role"], password_to_hash(u["password"])) for u in users}


USERS: dict[str, User] = _seed()


def search_by_username(username: str) -> User | None:
    """Busca um usuário pelo username."""
    return USERS.get(username)


def list_teachers() -> list[User]:
    """Lista todos os usuários com a role 'docente'."""
    return [u for u in USERS.values() if u.role == "docente"]
