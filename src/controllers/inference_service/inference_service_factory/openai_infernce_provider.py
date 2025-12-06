from ..inference_service_factory_interface import InferenceServiceFactoryInterface
from openai import OpenAI
from typing import List , Dict
from ..llm_enum import OpenaiEnumRole
import logging
class OpenaiInferenceProvider(InferenceServiceFactoryInterface):
    def __init__(self,
                base_url:str= None , 
                api_key:str=None ,
                max_input_token:int=1000,
                max_output_token:int = 1000,
                tempreature:int = .1):
        self.max_input_token = max_input_token
        self.max_output_token = max_output_token
        self.tempreature = tempreature
        
        self.llm_model_id = None
        self.embedding_model_id= None
        self.embedding_dim = None
        
        self.client = OpenAI(
            base_url=base_url , 
            api_key=api_key )

        self.logger = logging.getLogger(__name__)
    def set_generation_model(self, llm_model_id:str):
        self.llm_model_id = llm_model_id
        self.logger.info(f"the used llm is {self.llm_model_id}")
    
    def set_embedding_model(self, embedding_model_id, embedding_dim):
        self.embedding_model_id = embedding_model_id 
        self.embedding_dim =embedding_dim
        self.logger.info(f"the used embedding is {self.embedding_model_id}_{self.embedding_dim}")
    
    def generate_text(self, 
                    prompt:str,
                    history:List[Dict[str,str]],
                    max_output_token = None,
                    tempreature = None):
        
        if not self.client :
            self.logger.error(f"The client is not available")
            return None
        if not self.llm_model_id:
            self.logger.error("The generation mode is not assigned")
        
        max_output_token = max_output_token if max_output_token else self.max_output_token
        tempreature = tempreature if tempreature else self.tempreature
        self.logger.info(f"max_output_token is {max_output_token},tempreature is {tempreature}")
        prompt = self.process_input_token(prompt=prompt)
        history.append(
            self.construct_prompt(prompt=prompt)
        )
        llm_response = self.client.chat.completions.create(
            model=self.llm_model_id , 
            messages=history,
            max_tokens=max_output_token ,
            temperature=tempreature
        )
        if not(llm_response) or  len(llm_response.choices)==0 or not(llm_response.choices[0]) or not(llm_response.choices[0].message.content):
            self.logger.error("No response from model")
            return None
        
        self.logger.info(f"Generation Used {llm_response.usage.total_tokens} token")
        self.logger.info(f"Generation model name {llm_response.model}")
        return llm_response.choices[0].message.content
    
    def embed_text(self, text):  
        if not self.client :
            self.logger.error(f"the client is not available")
            return None
        if not self.embedding_model_id:
            self.logger.error(f"Embedding model is not set") 
        
        response = self.client.embeddings.create(input = text ,
                                         model=self.embedding_model_id)
        
        if not(response) or not(response.data) or not(response.data[0]) or not (response.data[0].embedding):
            self.logger.error("No response from embedding model please check your api")
            return None
        self.logger.info(f"Embedding used {response.usage.total_tokens} token")

        return response.data[0].embedding

    def construct_prompt(self, prompt):
        return {"role":OpenaiEnumRole.user.value , 
                "content":prompt}
    def process_input_token(self,prompt):
        return prompt[:self.max_input_token]
    

        
