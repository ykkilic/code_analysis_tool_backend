# app/api/api_v1/endpoints/cve.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.cve import CVE, CVECreate, CVEUpdate, CVESearchParams
from app.services.nvd_api import NVDAPIService

router = APIRouter()

@router.get("/", response_model=List[CVE])
async def list_cves(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: CVESearchParams = Depends()
):
    query = db.query(CVE)
    
    if search.keyword:
        query = query.filter(CVE.description.ilike(f"%{search.keyword}%"))
    if search.severity:
        query = query.filter(CVE.severity == search.severity)
    if search.score_min is not None:
        query = query.filter(CVE.base_score >= search.score_min)
    if search.score_max is not None:
        query = query.filter(CVE.base_score <= search.score_max)
        
    return query.offset(skip).limit(limit).all()

@router.post("/update-database")
async def update_cve_database(db: Session = Depends(get_db)):
    nvd_service = NVDAPIService()
    try:
        await nvd_service.update_cve_database(db)
        return {"message": "CVE database updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{cve_id}", response_model=CVE)
async def get_cve(cve_id: str, db: Session = Depends(get_db)):
    cve = db.query(CVE).filter(CVE.cve_id == cve_id).first()
    if not cve:
        raise HTTPException(status_code=404, detail="CVE not found")
    return cve