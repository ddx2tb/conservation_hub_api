from typing import Optional

from sqlalchemy.orm import Session

from app.models import User


async def get_user_by_username(username, db: Session) -> Optional[User]:
    sqla_user: Optional[User] = db.query(User).filter(
        User.username == username).first()
    return sqla_user
