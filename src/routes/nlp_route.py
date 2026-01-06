from fastapi import APIRouter ,status,UploadFile , Request
from fastapi.responses import JSONResponse
from utils import Settings 
from controllers import NaiveIndexing
from typing import List
from  models import (
                    ChunkModel ,
                    ProcessModel,
                    ResponseEnum)
NLP_Route=APIRouter(prefix="/Rag/NLP", 
                    tags=["welcome", "rag"])

@NLP_Route.get("/index/{Project}")
async def index_project(request:Request,
                        Project:str,
                        process_id:str):
    database_client = request.app.Database
    vector_db_client = request.app.vector_DB_client
    embedding_model = request.app.embedding_model
    process_model =  await ProcessModel.init_collection(database_client=database_client)
    chunk_model = await ChunkModel.init_collection(database_client=database_client)
    process = await process_model.find_by_id(process_id)
    
    if not process :
        return JSONResponse(
            {"message":ResponseEnum.PROCESS_NOT_EXIST.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )
        
    
    if  not process.processed:
        return JSONResponse(
            {"message":ResponseEnum.NOT_PROCESSED_YET.value},
            status_code=status.HTTP_400_BAD_REQUEST)

    
    if process.indexed:
        return JSONResponse(
            content={"message":ResponseEnum.FILE_INDEXED_SUCCESSFULLY.value}
        )
    

    chunks = []
    page=1
    while True :
        result = await chunk_model.find_by_process_id(process_id=process_id,page_size=50,page=page)
        if len(result[0])==0:
            break
        page+=1
        chunks.extend(result[0])
    
    nlp_controller = NaiveIndexing(
        process_id = process_id,
        project_name=Project,
        vector_database=vector_db_client)
    
    indexing_done = await nlp_controller.embed(
        chunks_list=chunks,
        embedding_client=embedding_model
                         )
    
    if not indexing_done:
        return JSONResponse({
        "message":ResponseEnum.INDEXING_FAILED.value} , 
    status_code=status.HTTP_400_BAD_REQUEST)
    _ = await process_model.update(id = process_id , processed=1 ,indexed =1)
    return JSONResponse(
            content={'message':ResponseEnum.INDEXED_SUCCESSFULLY.value}
    )
    

    

            



        

@NLP_Route.get("/query/{Project}")
async def query(request:Request,
                Project,
                process_ids:List[str]):
    
    pass
    ##Search without memory 
