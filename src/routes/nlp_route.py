from fastapi import APIRouter ,status,UploadFile , Request
from fastapi.responses import JSONResponse
from utils import Settings 
from controllers import NaiveIndexing,NaiveGeneration
from typing import List
import asyncio
from  models import (ChunkModel ,
                    ProcessModel,
                    ResponseEnum,
                    DataIndexingRequest,
                    SimpleQuestionRequest)

NLP_Route=APIRouter(prefix="/Rag/NLP", 
                    tags=["welcome", "rag"])

@NLP_Route.post("/index/{Project}")
async def index_project(request:Request,
                        Project:str,
                        indexing_request:DataIndexingRequest):
    process_id = indexing_request.process_id
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
            content={"message":ResponseEnum.INDEXED_SUCCESSFULLY.value}
        )
    
    nlp_controller = NaiveIndexing(
        process_id = process_id,
        project_name=Project,
        vector_database=vector_db_client)


    page=1
    while True :
        result = await chunk_model.find_by_process_id(process_id=process_id,page_size=200,page=page)
        if len(result[0])==0:
            break
        indexing_done = await nlp_controller.embed(
        chunks_list=result[0],
        embedding_client=embedding_model,
        use_index=True)
        await asyncio.sleep(1)
        page+=1
        
    
    
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
                Project:str,
                question_request:SimpleQuestionRequest):
    vector_db_client = request.app.vector_DB_client
    embedding_model = request.app.embedding_model
    llm_model = request.app.llm_model

    answer_generation = NaiveGeneration(
                    project_id=Project,
                    process_ids=question_request.process_ids,
                    embedding_model=embedding_model,
                    llm_model=llm_model,
                    vector_database_client=vector_db_client)
    
    answer , chunks = answer_generation.search_and_generate(question=question_request.question ,
                             topk=question_request.topk)
    return JSONResponse({"response":answer , 
                        "chunks":chunks})
