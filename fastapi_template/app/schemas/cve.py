# app/schemas/cve.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CVEBase(BaseModel):
    cve_id: str
    description: Optional[str]
    published_date: Optional[datetime]
    last_modified_date: Optional[datetime]
    base_score: Optional[float]
    impact_score: Optional[float]
    vector_string: Optional[str]
    severity: Optional[str]
    references: Optional[str]

class CVECreate(CVEBase):
    pass

class CVEUpdate(CVEBase):
    pass

class CVE(CVEBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CVESearchParams(BaseModel):
    keyword: Optional[str]
    severity: Optional[str]
    score_min: Optional[float]
    score_max: Optional[float]