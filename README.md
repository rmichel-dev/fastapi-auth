# Biblioteca FastAPI

API didática de biblioteca criada com FastAPI, SQLAlchemy e SQLite.

O projeto demonstra uma organização simples com routers separados, schemas Pydantic, cadastro de usuários, hash de senha, autenticação com JWT e rotas protegidas.

## Recursos

- Cadastro e listagem de usuários
- Cadastro e listagem de autores
- Login com JWT
- Cadastro de livros vinculado ao usuário autenticado
- Listagem dos livros do usuário logado
- Exclusão de livros somente pelo usuário dono do registro

## Requisitos

- Python 3.11 a 3.13
- FastAPI
- SQLAlchemy
- Uvicorn
- Bcrypt
- Python Jose
- Python Multipart
- Email Validator

## Instalação

1. Crie o ambiente virtual.

Linux/macOS:

```bash
python3.13 -m venv venv
```

Windows:

```powershell
py -3.13 -m venv venv
```

2. Ative o ambiente virtual.

Linux/macOS:

```bash
source venv/bin/activate
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
venv\Scripts\activate.bat
```

3. Instale as dependências.

Instale as dependências listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Execução

Execute a aplicação com:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa ficará disponível em:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Fluxo de teste no Swagger

1. Acesse `http://127.0.0.1:8000/docs`.
2. Use `POST /users/` para criar um usuário.
3. Clique em **Authorize**.
4. Informe o e-mail no campo `username` e a senha no campo `password`.
5. Use `POST /authors/` para criar um autor.
6. Use `POST /books/` para criar um livro vinculado ao usuário logado.
7. Use `GET /books/my-books` para listar apenas os livros do usuário autenticado.
8. Crie outro usuário e confirme que cada usuário vê somente os próprios livros.

## Como testar autenticação com curl

1. Crie um usuário:

Linux/macOS:

```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Rodrigo","email":"rodrigo@email.com","password":"123456"}'
```

Windows PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:8000/users/ `
  -H "Content-Type: application/json" `
  -d "{\"name\":\"Rodrigo\",\"email\":\"rodrigo@email.com\",\"password\":\"123456\"}"
```

2. Faça login usando o e-mail no campo `username`:

Linux/macOS:

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=rodrigo@email.com&password=123456"
```

Windows PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:8000/login `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=rodrigo@email.com&password=123456"
```

3. Copie o valor de `access_token` retornado.

4. Use o token em rotas protegidas:

Linux/macOS:

```bash
curl -X GET http://127.0.0.1:8000/books/my-books \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

Windows PowerShell:

```powershell
curl.exe -X GET http://127.0.0.1:8000/books/my-books `
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## Endpoints principais

- `GET /` - rota de teste
- `POST /users/` - cria um usuário com senha criptografada
- `GET /users/` - lista todos os usuários
- `POST /login` - autentica o usuário e retorna um token JWT
- `POST /authors/` - cria um autor
- `GET /authors/` - lista todos os autores
- `POST /books/` - cria um livro para o usuário autenticado
- `GET /books/my-books` - lista os livros do usuário autenticado
- `DELETE /books/{book_id}` - remove um livro do usuário autenticado

## Banco de dados

O projeto usa SQLite, e o arquivo do banco fica em `database.db` no diretório raiz.

## Observações

- As rotas `POST /books/`, `GET /books/my-books` e `DELETE /books/{book_id}` exigem autenticação com token Bearer.
- A rota `POST /login` usa `OAuth2PasswordRequestForm`, então os dados devem ser enviados como formulário.
- A chave `SECRET_KEY` em `app/auth.py` é apenas para estudo. Em produção, use uma chave forte e fora do código-fonte.
- Em produção, o ideal é usar variáveis de ambiente, banco PostgreSQL/MySQL e migrations com Alembic.
- No Windows PowerShell, use `curl.exe` nos exemplos. O comando `curl` sozinho pode ser um alias do PowerShell.
