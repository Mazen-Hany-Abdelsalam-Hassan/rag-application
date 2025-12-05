from fastapi import APIRouter , Depends,status
from fastapi.responses import JSONResponse 

from utils import Settings , get_settings
base_route =APIRouter(prefix="", tags=["welcome", "rag"])

@base_route.get("/")
async def base(app_setting:Settings=Depends(get_settings)):
    return JSONResponse(content= 
                        {"Name":app_setting.APP_NAME,
                        "Version":app_setting.VERSION},
                        status_code=status.HTTP_200_OK )
