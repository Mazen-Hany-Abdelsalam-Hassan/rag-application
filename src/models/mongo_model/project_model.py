from motor.motor_asyncio import (AsyncIOMotorDatabase ,
                                AsyncIOMotorCollection)
from ..mongo_db_schema import ProjectSchema
from .base_model import BaseDataModel
class ProjectModel(BaseDataModel):
    def __init__(self, collection:AsyncIOMotorCollection):
        super().__init__()
        self.collection = collection
    
    @classmethod
    async def init_collection(cls,
        database_client:AsyncIOMotorDatabase):
        collections = await database_client.list_collection_names()
        indices=ProjectSchema.get_index()
        collection = database_client['project']
        if "project" not in collections:
            for index in indices:
                await collection.create_index(
                    index['key'],
                    name =index['name'],
                    unique=index['unique']
                                                              )
        
        return cls(collection)                 
                
    
    async def insert_one(self,project:ProjectSchema):
        result = await self.collection.insert_one( 
           project.model_dump( exclude_none=True,
                                  by_alias = True)
           )
        return str(result.inserted_id)
       
    async def search_project_file_hash(
            self, 
            project_id:str,
            file_hash:str):
        result = await self.collection.find_one(
            {"file_hash":file_hash,
             "project_id":project_id})
        return result
    
    async def search_by_project(self, 
            project_id:str , page:int=1 , page_size = 10):
        document_count = await self.collection.count_documents({"project_id":
                                                                project_id})

        total_pages = document_count//page_size
        if document_count % page_size > 0:
            total_pages+=1
        cursor = self.collection.find({"project_id":project_id}).skip((page-1)*
                                            page_size).limit(page_size)
        documents = []
        async for document in cursor:
            documents.append(ProjectSchema(**document))    
        return documents ,total_pages 
    

    async def insert_project_file_hash(self,
                                    project_id:str,
                                    file_hash:str,
                                    file_id:str):
        project = await self.search_project_file_hash(
            project_id=project_id , 
            file_hash=file_hash)
        if project :
            project = ProjectSchema(**project)
            return project , True
        else:
            project = ProjectSchema(project_id=project_id,
                       file_id=file_id,
                       file_hash=file_hash)
            
            _ = await self.insert_one(project=project)
            return project, False
    
