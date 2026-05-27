from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from .models import Author, Base, Book, User
from .schemas import Token, UserCreate, UserResponse
from .security import ALGORITHM, SECRET_KEY, create_access_token, hash_password, verify_password


# Pydantic schema usado para validar os dados de criação de um autor.
class AuthorCreate(BaseModel):
    name: str
    biography: str | None = None


# Cria a instância principal da aplicação FastAPI.
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Garante que as tabelas definidas pelos modelos existam no banco SQLite.
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario nao encontrado")

    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return current_user


@app.get("/")
def home():
    # Rota de teste para verificar se o servidor está ativo.
    return {"message": "Hello World"}


@app.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Cria o usuário com a senha armazenada como hash.
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    # Persiste os dados do usuário no banco.
    db.add(user)
    db.commit()
    db.refresh(user)

    # Retorna os dados do usuário criado.
    return user


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais invalidas")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users")
def list_users():
    # Abre uma sessão de banco de dados para listar todos os usuários.
    db: Session = SessionLocal()

    # Executa a consulta para buscar todos os registros de usuário.
    users = db.query(User).all()

    return users


@app.post("/authors")
def create_author(author: AuthorCreate):
    # Inicia uma sessão de banco de dados para salvar o autor.
    db: Session = SessionLocal()

    # Cria a entidade Author usando dados validados pelo Pydantic.
    new_author = Author(name=author.name, biography=author.biography)

    # Persiste o autor no banco.
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    # Retorna o autor recém-criado.
    return {
        "id": new_author.id,
        "name": new_author.name,
        "biography": new_author.biography,
    }


@app.get("/authors")
def list_authors():
    # Abre uma sessão para recuperar todos os autores.
    db: Session = SessionLocal()

    # Consulta todos os autores cadastrados.
    authors = db.query(Author).all()

    return authors


@app.get("/authors/{author_id}")
def get_author(author_id: int):
    # Abre uma sessão para buscar o autor pelo ID informado.
    db: Session = SessionLocal()

    # Consulta o autor correspondente ao ID.
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        # Retorna uma mensagem simples se o autor não for encontrado.
        return {"error": "Author not found"}

    return {
        "id": author.id,
        "name": author.name,
        "biography": author.biography,
    }


@app.get("/books")
def list_books():
    # Abre uma sessão para listar os livros cadastrados.
    db: Session = SessionLocal()

    # Consulta todos os registros da tabela books.
    books = db.query(Book).all()

    return books


@app.post("/books")
def create_book(title: str, year: int, author_id: int):
    # Abre uma sessão de banco de dados para inserir um novo livro.
    db: Session = SessionLocal()

    # Cria o modelo Book com título, ano e autor associado.
    new_book = Book(title=title, year=year, author_id=author_id)

    # Salva o novo livro no banco de dados.
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    # Retorna o registro do livro criado.
    return {
        "id": new_book.id,
        "title": new_book.title,
        "year": new_book.year,
        "author_id": new_book.author_id,
    }


@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")

    db.delete(book)
    db.commit()

    return {"message": "Livro removido com sucesso"}
