from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import authors, books, login, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aula 03 - FastAPI com JWT",
    description="API didática com autenticação, rotas protegidas e organização em routers.",
    version="1.0.0",
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(books.router)


@app.get("/")
def home():
    return {"message": "Aula 03 - FastAPI com autenticação JWT"}
