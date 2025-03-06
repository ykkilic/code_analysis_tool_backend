# app/models/cve.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class CVE(Base):
    __tablename__ = "cves"
    
    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    published_date = Column(DateTime)
    last_modified_date = Column(DateTime)
    base_score = Column(Float)
    impact_score = Column(Float)
    vector_string = Column(String)
    severity = Column(String)
    references = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    vulnerabilities = relationship("Vulnerability", back_populates="cve")