import bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(pwd: str):
    return pwd_context.hash(secret=pwd)


def verify_pwd(pwd: str, hashed):
    return pwd_context.verify(secret=pwd, hash=hashed)
