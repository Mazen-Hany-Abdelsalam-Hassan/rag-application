from .providers import QdrantVectorDatabase
from .vector_db_enum import (VectorDatabaseProvider,
                             QdrantDistanceEnum)
from utils import Settings
class VectorDatabaseFactory:
    def __init__(self,config:Settings):
        self.config = config 
    
    def set_provider(self , vector_database_name):
        if vector_database_name == VectorDatabaseProvider.Qdrant.value:
            return QdrantVectorDatabase(
                qdrant_path=self.config.QDRANT_DATABASE_PATH,
                qdrant_url=self.config.QDRANT_DATABASE_URL,
                similarity_metric=self.config.DISTANCE_METRICS,
                topk=self.config.TOPK,
                vector_size=self.config.EMBEDDING_MODEL_DIM)
        else:
            raise NotImplementedError(f'{vector_database_name} is not implemented')
            