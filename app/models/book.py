from datetime import date

from app import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    price = db.Column(db.Float, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    author = db.relationship("Author", backpopulates="books")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", backpopulates="books")
    stock = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r}>"