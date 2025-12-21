from motor.motor_asyncio import AsyncIOMotorDatabase
from models import UserSchema ,FileStatus
from .base_model import BaseDataModel
class UserModel(BaseDataModel):
    def __init__(self, database_client:AsyncIOMotorDatabase):
        super().__init__()
        self.collection = database_client['user']
    
    async def insert_one(self,user_schema:UserSchema):
        result = await self.collection.insert_one( 
           user_schema.model_dump(exclude_unset=True,
                                  by_alias = True)
           )
        return str(result.inserted_id)
       
    async def search_user_text_hash(
            self, 
            username:str,
            text_encoding:str):
        result = await self.collection.find_one(
            {"text_encoding":text_encoding,
             "username":username})
        return result
    
    async def search_by_user(self, 
            username:str , page:int=1 , page_size = 10):
        document_count = await self.collection.count_documents({"username":
                                                                username})
        total_pages = document_count//page_size
        if total_pages % page_size > 0:
            total_pages+=1
        cursor = self.collection.find({"username":username}).skip((page-1)*
                                                                         page_size).limit(page_size)
        documents = []
        async for document in cursor:
            documents.append(UserSchema(**document))    
        return documents ,total_pages
    

    async def insert_user_text_hash(self,
                                    username:str,
                                    text_encoding:str,
                                    file_id:str,
                                    parsing_method:str="Naive"):
        user = await self.search_user_text_hash(
            username=username , 
            text_encoding=text_encoding)
        if user :
            user = UserSchema(**user)
            return user , True
        else:
            user = UserSchema(username=username,
                       file_id=file_id,
                       text_encoding=text_encoding,
                       status=FileStatus.UPLOADED.value,
                       parsing_method=parsing_method)
            
            _ = await self.insert_one(user_schema=user)
            return user, False
    
    async def search_user_file_id(
            self, 
            username:str,
            file_id:str):
        result = await self.collection.find_one(
            {"file_id":file_id,
             "username":username})
        return result
    
    async def add_chunk_size_and_overlap(self , username:str, file_id:str , 
                                        chunk_size:int , 
                                        chunk_overlap:int):
        exist = await self.search_user_file_id(username=username,
                                               file_id=file_id)
        
        if exist:
            updated = await self.collection.update_one(
                {"file_id":file_id , 
                 "username":username}, 
                 {"$set":{"chunk_size":chunk_size , 
                          "chunk_overlap":chunk_overlap}})
            return updated.raw_result
        
        return False
             
        
        


        