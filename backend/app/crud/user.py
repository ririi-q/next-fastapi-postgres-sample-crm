from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.company import Company
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.associations and user.associations.companies:
        companies = db.query(Company).filter(Company.id.in_(user.associations.companies)).all()
        db_user.companies = companies
        db.commit()

    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate, current_user: User):
    db_user = get_user(db, user_id)
    if db_user and db_user.id == current_user.id:
        update_data = user_update.dict(exclude_unset=True)
        associations = update_data.pop('associations', None)

        # パスワードの更新処理
        if 'password' in update_data:
            hashed_password = get_password_hash(update_data['password'])
            update_data['hashed_password'] = hashed_password
            del update_data['password']

        for key, value in update_data.items():
            setattr(db_user, key, value)

        if associations:
            # associationsがPydanticモデルの場合
            if hasattr(associations, 'companies'):
                company_ids = associations.companies
            # associationsが辞書の場合
            elif isinstance(associations, dict) and 'companies' in associations:
                company_ids = associations['companies']
            else:
                company_ids = None

            if company_ids:
                companies = db.query(Company).filter(Company.id.in_(company_ids)).all()
                db_user.companies = companies

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int, current_user: User):
    db_user = get_user(db, user_id)
    if db_user and db_user.id == current_user.id:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
