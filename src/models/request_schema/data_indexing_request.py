from pydantic import BaseModel

class DataIndexingRequest(BaseModel):
    process_id:str
