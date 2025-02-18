
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from core_app.services import ProcessClaiFile
from core_app.models import get_db, Claim
api_router = APIRouter()

@api_router.post("/upload_claim_file")
async def upload_claim_file(file: UploadFile, db: Session = Depends(get_db)):
    data = ProcessClaiFile().execute(file, db)
    return {"data": data}

@api_router.get("/get_top_10_provider")
async def get_top_10_provider(db: Session = Depends(get_db)):
    """ fetch top 10 provider from db where net fee is highest.
        Info: Instruction are unclear to fetching top 10 provider in instruction.
        assuming as of now fetching record in which net fee is highest
    """
    return db.query(Claim).distinct().order_by(Claim.net_fee.desc()).limit(10).all()
