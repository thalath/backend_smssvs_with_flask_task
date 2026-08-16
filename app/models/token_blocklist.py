from extensions import db, jwt
from datetime import datetime, timezone


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))



@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token = db.session.scalar(
        db.select(TokenBlocklist).filter(TokenBlocklist.jti==jti)
    )
    
    return token is not None