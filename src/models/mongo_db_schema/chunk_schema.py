from pydantic import BaseModel ,Field
from bson.objectid import ObjectId
from datetime import datetime, timezone

class ChunkSchema(BaseModel):
    """
    Collect the project chunks
    """
    id:ObjectId=Field(None , alias="_id")
    process_id:str
    chunk_text:str
    chunk_meta_data:dict
    chunk_order:int
    upload_time: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc))


    class Config:
        arbitrary_types_allowed=True

    @classmethod
    def get_index(cls):
        return [
             {
            "key":[("process_id" , 1)],  
             "name":"process_id",
             "unique":False},                       
            ]

        

    