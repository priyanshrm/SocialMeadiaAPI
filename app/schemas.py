from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# REQUEST USER


class UserReq(BaseModel):
    username: str
    email: EmailStr
    password: str


# RESPONSE USER


class UserRes(BaseModel):
    username: str
    email: EmailStr
    id: int
    date_joined: datetime
    # password: str

    class Config:
        orm_mode = True

# REQUEST POST


class PostReq(BaseModel):
    title: str
    content: str
    published: bool = True

# RESPONSE POST


class PostRes(BaseModel):
    title: str
    content: str
    published: bool
    id: int
    created_at: datetime
    usr_id: int
    # user: UserResponse2

    class Config:
        orm_mode = True

# REQUEST VOTE


class VoteReq(BaseModel):
    post_id: int
    dir: conint(le=1)  # less than or equal to 1

# RESPONSE VOTE


class VoteRes(VoteReq):
    pass


# TOKEN

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
