from fastapi import APIRouter ,status,UploadFile , Request
from fastapi.responses import JSONResponse 
from utils import Settings 
from controllers import DataLoadingController ,DataProcessingController
import aiofiles
import os
import hashlib
from models import ProcessResponse ,ResponseEnum,ProjectModel
DataRoute =APIRouter(prefix="/Rag", 
                           tags=["welcome", "rag"])
@DataRoute.post("/upload_file/{Project}")
async def file_upload(request:Request,Project:str, file:UploadFile):
    data_controller = DataLoadingController(Project)
    chunk_size = data_controller.environment_variable.CHUNK_SIZE
    file_id =  data_controller.is_valid_file(file)
    hasher = hashlib.sha256()
    if file_id: 
        file_path = os.path.join(data_controller.project_directory,
                                 file_id)
        i = 0
        database_client = request.app.Database
        project_model =  await ProjectModel.init_collection(database_client=database_client)
        async with aiofiles.open(file_path,'wb') as f :
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                if  i == 0:
                   hasher.update(chunk)
                   file_hash = str(hasher.hexdigest())
                   i+=1
                   project,exists = await project_model.insert_project_file_hash(
                                                                project_id=Project,
                                                                file_hash=file_hash,
                                                                file_id=file_id
                                                                )
                   
                   
                if exists :
                    os.remove(file_path)
                    break
                await f.write(chunk)
        
        return JSONResponse(content={"message": ResponseEnum.FILE_UPLOADED_SUCCESSFULLY.value,
                                     "process_id":project.file_id})
    
    return JSONResponse(content={"message": ResponseEnum.FILE_NOT_UPLOADED_SUCCESSFULLY.value} 
                        ,status_code=status.HTTP_400_BAD_REQUEST)
    

@DataRoute.post("/process/{Project}")
async def process(Project:str , process_request:ProcessResponse):
    process_controller = DataProcessingController(user = Project)
    content= process_controller.load_file(process_request.file_id)

    if  not content:
        return JSONResponse(content={"message": ResponseEnum.FILE_PROCESSING_FAIL.value})

    chunks_text,meta_data = process_controller.chunk_file(
        loaded_pdf=content,
        chunk_size=process_request.chunk_size,
        chunk_overlap=process_request.chunk_overlap)
    
    #return chunks_text , meta_data
     
    return JSONResponse({"content":ResponseEnum.FILE_PROCESSING_SUCCESS.value})
    
