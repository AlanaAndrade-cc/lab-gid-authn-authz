# Gestão de Identidade, Autenticação e Autorização

**Autor:** Emerson Ribeiro de Mello  

## 1. API RESTful e uso de JWT

No sistema, existem três papéis distintos: aluno de graduação, aluno de pós-graduação e professor. Cada usuário, ao invocar o endpoint de login, recebe um token JWT que identifica seu papel entre outras informações pessoais.

Mantenha uma estrutura de dados com usuários e seus respectivos papéis, podendo ser: uma coleção em memória; um banco de dados relacional em memória (ex: H2); ou banco de dados relacional SQLite. Ao iniciar a aplicação, já carregue estaticamente um conjunto de usuários para testes.

### 1.1 Endpoint de autenticação (`/api/login`)

- Receba credenciais (usuário e senha) como entrada.
- Valide as credenciais contra o banco de dados de usuários.
- Retorne um token JWT assinado contendo:
  - **Subject (`sub`)**: identificador único do usuário.
  - **Role (`role`)**: o papel do usuário (`graduacao`, `pos-graduacao`, `professor`).
  - **Data de expiração (`exp`)**.
  - Outras declarações (*claims*) relevantes (nome, e-mail, etc.).
- Retorne erro **401 (Unauthorized)** em caso de credenciais inválidas.

### 1.2 Demais endpoints da API

Além do endpoint `/api/login`, sua API também deve prover:

1. **Endpoint público**
   - **Método:** `GET /api/info`
   - **Descrição:** retorna informações gerais sobre a API.
   - **Autenticação:** não requerida.

2. **Endpoint autenticado (qualquer papel)**
   - **Método:** `GET /api/perfil`
   - **Descrição:** retorna dados do perfil do usuário autenticado.
   - **Autenticação:** requerida (qualquer papel válido).
   - **Resposta:** código `401` se token inválido ou ausente.

3. **Endpoint com papel de professor**
   - **Método:** `GET /api/docentes`
   - **Descrição:** retorna lista de professores (exemplo).
   - **Autenticação:** requerida, apenas para papel `professor`.
   - **Resposta:** código `401` se token inválido ou ausente; código `403 (Forbidden)` se usuário não é professor.

### 1.3 Validação e testes

Faça uso de ferramentas de testes de API como: [Postman](https://www.postman.com/), [Insomnia](https://insomnia.rest) ou [Bruno](https://www.usebruno.com). Documente o passos para testar sua API, fornecendo comandos com o cURL (as ferramentas acima podem exportar as chamadas para cURL). Também é importante informar qual algoritmo usou para assinar os tokens JWT e o motivo da escolha.

## Sugestões de implementação

- **Java**
  - [Spring Boot (Spring Security)](https://spring.io)
  - [Spark Java](https://sparkjava.com)
  - [JJWT](https://github.com/jwtk/jjwt)
- **Python**
  - [FastAPI com PyJWT](https://fastapidozero.dunossauro.com/estavel/06)
  - [Flask com Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io)

---

*Documento licenciado sob [Creative Commons "Atribuição 4.0 Internacional"](https://creativecommons.org/licenses/by/4.0/deed.pt_BR).*
