from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import crud

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードの検証を行う。

    プレーンテキストのパスワードとハッシュ化されたパスワードを比較し、
    パスワードが正しいかどうかを判断する。

    Args:
        plain_password (str): 検証するプレーンテキストのパスワード。
        hashed_password (str): データベースに保存されているハッシュ化されたパスワード。

    Returns:
        bool: パスワードが正しい場合はTrue、そうでない場合はFalse。

    Example:
        >>> verify_password("mypassword", "$2b$12$...")
        True
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """パスワードのハッシュ化を行う。

    プレーンテキストのパスワードをハッシュ化し、ハッシュ化されたパスワードを返す。

    Args:
        password (str): ハッシュ化するプレーンテキストのパスワード。

    Returns:
        str: ハッシュ化されたパスワード。

    Example:
        >>> get_password_hash("mypassword")
        "$2b$12$..."
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """アクセストークンの作成を行う。

    データベースに保存されているユーザー情報をもとに、アクセストークンを作成する。

    Args:
        data (dict): ユーザー情報を含むデータ。
        expires_delta (Optional[timedelta]): トークンの有効期限。

    Returns:
        str: アクセストークン。

    Example:
        >>> create_access_token({"sub": "user@example.com"})
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzI4MzIwMDAwLCJpYXQiOjE3MjgzMTY0MDB9...."
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate(db: Session, *, email: str, password: str):
    """ユーザーの認証を行う。

    データベースに保存されているユーザー情報をもとに、ユーザーが存在し、
    かつパスワードが正しいかどうかを判断する。

    Args:
        db (Session): データベースセッション。
        email (str): ユーザーのメールアドレス。
        password (str): ユーザーのパスワード。

    Returns:
        User: ユーザー情報。

    Example:
        >>> authenticate(db, email="user@example.com", password="mypassword")
        <User object>
    """
    user = crud.user.get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def decode_access_token(token: str):
    """アクセストークンのデコードを行う。

    アクセストークンをデコードし、ペイロードを返す。

    Args:
        token (str): デコードするアクセストークン。

    Returns:
        dict: デコードされたペイロード。
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """リフレッシュトークンの作成を行う。

    データベースに保存されているユーザー情報をもとに、リフレッシュトークンを作成する。

    Args:
        data (dict): ユーザー情報を含むデータ。
        expires_delta (Optional[timedelta]): トークンの有効期限。

    Returns:
        str: リフレッシュトークン。
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # リフレッシュトークンの有効期限を7日に設定
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_refresh_token(token: str):
    """リフレッシュトークンのデコードを行う。

    リフレッシュトークンをデコードし、ペイロードを返す。

    Args:
        token (str): デコードするリフレッシュトークン。

    Returns:
        dict: デコードされたペイロード。
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
