from typing import List, Optional 
from ..models.permission import Permission
from extensions import db


class PermissionService:
    @staticmethod
    def get_all_permissions() -> List[Permission]:
        return Permission.query.order_by(Permission.code.asc()).all()

    @staticmethod
    def get_permission_by_id(perm_id: int) -> Optional[Permission]:
        perms = Permission.query.get(perm_id)
        return perms
    
    @staticmethod
    def create_permission(data: dict) -> Permission:
        perm = Permission(
            code=data['code'],
            name=data['name'],
            module=data.get("module", "General"),
            description=data.get("description") or ""
        )
        
        db.session.add(perm)
        db.session.commit()
        return perm

    @staticmethod
    def update_permission(perm: Permission, data: dict) -> Permission:
        perm.code=data['code']
        perm.name=data['name']
        perm.module=data.get("module", "General")
        perm.description=data.get("description") or ""

        db.session.commit()
        return perm

    @staticmethod
    def delete_permission(perm: Permission) -> None:
        db.session.delete(perm)
        db.session.commit()
        