from datetime import date

from app import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    price = db.Column(db.Float, nullable=True)
    author = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r}>"