from typing import Optional

from app import db
from app.models.category import Category


class CategoryRepository:
    def add(self, category: Category) -> Category:
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)
        return category

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return db.session.get(Category, category_id)

    def get_by_name(self, name: str) -> Optional[Category]:
        return Category.query.filter_by(name=name).first()

    def list_all(self) -> list[Category]:
        return Category.query.order_by(Category.id.asc()).all()

    def update(self, category: Category) -> Category:
        db.session.commit()
        db.session.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        db.session.delete(category)
        db.session.commit()


