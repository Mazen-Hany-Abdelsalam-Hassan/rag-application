from motor.motor_asyncio import (AsyncIOMotorDatabase,
                                 AsyncIOMotorCollection)
from ..mongo_db_schema import ChunkSchema
from .base_model import BaseDataModel
from typing import List

class ChunkModel(BaseDataModel):
    def __init__(self, collection:AsyncIOMotorCollection):
        super().__init__()
        self.collection = collection
    
    @classmethod
    async def init_collection(cls,
        database_client:AsyncIOMotorDatabase):
        collections = await database_client.list_collection_names()
        indices=ChunkSchema.get_index()
        collection = database_client["chunk"]
        if "chunk" not in collections:
            for index in indices:
                await collection.create_index(
                    index['key'],
                    name =index['name'],
                    unique=index['unique']
                          )
        return cls(collection) 

    async def find_by_process_id(self,
                    process_id:str,
                    page:int=1,
                    page_size:int=50):
        
        document_count = await self.collection.count_documents(
            {"process_id": process_id})
        total_pages = document_count//page_size
        if document_count % page_size > 0:
            total_pages+=1
        cursor = self.collection.find({"process_id":process_id}).skip((page-1)*
                                            page_size).limit(page_size)
        documents = []
        async for document in cursor:
            documents.append(ChunkSchema(**document))    
        return documents ,total_pages 

    async def insert_chunks(self,
                            chunks:List[ChunkSchema],
                            batch_size:int = 50):
        for start_index in range(0 , 
                                 len(chunks) , batch_size):
            
            to_inserted_chunks = chunks[start_index:
                                        start_index+batch_size]
            
            to_inserted_chunks = [chunk.model_dump(exclude_none=True,
                                by_alias=True) for chunk in  to_inserted_chunks]
            
            
            await self.collection.insert_many(to_inserted_chunks,ordered=False)
        return True 
    
    async def delete_by_process_id(self,process_id:str):
        delete_many = await  self.collection.delete_many(
            {"process_id":process_id}
        )
        return delete_many.deleted_count
    
