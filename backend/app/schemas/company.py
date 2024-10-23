import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


def validate_domain(domain: str) -> str:
    pattern = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    if not re.match(pattern, domain):
        raise ValueError('Invalid domain format')
    return domain

class CompanyBase(BaseModel):
    name: str
    domain: str = Field(..., description="Company's website domain")

    # ドメインのバリデーション
    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v):
        pattern = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid domain format')
        return v

class AssociationCreate(BaseModel):
    users: Optional[List[int]] = None
    # 他のテーブルの関連付けも同様に追加できます

class CompanyCreate(CompanyBase):
    associations: Optional[AssociationCreate] = None

class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    domain: Optional[str] = None
    associations: Optional[AssociationCreate] = None

class CompanyInDB(CompanyBase):
    id: int
    users: List['UserBase'] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 循環インポートを避けるため、UserInDBの型ヒントを文字列で指定しています
from .user import UserBase


