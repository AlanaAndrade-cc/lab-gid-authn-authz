# GId Auth API

Toy de autenticação e autorização.

## Guia de Uso

### Instalar o `uv`

Se `uv --version` já funcionar, pule esta etapa.

Linux/macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternativas, com já tendo Python:

```bash
python -m pip install --user uv
# ou
pipx install uv
```

Feche o terminal, então confirme com:

```bash
uv --version
```

### Configuração

Após o `git clone`:

```bash
cd lab-gid-authn-authz   # entre na pasta do projeto
uv python install 3.15   # opcional: o uv já baixa se faltar
uv sync
```

`uv sync` cria o `.venv` e instala as versões travadas em `uv.lock`; não é preciso ativar o ambiente manualmente.

### Executar

```bash
./scripts/dev-secret.sh
uv run uvicorn lab_gid_authn_authz.main:app --port 8000
```

**Swagger** em `http://localhost:8000/docs`. No botão *Authorize*, informe `username` e `password` do login.

Logins do seed:

| Usuário | Senha | Papel |
|---|---|---|
| `dalton` | `senha789` | docente |
| `alana` | `senha123` | graduação |
| `arthur` | `senha456` | pós-graduação |

### Testes

Com a API no ar, em outro terminal:

PyTest:
```bash
uv run pytest -q
```

Bruno:
```bash
cd bruno
npx @usebruno/cli run --env local
```

Resultados esperados: pytest `13 passed`; Bruno `13 requests (13 Passed)` e `Tests 30/30`.

## Decisões

1. Python + FastAPI por familiaridade.

2. Função `bcrypt` para o cálculo do hash das senhas, pois, pelo o que foi exposto nos materiais, é uma função "lenta" e é mais resistente à ataques de força bruta. O `salt` vem embutido no hash.

3. Fluxo com `OAuth2` tanto no POST (`/api/login`) quanto no GET (`/api/perfil` e `/api/docentes`).

4. O `FastAPI` fica responsável por fazer uma primeira verificação e validação do token da requisição, com o `Depends`, em caso de token ausente ele já retorna erro `401`. Para o endpoint `/api/perfil`, depois dessa verificação, a função `get_current_user()` verifica se o token representa um usuário real e, caso positivo, retorna o payload com código `200`. Para o endpoint `/api/docentes`, além de validar que o usuário é um usuário real, ele verifica se o `role` do usuário é "docente", através do `require_teacher()`.

5. Token JWT assinado com chave, de acordo com algoritmo `HS256`.

6. Código `401` para token ausente ou inválido (problema de autenticação). Código `403` para token válido sem `role` exidigo (problema de autorização). Código `200` representando ação bem sucedida.
