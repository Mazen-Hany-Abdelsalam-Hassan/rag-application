from pydantic import BaseModel

class DataProcessingRequest(BaseModel):
    file_id:str
    processing_method:str
    processing_parameter:dict