from datetime import timedelta

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_active_user
from app.core import security
from app.core.config import Config
from app.db.session import get_db

router = APIRouter()


oauth = OAuth()

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

## ログイン
@router.post("/token", response_model=schemas.user.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = security.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=schemas.user.Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = security.decode_refresh_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    user = crud.user.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token = security.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.user.UserInDB)
async def read_users_me(current_user: models.user.User = Depends(get_current_active_user)):
    print(current_user)
    return current_user

@router.get("/check-auth", response_model=schemas.user.UserInDB)
async def check_auth(current_user: models.user.User = Depends(get_current_active_user)):
    return current_user

## Google OAuth2
@router.get("/google-oauth2/authorize")
async def google_oauth2_authorize(request: Request):
    redirect_uri = request.url_for('google_oauth2_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google-oauth2/callback")
async def google_oauth2_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        print(token)
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
        user_info = resp.json()
        print(user_info)

        if not user_info:
            raise HTTPException(status_code=400, detail="Google authentication failed")

        db_user = crud.user.get_user_by_email(db, email=user_info['email'])
        if not db_user:
            # 新しいユーザーを作成
            user_in = schemas.user.UserCreate(
                email=user_info['email'],
                name=user_info['name'],
                password=security.get_password_hash(token['access_token']),  # 一時的なパスワード
                is_active=True
            )
            db_user = crud.user.create_user(db, user_in)

        # プロバイダー情報を更新
        db_user.provider = "google"
        db_user.provider_id = user_info['sub']
        db.commit()

        # JWTトークンを生成
        access_token = security.create_access_token(data={"sub": db_user.email})
        return RedirectResponse(url=f"{Config.FRONTEND_URL}/auth/callback?token={access_token}")
    except Exception as e:
        print(f"Error in Google OAuth callback: {str(e)}")
        raise HTTPException(status_code=400, detail="Google authentication failed")



