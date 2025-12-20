from pydantic import BaseModel
from typing import Optional
class ProcessResponse(BaseModel):
    file_id:str
    chunk_size:Optional[int] = 200   
    chunk_overlap:Optional[int] =40
    do_reset:Optional[int]=0

    