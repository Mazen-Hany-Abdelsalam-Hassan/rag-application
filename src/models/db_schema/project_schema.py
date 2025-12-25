from pydantic import BaseModel ,Field
from datetime import datetime, timezone
from bson.objectid import ObjectId

class ProjectSchema(BaseModel):
    """
    This Schema contains every details related to any upload transaction 
    preformed by user
    """
    id:ObjectId=Field(None , alias="_id") ##
    project_id:str
    file_id:str
    file_hash:str ## for deduplication
    upload_time: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc))
    class Config:
        arbitrary_types_allowed=True

    @classmethod
    def get_index(cls):
        return [
            {"key":[("project_id",1)
                    ,("file_hash",1)],
             "name":"unique_key",
             "unique":True       
                    },

            {
                "key":[
                    ("project_id",1),
                    ("upload_time",-1)],
                "name":"project_id_upload_time",
                "unique":False
            }   
        ]

