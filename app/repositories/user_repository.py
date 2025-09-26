from typing import Optional

from app import db
from app.models.user import User


class UserRepository:
    def add(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def list_all(self) -> list[User]:
        return User.query.order_by(User.id.asc()).all()

    def update(self, user: User) -> User:
        db.session.commit()
        db.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        db.session.delete(user)
        db.session.commit()


