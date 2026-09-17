import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.user import User, UserSession
from app.schemas.auth import UserCreate


class AuthService:
    @staticmethod
    def create_user(database: Session, payload: UserCreate) -> User:
        user = User(email=str(payload.email).lower(), password_hash=AuthService._hash_password(payload.password))
        database.add(user)
        try:
            database.commit()
        except IntegrityError as error:
            database.rollback()
            raise ValueError("A user with this email already exists.") from error
        database.refresh(user)
        return user

    @staticmethod
    def authenticate(database: Session, email: str, password: str) -> User | None:
        user = database.scalar(select(User).where(User.email == email.lower()))
        if user is None or not AuthService._verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_session(database: Session, user: User) -> tuple[UserSession, str]:
        access_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(minutes=get_settings().session_expire_minutes)
        session = UserSession(user_id=user.id, token_hash=AuthService._hash_token(access_token), expires_at=expires_at)
        database.add(session)
        database.commit()
        database.refresh(session)
        return session, access_token

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
        return f"{salt.hex()}${digest.hex()}"

    @staticmethod
    def _verify_password(password: str, stored_hash: str) -> bool:
        salt_hex, digest_hex = stored_hash.split("$", maxsplit=1)
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 600_000)
        return hmac.compare_digest(candidate.hex(), digest_hex)

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
