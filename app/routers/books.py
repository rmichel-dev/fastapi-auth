from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import Author, Book, User
from ..schemas import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    author = db.query(Author).filter(Author.id == book_data.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    book = Book(
        title=book_data.title,
        year=book_data.year,
        author_id=book_data.author_id,
        owner_id=current_user.id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("/my-books", response_model=list[BookResponse])
def list_my_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Book).filter(Book.owner_id == current_user.id).all()


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    if book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não pode excluir este livro")

    db.delete(book)
    db.commit()
    return None
