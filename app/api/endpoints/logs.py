from fastapi import APIRouter, HTTPException
from app.models.log import Log
from app.services.log_processor import process_log

router = APIRouter()

@router.post("/")
async def receive_log(log: Log):
    try:
        response = process_log(log)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
