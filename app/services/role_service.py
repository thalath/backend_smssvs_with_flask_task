from typing import Optional, List

from ..models import Permission
from ..models  import Role
from extensions import db

class RoleService:
    
    @staticmethod
    def get_all_roles() -> List[Role]:
        return Role.query.order_by(Role.name.asc()).all()

    @staticmethod
    def get_role_by_id(role_id: int) -> Optional[Role]:
        return Role.query.get(role_id)
    
    @staticmethod
    def create_role(data: dict, permission_ids: Optional[List[int]] = None) -> Role:
        role = Role(
            name=data["name"],
            description=data.get("description") or ""
        )
        
        if permission_ids:
            permissions = db.session.scalars(
                db.select(Permission).filter(
                    Permission.id.in_(permission_ids)
                )
            ).all()
            role.permissions = list(permissions)

        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def update_role(role: Role, data: dict, permission_ids: Optional[List[int]] = None) -> Role:
        role.name =data["name"]
        role.description = data.get("description") or ""

        if permission_ids is not None:
            perms: List[Permission] = []
            if permission_ids:
                perms = db.session.scalars(
                    db.select(Permission).filter(
                        Permission.id.in_(permission_ids)
                    )
                ).all()

            role.permissions = list(perms)

        db.session.commit()
        return role
    
    
    @staticmethod
    def delete_role(role: Role) -> None:
        db.session.delete(role)
        db.session.commit()
    