import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext


JWT_ALGORITHM = "HS256"
# Use pbkdf2_sha256 for compatibility on Python 3.13 environments.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def _get_db_path() -> str:
    return os.getenv("AUTH_DB_PATH", "./adk_users.db")


def init_auth_db() -> None:
    db_path = _get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def _get_conn() -> sqlite3.Connection:
    return sqlite3.connect(_get_db_path())


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_user(email: str, password: str) -> None:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
            (email, hash_password(password), datetime.utcnow().isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def get_user_by_email(email: str) -> Optional[dict]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        if not row:
            return None
        return {"id": row[0], "email": row[1], "password_hash": row[2]}
    finally:
        conn.close()


def _token_minutes() -> int:
    try:
        return int(os.getenv("JWT_EXPIRES_MINUTES", "1440"))
    except ValueError:
        return 1440


def create_access_token(email: str, expires_minutes: Optional[int] = None) -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not set")
    minutes = expires_minutes if expires_minutes is not None else _token_minutes()
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[str]:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not set")
    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
