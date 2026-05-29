from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Author
from ..schemas import AuthorCreate, AuthorResponse

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author_data: AuthorCreate, db: Session = Depends(get_db)):
    author = Author(name=author_data.name, biography=author_data.biography)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.get("/", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()
