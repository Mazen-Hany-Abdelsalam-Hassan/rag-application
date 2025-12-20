from pydantic import BaseModel ,Field
from bson.objectid import ObjectId
from typing import Literal
from ..enumeration import Status
class UserSchema(BaseModel):
    """
    This Schema contains every details related to any upload transaction 
    preformed by user
    """
    id:ObjectId=Field(None , alias="_id") ##
    username:str
    file_id:str
    status:Status
    text_encoding:str ## for deduplication
    chunk_size:int
    chunk_overlap:int
    parsing_method:Literal["Naive"]= Field(default="Naive")

    class Config:
        arbitrary_types_allowed=True
