# app/models/project.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
import enum

class LanguageType(str, enum.Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    SQL = "sql"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    language = Column(Enum(LanguageType))
    repository_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    analyses = relationship("Analysis", back_populates="project")

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    project = relationship("Project", back_populates="analyses")
    vulnerabilities = relationship("Vulnerability", back_populates="analysis")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    cve_id = Column(Integer, ForeignKey("cves.id"))
    file_path = Column(String)
    line_number = Column(Integer)
    severity = Column(String)
    description = Column(Text)
    remediation = Column(Text)
    
    analysis = relationship("Analysis", back_populates="vulnerabilities")
    cve = relationship("CVE", back_populates="vulnerabilities")