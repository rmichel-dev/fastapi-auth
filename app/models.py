from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base


# Modelo de usuário usado apenas como exemplo.
class User(Base):
    __tablename__ = "users"

    # Identificador único do usuário.
    id = Column(Integer, primary_key=True, index=True)
    # Nome do usuário.
    name = Column(String, nullable=False)
    # Email do usuário, que deve ser único.
    email = Column(String, unique=True, nullable=False)
    # Senha do usuário, armazenada de forma segura (hash).
    hashed_password = Column(String, nullable=False)
    # Indica se o usuário tem privilégios de administrador.
    is_admin = Column(Boolean, default=False)

    # Livros cadastrados por este usuário.
    books = relationship("Book", back_populates="owner")


# Autor no sistema de biblioteca.
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    # Nome do autor.
    name = Column(String, nullable=False)
    # Biografia do autor, campo opcional.
    biography = Column(String, nullable=True)

    # Relacionamento com a tabela de livros.
    books = relationship("Book", back_populates="author")


# Livro no sistema de biblioteca.
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    # Título do livro.
    title = Column(String, nullable=False)
    # Ano de publicação do livro.
    year = Column(Integer, nullable=False)
    # Chave estrangeira para o autor do livro.
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relacionamento reverso para acessar o autor.
    author = relationship("Author", back_populates="books")
    owner = relationship("User", back_populates="books")
