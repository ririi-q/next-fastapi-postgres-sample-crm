from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def get_company_by_domain(db: Session, domain: str):
    return db.query(Company).filter(Company.domain == domain).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: CompanyCreate):
    db_company = Company(name=company.name, domain=company.domain)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    if company.associations and company.associations.users:
        users = db.query(User).filter(User.id.in_(company.associations.users)).all()
        db_company.users = users
        db.commit()

    return db_company

def update_company(db: Session, company_id: int, company_update: CompanyUpdate):
    db_company = get_company(db, company_id)
    if db_company:
        update_data = company_update.dict(exclude_unset=True)
        associations = update_data.pop('associations', None)
        for key, value in update_data.items():
            setattr(db_company, key, value)

        if associations and associations.users:
            users = db.query(User).filter(User.id.in_(associations.users)).all()
            db_company.users = users

        db.add(db_company)
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company

