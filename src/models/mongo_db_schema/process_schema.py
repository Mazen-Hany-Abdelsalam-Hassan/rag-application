from pydantic import BaseModel ,Field
from datetime import datetime, timezone
from bson.objectid import ObjectId

class ProcessSchema(BaseModel):
    """
    This Schema contains every details related to any upload transaction 
    preformed by user
    """
    id:str=Field(..., alias="_id")   ## instead of making mongo index I will make 
    file_id:str                         ## my own index
    project_id:str
    processing_method:str="Simple" #the processing method
    processed:int=0 ## not processed yet 0  
    indexed:int=0 ## not indexed yet 0 
    processing_parameter:dict
    upload_time:datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        arbitrary_types_allowed=True
    @classmethod
    def get_index(cls):
        return [
            {
                "key":[("project_id",1)  ##Processed or not
                    ,("file_id",1),
                    ("upload_time",-1)],  ##Indexed or not
                                      ##processing type
             "name":"project_id_file_id_index_sorted",
             "unique":False},                       
             ]

