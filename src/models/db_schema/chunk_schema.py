from pydantic import BaseModel ,Field
from bson.objectid import ObjectId
from typing import Literal
class ChunkSchema(BaseModel):
    """
    Collect the project chunks
    """
    id:ObjectId=Field(None , alias="_id")
    file_id:str
    chunk_text:str
    chunk_metadata:dict 
    chunk_order:int

    class Config:
        arbitrary_types_allowed=True


    