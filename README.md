# Biblioteca FastAPI

Este projeto é uma API simples de biblioteca criada com FastAPI e SQLAlchemy usando SQLite como banco de dados.

## Descrição

A aplicação inclui modelos relacionais para:

- `Author`: autor com `id`, `name` e `biography`
- `Book`: livro com `id`, `title`, `year` e `author_id`

Também há rotas para criar e listar autores, livros e usuários.
O projeto também inclui cadastro de usuário com senha criptografada, login com JWT e uma rota de exclusão de livros protegida para administradores.

## Requisitos

- Python 3.11+ (ou outra versão compatível)
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
python3 -m venv venv
```

Windows:

```powershell
py -m venv venv
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

3. Instale as dependências:

```bash
pip install fastapi uvicorn sqlalchemy bcrypt "python-jose[cryptography]" python-multipart email-validator
```

## Execução

Execute a aplicação com:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

A documentação interativa ficará disponível em:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Como testar autenticação

1. Crie um usuário:

Linux/macOS:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Rodrigo","email":"rodrigo@email.com","password":"123456"}'
```

Windows PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:8000/users `
  -H "Content-Type: application/json" `
  -d "{\"name\":\"Rodrigo\",\"email\":\"rodrigo@email.com\",\"password\":\"123456\"}"
```

2. Faça login usando o email no campo `username`:

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
curl -X DELETE http://127.0.0.1:8000/books/1 \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

Windows PowerShell:

```powershell
curl.exe -X DELETE http://127.0.0.1:8000/books/1 `
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

Observação: a rota `DELETE /books/{book_id}` exige que o usuário tenha `is_admin = true` no banco de dados.

## Endpoints principais

- `GET /` - rota de teste
- `POST /authors` - cria um novo autor
- `GET /authors` - lista todos os autores
- `GET /authors/{author_id}` - busca autor por ID
- `POST /books` - cria um novo livro
- `GET /books` - lista todos os livros
- `DELETE /books/{book_id}` - remove um livro, exige usuário administrador autenticado
- `POST /users` - cria um usuário com senha criptografada
- `GET /users` - lista todos os usuários
- `POST /login` - autentica o usuário e retorna um token JWT

## Banco de dados

O arquivo SQLite usado pelo projeto é `database.db` no diretório raiz.

## Observações

- A rota `POST /books` espera parâmetros `title`, `year` e `author_id` no corpo da requisição ou em query string.
- A rota `POST /authors` valida o corpo com um schema Pydantic.
- A rota `POST /login` usa `OAuth2PasswordRequestForm`, então os dados devem ser enviados como formulário.
- A chave `SECRET_KEY` em `app/security.py` é apenas para estudo. Em produção, use uma chave forte e fora do código-fonte.
- No Windows PowerShell, use `curl.exe` nos exemplos. O comando `curl` sozinho pode ser um alias do PowerShell.
