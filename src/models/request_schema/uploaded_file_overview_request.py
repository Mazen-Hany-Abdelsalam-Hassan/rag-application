from pydantic import BaseModel, Field

class UploadedFileOverviewRequest(BaseModel):
    page_size:int= Field(...,gt=0 , le=100)
    page:int =Field(...,gt=0)