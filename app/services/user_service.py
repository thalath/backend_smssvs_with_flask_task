from typing import List, Optional

from app.models.user import User
from app.models.token_blocklist import TokenBlocklist
from extensions import db

class UserService:
    
    @staticmethod
    def get_all() -> List[User]:
        return User.query.order_by(User.id.desc()).all()
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)
    
    @staticmethod
    def create_user(data: dict, password: str) -> User:
        user = User(
            username=data["username"],
            full_name=data["full_name"],
            is_active=data.get("is_active", True),
            email=data["email"]
        )
        
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user: User, data: dict, password: Optional[str] = None) -> User:
        user.full_name = data['full_name']
        user.email = data['email']
        user.is_active = data.get("is_active", True)
        user.username = data["username"]

        if password:
            user.set_password(password)
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
        
