
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Simple in-memory claim store
db_claims = {}

class Procedure(BaseModel):
    code: str
    total_price: float

class Claim(BaseModel):
    claim_id: str
    patient_id: str
    provider_id: str
    policy_id: str
    diagnosis_codes: List[str]
    procedure_codes: List[Procedure]
    submitted_at: str
    status: Optional[str] = "PENDING"
    status_reason: Optional[str] = "Waiting for review"

@app.post("/claims/submit")
def submit_claim(claim: Claim):
    if claim.claim_id in db_claims:
        raise HTTPException(status_code=400, detail="Duplicate claim_id")
    claim.status = "APPROVED"
    claim.status_reason = "Auto-approved for testing"
    db_claims[claim.claim_id] = claim
    return {"message": "Claim received", "status": claim.status, "reason": claim.status_reason}
