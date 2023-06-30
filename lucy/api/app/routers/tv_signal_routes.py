from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..models.signal_incoming import SignalIncoming
from app.services.signal_service import SignalService

router = APIRouter()

@router.post("/signal", status_code=status.HTTP_201_CREATED)
def post(signal: SignalIncoming):
    success, message = SignalService().handle(signal)
    resp =  {"success": success, "message": message}    
    if success:
        return resp
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=resp)
    