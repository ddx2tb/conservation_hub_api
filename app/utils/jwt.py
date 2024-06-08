from datetime import timedelta, datetime, timezone
from typing import Dict, Any, Optional

import jwt

from app.settings import default_settings


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    data.update({"exp": expire})

    encoded_jwt = jwt.encode(data, default_settings.SECRET_KEY, algorithm=default_settings.ALGORITHM)

    return encoded_jwt
