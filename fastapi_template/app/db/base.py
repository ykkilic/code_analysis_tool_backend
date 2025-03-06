# app/db/base.py
from app.db.base_class import Base
from app.models.cve import CVE
from app.models.project import Project, Analysis, Vulnerability

# Import all models here that should be included in database migrations
# This ensures all models are registered with SQLAlchemy