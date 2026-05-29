from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=80)


class UserResponse(BaseModel):
    # Permite criar a resposta a partir de objetos do SQLAlchemy, lendo atributos como user.id e user.email.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    is_admin: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    biography: str | None = None


class AuthorResponse(BaseModel):
    # Permite criar a resposta a partir de objetos do SQLAlchemy, lendo atributos como author.id e author.name.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    biography: str | None = None


class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    year: int | None = None
    author_id: int


class BookResponse(BaseModel):
    # Permite criar a resposta a partir de objetos do SQLAlchemy, lendo atributos como book.id e book.title.
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    year: int | None = None
    author_id: int
    owner_id: int
