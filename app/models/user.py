from extensions import db

from datetime import datetime
from typing import Dict, Any
import re

from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError

from app.models.associations import user_roles

class User(db.Model):
    __tablename__ ="users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    roles = db.relationship("Role", secondary=user_roles, back_populates="users")

    def set_password(self, password: str) -> None:
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contained at least on digit.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contained at least one lowercase character.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contained at least one uppercase character.")
        if not re.search(r"[!@#$%^&*()_+{}\";' <>/?.,]", password):
            raise ValidationError("Password must contained at least one special character.")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name:str) -> bool:
        return any(
            role.name == role_name 
            for role in self.roles
        )
    
    def get_permission_codes(self) -> set[str]:
        return {
            perm.code 
            for role in self.roles 
            for perm in role.permissions
        }
    
    def has_permission(self, permission_code: str) -> bool:
        return permission_code in self.get_permission_codes()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "is_active": self.is_active
        }
        
    def __repr__(self) -> str:
        return f"<Users {self.username}>"