# app/schemas/project.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class LanguageType(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    SQL = "sql"

class ProjectBase(BaseModel):
    name: str
    description: Optional[str]
    language: LanguageType
    repository_url: Optional[str]

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class VulnerabilityBase(BaseModel):
    file_path: str
    line_number: int
    severity: str
    description: str
    remediation: Optional[str]

class VulnerabilityCreate(VulnerabilityBase):
    analysis_id: int
    cve_id: int

class Vulnerability(VulnerabilityBase):
    id: int
    analysis_id: int
    cve_id: int

    class Config:
        orm_mode = True

class AnalysisBase(BaseModel):
    project_id: int
    status: str

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: int
    started_at: datetime
    completed_at: Optional[datetime]
    vulnerabilities: List[Vulnerability] = []

    class Config:
        orm_mode = True