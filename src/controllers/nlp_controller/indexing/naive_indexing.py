from ...base_controller import BaseController
from models import  ChunkSchema
from typing import List
import asyncio
from inference_service import InferenceServiceFactoryInterface
from vector_database import VectorDbInterface
import os 
class NaiveIndexing(BaseController):
    def __init__(
            self,
            process_id,
            project_name,
            vector_database:VectorDbInterface):
        super().__init__()
        self.process_id = process_id
        self.vector_database = vector_database
        self.project_name = project_name
    async def embed(self,
              chunks_list:List[ChunkSchema],
              embedding_client:InferenceServiceFactoryInterface,
              use_index=True):
        
        
        embedding_vectors = []
        
        for chunk in chunks_list:
            emb = embedding_client.embed_text(chunk.chunk_text)
            embedding_vectors.append(emb)
            await asyncio.sleep(.1)
        

        
        text_chunks = [
            chunk.chunk_text
            for chunk in chunks_list 
        ]

        meta_data = [
            {
                "meta_data":chunk.chunk_meta_data,
                "chunk_order":chunk.chunk_order 
            }
            for chunk in chunks_list
        ]
        
        
        if len(embedding_vectors)==0 :
            return False

        self.vector_database.create_collection(
                                        self.project_name,
                                        )
        
        result = self.vector_database.batch_insert_vector(

            vectors = embedding_vectors,
            collection_name=self.project_name,
            chunks=text_chunks,
            meta_data_list=meta_data,
            batch_size=50 ,
            payload_index={"process_id":self.process_id} if use_index  else {}
            )   
        return result




