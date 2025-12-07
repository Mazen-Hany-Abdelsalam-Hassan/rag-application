from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from ..vector_db_interface import VectorDbInterface
from ..vector_db_enum import QdrantDistanceEnum
from typing import Literal
import uuid
import logging
from qdrant_client.models import PointStruct


class QdrantVectorDatabase(VectorDbInterface):
    def __init__(self,database_path:str,similarity_metric:Literal['cosine','euclid'],topk:int,vector_size:int ):
        self.client = None
        self.topk = topk
        self.vector_size = vector_size
        self.logger = logging.getLogger(__name__)
        self.database_path = database_path
        if similarity_metric =='cosine':
            self.similarity_metric = Distance.COSINE
        elif similarity_metric =='euclid':
            self.similarity_metric = Distance.EUCLID
        else:
            self.logger.error(f"the similarity metric in qdrant must be cosine or euclid")
    
    
    def connect(self):
        self.client = QdrantClient(path=self.database_path,
                                   prefer_grpc=False  )
        self.logger.info("Qdrant DB connected")
    def disconnect(self):
        self.client = None
        self.logger.info("Qdrant DB disconnected")
    
    def is_collection_exist(self, collection_name:str)->bool:
        if not self.client :
            self.logger.error("Qqdrant DB disconected ")
            return False
        response = self.client.collection_exists(collection_name=collection_name)
        return response
    
    def delete_collection(self, collection_name):
        if not self.client:
            self.logger.error("Qqdrant DB disconected ")
            return False
        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.warning(f"This collection {collection_name} not exist")
            return False
        _ = self.client.delete_collection(collection_name=collection_name)
        self.logger.info(f"The collection {collection_name} deleted ")
        return True
    
    def create_collection(self, collection_name, remove_if_exist):
        if not self.client :
            self.logger.error("Qqdrant DB disconected ")
            return False
        if remove_if_exist and self.is_collection_exist(collection_name=collection_name):
            _ = self.delete_collection(collection_name=collection_name)
            self.client.create_collection(
                collection_name= collection_name ,
                vectors_config=VectorParams(size=self.vector_size,
                                            distance=self.similarity_metric),
            )
            self.logger.warning(f"collection {collection_name} has been reseted")
            return True 
        elif not(self.is_collection_exist(collection_name=collection_name)):
            self.client.create_collection(
                collection_name= collection_name ,
                vectors_config=VectorParams(size=self.vector_size,
                distance=self.similarity_metric),
            )
            self.logger.info(f"collection {collection_name} has been creted")
            return True 
        self.logger.info(f"collection {collection_name} already exist")
        return False
    
    def get_all_collection(self):
        if not self.client :
            self.logger.error("Qqdrant DB disconected ")
            return False
        return self.client.get_collections().collections


    def insert_vector(self,vector, collection_name, chunk, meta_data,id=None):
        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.error(f"The collection {collection_name} not exist")
            return False
        if not(isinstance(chunk,str)) :
            self.logger.error("chunk  must be string")
            return False
        if not self.client:
            self.logger.error("Qqdrant DB disconected ")
            return False
        if len(vector) != self.vector_size:
            self.logger.error(f"The vector length must be {self.vector_size}")
        _ = self.client.upsert(
        collection_name=collection_name,
        points=[
        PointStruct(
            id=id if id else uuid.uuid1(),
            payload={
                "chunk": chunk,
                "meta_data":meta_data},
                vector=vector)]
                
                )
        self.logger.info("the chunk uploaded succesfully")
        return True
    
    def batch_insert_vector(self, vectors, collection_name, chunks, meta_data_list, batch_size: int, ids=None):
        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.error(f"The collection {collection_name} not exist")
            return False
        try:
            if ids == None:
                ids = [uuid.uuid1() for i in range(len(chunks))]
            if len(vectors[0]) != self.vector_size or len(vectors) != len(chunks) or len(chunks) != len(meta_data_list):
                self.logger.error(f"The input is not valid the vector dimension must be {self.vector_size}")
                self.logger.error(f"The number of chunks, vectors and meta data must be same")
                return False
        except:
            self.logger.error('The vector must be list of list')
            return False
        
        for index in range(0, len(vectors), batch_size):
            vectors_batch = vectors[index:index+batch_size]
            chunks_batch = chunks[index:index+batch_size]
            meta_data_batch = meta_data_list[index:index+batch_size]
            ids_batch = ids[index:index+batch_size]
            
            points = [
                PointStruct(id=id, vector=vector, payload={"text": chunk,
                                                            "meta_data": meta_data})
                for id, vector, chunk, meta_data in zip(ids_batch, vectors_batch, chunks_batch, meta_data_batch)
            ]
            self.client.upsert(
                wait=True,
                collection_name=collection_name,
                points=points
            )
        self.logger.info(f"{len(chunks)} uploaded")
        return True


    def vector_search(self, vector, topk):
        return super().vector_search(vector, topk)
    
        