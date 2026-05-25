from argon2 import PasswordHasher
import secrets

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, password)
    except Exception:
        return False

def generate_token() -> str:
    return secrets.token_urlsafe(32)