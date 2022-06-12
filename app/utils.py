import re
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return password_context.hash(password)


def verify(pswd, hashed_pswd):
    return password_context.verify(pswd, hashed_pswd)
