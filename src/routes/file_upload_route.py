from fastapi import APIRouter ,status,UploadFile
from fastapi.responses import JSONResponse 
from utils import Settings 
from controllers import DataLoadingController
import aiofiles
FileUploadRoute =APIRouter(prefix="/Rag/upload_file", 
                           tags=["welcome", "rag"])
@FileUploadRoute.post("/{User}")
async def file_upload(User:str, file:UploadFile):
    data_controller = DataLoadingController(User)
    chunk_size = data_controller.environment_variable.CHUNK_SIZE
    response , file_path =  data_controller.is_valid_file(file)
    if file_path: 
        async with aiofiles.open(file_path,'wb') as f :
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                await f.write(chunk)

        
        return JSONResponse(content={"message": response})
    
    return JSONResponse(content={"message": response} 
                        ,status_code=status.HTTP_400_BAD_REQUEST)
    
