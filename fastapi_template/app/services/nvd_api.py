# app/services/nvd_api.py
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
from app.core.config import settings
from app.schemas.cve import CVECreate

class NVDAPIService:
    def __init__(self):
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.api_key = settings.NVD_API_KEY
        self.headers = {"apiKey": self.api_key} if self.api_key else {}

    async def fetch_cves(self, 
                        last_modified_start: Optional[datetime] = None,
                        page_size: int = 100) -> List[CVECreate]:
        params = {
            "resultsPerPage": page_size,
        }
        
        if last_modified_start:
            params["lastModStartDate"] = last_modified_start.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.base_url,
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                cves = []
                for vuln in data.get("vulnerabilities", []):
                    cve_item = vuln.get("cve", {})
                    metrics = cve_item.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {})
                    
                    cve = CVECreate(
                        cve_id=cve_item.get("id"),
                        description=cve_item.get("descriptions", [{}])[0].get("value"),
                        published_date=datetime.strptime(cve_item.get("published"), "%Y-%m-%dT%H:%M:%S.%fZ"),
                        last_modified_date=datetime.strptime(cve_item.get("lastModified"), "%Y-%m-%dT%H:%M:%S.%fZ"),
                        base_score=metrics.get("baseScore"),
                        impact_score=metrics.get("impactScore"),
                        vector_string=metrics.get("vectorString"),
                        severity=metrics.get("baseSeverity"),
                        references=",".join([ref.get("url") for ref in cve_item.get("references", [])])
                    )
                    cves.append(cve)
                
                return cves

        except httpx.HTTPError as e:
            raise Exception(f"Error fetching CVEs from NVD: {str(e)}")

    async def update_cve_database(self, db):
        # Get last update time from database or default to 24 hours ago
        last_update = datetime.utcnow() - timedelta(hours=24)
        cves = await self.fetch_cves(last_modified_start=last_update)
        
        for cve_data in cves:
            # Update or create CVE records in database
            await db.execute(
                """
                INSERT INTO cves (cve_id, description, published_date, last_modified_date,
                                base_score, impact_score, vector_string, severity, references)
                VALUES (:cve_id, :description, :published_date, :last_modified_date,
                        :base_score, :impact_score, :vector_string, :severity, :references)
                ON CONFLICT (cve_id) DO UPDATE SET
                    description = EXCLUDED.description,
                    last_modified_date = EXCLUDED.last_modified_date,
                    base_score = EXCLUDED.base_score,
                    impact_score = EXCLUDED.impact_score,
                    vector_string = EXCLUDED.vector_string,
                    severity = EXCLUDED.severity,
                    references = EXCLUDED.references,
                    updated_at = CURRENT_TIMESTAMP
                """,
                cve_data.dict()
            )