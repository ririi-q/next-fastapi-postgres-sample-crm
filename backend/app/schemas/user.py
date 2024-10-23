from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr

class AssociationCreate(BaseModel):
    companies: Optional[List[int]] = None
    # 他のテーブルの関連付けも同様に追加できます
    # other_tables: Optional[List[int]] = None

class UserCreate(UserBase):
    password: str
    associations: Optional[AssociationCreate] = None

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    associations: Optional[AssociationCreate] = None

class UserInDB(UserBase):
    id: int
    hashed_password: str
    companies: List['CompanyBase'] = []
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool
    class Config:
        from_attributes = True

# 循環インポートを避けるために、ここでCompanyInDBをインポートします
from .company import CompanyBase


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
