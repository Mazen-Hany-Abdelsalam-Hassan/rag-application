from abc import ABC , abstractmethod
from typing import List
class VectorDbInterface(ABC):
    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass
    @abstractmethod
    def get_all_collection(self):
        pass
    @abstractmethod
    def delete_collection(self , collection_name:str)->bool:
        pass
    @abstractmethod
    def is_collection_exist(self , collection_name:str)->bool:
        pass
    
    @abstractmethod
    def create_collection(self, collection_name:str,remove_if_exist:bool=False):
        pass

    @abstractmethod
    def insert_vector(self ,
                    vector:List[float],   
                    collection_name:str ,
                    chunk:str,
                    meta_data:str)->bool:
        pass


    @abstractmethod
    def batch_insert_vector(self, 
                vectors:List[List[float]],   
                collection_name:str ,
                chunks:List[str],
                meta_data_list:List[str],
                batch_size:int=50,
                payload_index:dict=None,
                ids=None)->bool:
        pass
    @abstractmethod
    def vector_search(
        self,
        vector:List[float] ,
        topk:int,
        data_filter:dict= None):
        pass


