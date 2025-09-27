from datetime import date

from app import db


class Book(db.Model):
    __tablename__ = "books"
    
    # Composite indexes for query optimization
    __table_args__ = (
        # Most common filter combination from your API
        db.Index('idx_category_price_date', 'category', 'price', 'release_date'),
        # Author + category filtering
        db.Index('idx_author_category', 'author', 'category'),
        # Price range queries
        db.Index('idx_price_date', 'price', 'release_date'),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date, nullable=True, index=True)
    price = db.Column(db.Float, nullable=True, index=True)
    author = db.Column(db.String(200), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    stock = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r}>"