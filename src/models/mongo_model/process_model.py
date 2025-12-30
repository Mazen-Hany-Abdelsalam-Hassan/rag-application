from motor.motor_asyncio import (AsyncIOMotorDatabase,
                                 AsyncIOMotorCollection)
from ..mongo_db_schema import ProcessSchema
from .base_model import BaseDataModel
from pymongo import ReturnDocument

class ProcessModel(BaseDataModel):
    def __init__(self, collection:AsyncIOMotorCollection):
        super().__init__()
        self.collection = collection
    
    @classmethod
    async def init_collection(cls,
        database_client:AsyncIOMotorDatabase):
        collections = await database_client.list_collection_names()
        indices=ProcessSchema.get_index()
        collection = database_client['process']
        if "process" not in collections:
            for index in indices:
                await collection.create_index(
                    index['key'],
                    name =index['name'],
                    unique=index['unique']
                          )
        return cls(collection)                 
    
    ## Insertion 
    async def insert_process_if_not_exist(
            self, 
            process:ProcessSchema):
        id = process.id
        update_result = await self.collection.update_one(
            {"_id": id},
            {
                "$setOnInsert": process.model_dump(
                    exclude_none=True,
                    by_alias=True
                )
            },
                upsert=True
            )
        exist = update_result.upserted_id is None
        return exist

    
    ## Retrieve
    async def find_by_project(self,
                    project_id:str,
                    processed:int=0,
                    indexed:int=0,
                    page:int=1,
                    page_size:int=20):
        
        query = {"project_id":project_id}
        
        if processed:
            query= {"project_id":project_id,"processed":1}
        
        elif indexed :
            query = {"project_id":project_id,
                     "processed":1,
                     "indexed":1}
        
        document_count = await self.collection.count_documents(query)
        
        total_pages = document_count//page_size
        if document_count % page_size > 0:
            total_pages+=1


        cursor =  self.collection.find(query).skip((page-1)*
                            page_size).limit(page_size)
        
        documents = []
        async for document in cursor:
            documents.append(ProcessSchema(**document))     
        return documents ,total_pages
    
    async def find_by_project_file_id(
                    self,
                    file_id:str,
                    project_id:str,
                    processed:int=0,
                    indexed:int=0,
                    page:int=1,
                    page_size:int=20):
    
        query = {"project_id":project_id,
                 "file_id":file_id}
        
        if processed:
            query= {"project_id":project_id,
                    "file_id":file_id,
                    "processed":1}
        
        elif indexed :
            query = {"project_id":project_id,
                     "file_id":file_id,
                     "processed":1,
                     "indexed":1}
        
        document_count = await self.collection.count_documents(query)
        
        total_pages = document_count//page_size
        if document_count % page_size > 0:
            total_pages+=1


        cursor = self.collection.find(query).skip((page-1)*
                            page_size).limit(page_size)
        
        documents = []
        async for document in cursor:
            documents.append(ProcessSchema(**document))     
        return documents ,total_pages
    
    async def latest_only(self):
        pass


    async def update(self,
                    id:str,
                    processed:int = 0, 
                    indexed:int = 0):
        result = await self.collection.find_one_and_update(
             {'_id':id},
            
            {'$set': {"processed":processed,
                      "indexed":indexed}},
            return_document=ReturnDocument.AFTER
                      )
        return result