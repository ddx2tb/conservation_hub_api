from pydantic import BaseModel


class JWTToken(BaseModel):
    access_token: str
    token_type: str
