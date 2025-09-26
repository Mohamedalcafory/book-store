from typing import Optional

from app import db
from app.models.author import Author


class AuthorRepository:
    def add(self, author: Author) -> Author:
        db.session.add(author)
        db.session.commit()
        db.session.refresh(author)
        return author

    def get_by_id(self, author_id: int) -> Optional[Author]:
        return db.session.get(Author, author_id)

    def get_by_name(self, name: str) -> Optional[Author]:
        return Author.query.filter_by(name=name).first()

    def list_all(self) -> list[Author]:
        return Author.query.order_by(Author.id.asc()).all()

    def update(self, author: Author) -> Author:
        db.session.commit()
        db.session.refresh(author)
        return author

    def delete(self, author: Author) -> None:
        db.session.delete(author)
        db.session.commit()


