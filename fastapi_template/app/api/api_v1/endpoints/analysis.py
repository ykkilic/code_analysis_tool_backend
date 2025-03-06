# app/api/api_v1/endpoints/analysis.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.schemas.project import Analysis, AnalysisCreate, Vulnerability, VulnerabilityCreate

router = APIRouter()

async def run_code_analysis(
    db: Session,
    analysis_id: int,
    project_id: int
):
    # Simulated code analysis process
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        return
    
    try:
        # Perform code analysis here
        # This is a placeholder for the actual code analysis implementation
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()
        
        # Example vulnerability creation
        vulnerability = Vulnerability(
            analysis_id=analysis_id,
            file_path="/example/path.py",
            line_number=42,
            severity="HIGH",
            description="Example vulnerability",
            cve_id=1  # Reference to actual CVE
        )
        db.add(vulnerability)
        
    except Exception as e:
        analysis.status = "failed"
        db.add(analysis)
    
    db.commit()

@router.post("/{project_id}/analyze", response_model=Analysis)
async def start_analysis(
    project_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Create new analysis record
    analysis = Analysis(
        project_id=project_id,
        status="pending",
        started_at=datetime.utcnow()
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    # Start analysis in background
    background_tasks.add_task(run_code_analysis, db, analysis.id, project_id)
    
    return analysis

@router.get("/{project_id}/analyses", response_model=List[Analysis])
async def list_analyses(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    analyses = db.query(Analysis)\
        .filter(Analysis.project_id == project_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return analyses

@router.get("/analyses/{analysis_id}", response_model=Analysis)
async def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.get("/analyses/{analysis_id}/vulnerabilities", response_model=List[Vulnerability])
async def list_vulnerabilities(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    vulnerabilities = db.query(Vulnerability)\
        .filter(Vulnerability.analysis_id == analysis_id)\
        .all()
    return vulnerabilities