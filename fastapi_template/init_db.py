# init_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from app.core.config import settings
from app.db.base_class import Base
from app.models.cve import CVE
from app.models.project import Project, Analysis, Vulnerability
from app.services.nvd_api import NVDAPIService

def init_db():
    # Create database engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")

        # Create SessionLocal class for database sessions
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Initialize CVE database
        db = SessionLocal()
        nvd_service = NVDAPIService()
        
        # Run initial CVE fetch in async context
        async def fetch_initial_cves():
            try:
                await nvd_service.update_cve_database(db)
                print("Initial CVE data fetched successfully!")
            except Exception as e:
                print(f"Error fetching initial CVE data: {str(e)}")
            finally:
                db.close()

        # Run the async function
        asyncio.run(fetch_initial_cves())
        
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    print("Initializing database...")
    init_db()