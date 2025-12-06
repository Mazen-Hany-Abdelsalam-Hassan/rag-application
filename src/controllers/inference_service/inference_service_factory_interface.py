from abc import ABC , abstractmethod
from typing import List , Dict
class InferenceServiceFactoryInterface(ABC):
    @abstractmethod
    def set_generation_model(self, llm_model_id:str):
        pass
    @abstractmethod
    def set_embedding_model(self, embedding_model_id:str , embedding_dim:int):
        pass
    @abstractmethod
    def generate_text(self,
                    prompt:str, 
                    history:List[Dict[str , str]],
                    max_output_token:int, 
                    tempreature:float)-> str:
            pass
    @abstractmethod
    def embed_text(self,
              text:str )->List[float]:
        pass

    @abstractmethod
    def construct_prompt(self , prompt:str)-> Dict[str, str]:
         pass 