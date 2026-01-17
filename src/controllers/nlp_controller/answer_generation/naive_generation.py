from ...base_controller import BaseController
from models import  ChunkSchema
from typing import List
from inference_service import InferenceServiceFactoryInterface
from vector_database import VectorDbInterface
import os 
from prompts import footer_prompt , system_prompt , document_prompt 
from logging import Logger

class NaiveGeneration(BaseController):
    def __init__(self,
            embedding_model:InferenceServiceFactoryInterface,
            llm_model:InferenceServiceFactoryInterface,
            project_id:str , 
            process_ids:List[str],
            vector_database_client:VectorDbInterface):
        super().__init__()
        self.logger =Logger(__name__)
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        if self.llm_model.llm_model_id is None:
            self.logger.error("LLM Model is not initialized")
        elif self.embedding_model.embedding_model_id is None:
            self.logger.error("embedding model is not initialized")
        self.process_ids = process_ids
        self.extract_process_id()
        self.project_id= project_id 
        self.vector_database_client = vector_database_client


    def search(self, question:str , topk=5):
        search_filter = self.make_search_filter()
        embedding_vector = self.embedding_model.embed_text(question)
        search_result = self.vector_database_client.vector_search(
            vector=embedding_vector,
            collection_name=self.project_id,
            filter=search_filter,
            topk=topk
        )
        
        chunks = [text.text_chunk for text in search_result]
        
        formatted_docs = []

        for i, text in enumerate(chunks, start=1):
            formatted_docs.append(
                document_prompt.substitute(
                    doc_num=i,
                    chunk_text=text
                )
            )

        context = "\n\n".join(formatted_docs)  
        final_prompt = context + "\n\n" + footer_prompt.substitute(query=question)
        
        history = [{"role":"system"
            ,"content":system_prompt.safe_substitute()}]
        #print(history)
        print(final_prompt)
        try:
            return self.llm_model.generate_text(final_prompt , history=history)
        except Exception as e:
            print('bad')
        
    
    def extract_process_id(self):

        document_names =set()
        unique_process  = []
        
        for process_id in self.process_ids:
            document_name = process_id.split(self.separator)[1]
            if document_name not in document_names:
                document_names.add(document_name)
                unique_process.append(process_id)
    
        self.process_ids = unique_process

    def make_search_filter(self):
        return {
            "should": [
                {
                    "key": "process_id",
                    "match": {
                        "value": pid
                    }
                }
                for pid in self.process_ids
            ],
            
        }

