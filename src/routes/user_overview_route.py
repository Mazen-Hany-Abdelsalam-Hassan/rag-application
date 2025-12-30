from fastapi import APIRouter 
from fastapi.responses import JSONResponse 
from fastapi import Request
from models import (
                    ProjectModel,
                    UploadedFileOverviewRequest,
                    ProcessModel,
                    ProcessOverviewRequest)
UserOverviewRoute = APIRouter(prefix="/Rag/UserOverview", tags=["welcome", "rag"])

@UserOverviewRoute.get("/uploaded_file/{Project}")
async def show_uploaded_file(request:Request
                             ,Project:str,
                             overview_request:UploadedFileOverviewRequest):
    
    
    database_client = request.app.Database
    project_model =  await ProjectModel.init_collection(
        database_client=database_client)
    results , total_pages = await project_model.search_by_project(project_id=Project,
            page=overview_request.page,
            page_size=overview_request.page_size)
    
    results = [
        {"file":result.file_id , 
         "upload_time":result.upload_time.strftime("%b %d, %Y · %I:%M %p")}
        for result in results 

    ]
    message = {"available_data":results,
               "total_pages":total_pages}

    return JSONResponse(content=message)
    

@UserOverviewRoute.get("/process/{Project}")
async def show_process(
    request:Request,
    Project:str,
    process_overview:ProcessOverviewRequest):

    database_client = request.app.Database
    process_model = await ProcessModel.init_collection(database_client)

    if process_overview.file_id is None:
        results , total_pages = await process_model.find_by_project(
        project_id=Project,
        processed=process_overview.processed,
        indexed = process_overview.indexed,
        page_size=process_overview.page_size,
        page=process_overview.page)
    
    else: 
        results , total_pages = await process_model.find_by_project_file_id(
            file_id=process_overview.file_id,
            project_id=Project,
            processed=process_overview.processed,
            indexed = process_overview.indexed,
            page_size=process_overview.page_size,
            page=process_overview.page)
    
    results = [
        {"file":result.file_id , 
         "processing_parameter":result.processing_parameter ,
         "upload_time":result.upload_time.strftime("%b %d, %Y · %I:%M %p")}
        for result in results ]
    message = {"available_data":results,
               "total_pages":total_pages}

    return JSONResponse(content=message)
    
    
    

        

    
    
    
    pass