from datetime import datetime

from app import db


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    biography = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    country = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    books = db.relationship("Book", backpopulates="author", lazy=True)

    def __repr__(self) -> str:
        return f"<Author id={self.id} name={self.name!r}>"


