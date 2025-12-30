from pydantic import BaseModel, Field
from typing import Literal
class ProcessOverviewRequest(BaseModel):
    file_id:str=None
    processed:Literal[0,1]=1
    indexed:Literal[0,1]=0
    page_size:int= Field(...,gt=0 , le=100)
    page:int =Field(...,gt=0)