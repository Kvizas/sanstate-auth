import time
from db_models.account import Account
import jwt
import os


def get_jwt(acc: Account):
    return jwt.encode(
        {"id": acc.id, "exp": int(time.time() + 60 * 60)},
        os.environ.get("JWT_SECRET"),
    ).decode("utf-8")
