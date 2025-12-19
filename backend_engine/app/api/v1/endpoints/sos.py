from fastapi import APIRouter

router = APIRouter()

@router.post("/sos")
async def trigger_sos():
    return {"status": "SOS triggered"}
