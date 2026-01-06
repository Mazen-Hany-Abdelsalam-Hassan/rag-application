from fastapi import APIRouter ,status,UploadFile , Request
from fastapi.responses import JSONResponse 
from utils import Settings 
from controllers import DataLoadingController,DataProcessor
import aiofiles
import os
import hashlib
from models import (ProjectModel , 
                    ResponseEnum,
                    DataProcessingRequest,
                    ProcessModel,
                    ProcessSchema,
                    ChunkModel)
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
        #print(await project_model.search_by_project(project_id=Project , page=1))
        return JSONResponse(content={"message": ResponseEnum.FILE_UPLOADED_SUCCESSFULLY.value,
                                     "process_id":project.file_id})
    
    return JSONResponse(content={"message": ResponseEnum.FILE_NOT_UPLOADED_SUCCESSFULLY.value} 
                        ,status_code=status.HTTP_400_BAD_REQUEST)
    

@DataRoute.post("/process/{Project}")
async def process( request:Request,
                  Project:str,
                 process_request:DataProcessingRequest):
    #####Database Interaction
    database_client = request.app.Database
    process_model =  await ProcessModel.init_collection(database_client=database_client)
    ######

    ##### Database Interaction
    chunk_model = await ChunkModel.init_collection(database_client=database_client)
    #####
    
    #####Factory  Select your class
    ProcessController = DataProcessor.load_processor(
        processing_method=process_request.processing_method)
    if not ProcessController:
        return JSONResponse(content={"message":
                ResponseEnum.WRONG_PROCESSING_METHOD.value},
                status_code=status.HTTP_400_BAD_REQUEST)
    ######
    ######  Factory initiate object
    process_controller = ProcessController(
    project=Project,
    file_id = process_request.file_id,
    processing_parameter=process_request.processing_parameter)
    #######
    
    ####### Validator
    if not process_controller.valid_processing:
        return JSONResponse(content={"message": ResponseEnum.WRONG_PROCESSING_PARAMETER.value},
                      status_code=status.HTTP_400_BAD_REQUEST)
    
    if  not process_controller.file_exist:
        return JSONResponse(content={"message": ResponseEnum.FILE_PROCESSING_FAIL.value},
                      status_code=status.HTTP_400_BAD_REQUEST)
    
    #######
    ####### insert to DB 
    FingerPrint = process_controller.create_fingerprint()
    
    process_schema = ProcessSchema(_id = FingerPrint , 
                  file_id=process_request.file_id,
                  project_id=Project,
                  processing_pipeline=process_request.processing_method,
                  processing_parameter= process_request.processing_parameter
                  )
    
    

    exist = await process_model.insert_process_if_not_exist(
                process=process_schema)


    ####### Data Processing
    
    if not exist:
        Content= process_controller.load_file()
        Chunks = process_controller.chunk_file(Content)
        _= await chunk_model.insert_chunks(chunks=Chunks)
        _ = await process_model.update(id = FingerPrint,processed = 1, indexed = 0)

        
    
    return JSONResponse({"content":ResponseEnum.FILE_PROCESSING_SUCCESS.value,
                         "process_id" :FingerPrint})