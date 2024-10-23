from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.company.CompanyInDB)
def create_company(company: schemas.company.CompanyCreate, db: Session = Depends(get_db)):
    db_company = crud.company.get_company_by_domain(db, domain=company.domain)
    if db_company:
        raise HTTPException(status_code=400, detail="Domain already registered")
    return crud.company.create_company(db=db, company=company)

@router.get("/", response_model=List[schemas.company.CompanyInDB])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    companies = crud.company.get_companies(db, skip=skip, limit=limit)
    return companies

@router.get("/{company_id}", response_model=schemas.company.CompanyInDB)
def read_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud.company.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.put("/{company_id}", response_model=schemas.company.CompanyInDB)
def update_company(company_id: int, company_update: schemas.company.CompanyUpdate, db: Session = Depends(get_db)):
    db_company = crud.company.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.company.update_company(db, company_id=company_id, company_update=company_update)

@router.delete("/{company_id}", response_model=schemas.company.CompanyInDB)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud.company.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.company.delete_company(db, company_id=company_id)
