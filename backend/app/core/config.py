import os

from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.config import OAuth2Config
from social_core.backends.google import GoogleOAuth2


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@db:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OAUTH2_CONFIG = OAuth2Config(
        jwt_secret=os.environ.get('JWT_SECRET', 'your-jwt-secret'),
        clients=[
            OAuth2Client(
                backend=GoogleOAuth2,
                client_id=os.environ.get('GOOGLE_CLIENT_ID'),
                client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
                redirect_uri=os.environ.get('GOOGLE_REDIRECT_URI'),
                scope=['openid', 'email', 'profile'],
            )
        ]
    )
