from .base_controller import BaseController
from langchain_community.document_loaders import (PyMuPDFLoader,
                                                  TextLoader)
import os
import logging
from typing import List
from langchain_classic.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


from models import AllowedFileExtension
class DataProcessingController(BaseController):
    def __init__(self ,user:str):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.user_path= os.path.join(self.save_path,user)
    def load_file(self,file_id:str): 
        file_path = os.path.join(self.user_path , file_id)
        if not os.path.exists(file_path):
            self.logger.error("File Not Exist")
            return None
        extension = os.path.splitext(file_path)[-1]
        if extension == AllowedFileExtension.PDF.value:
            loader = PyMuPDFLoader(file_path=file_path)
            return loader.load()
        elif extension ==AllowedFileExtension.TXT.value:
            loader = TextLoader(file_path=file_path)
            return loader.load()
        else:
            self.logger.error("File type not processed")
            return None 
        
    def chunk_file(self,
                loaded_pdf:List[Document] ,
                chunk_size:int,
                chunk_overlap:int):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(loaded_pdf)
        chunks_text = [
            chunk.page_content
            for chunk in chunks
        ]
        chunks_meta_data = [
            chunk.metadata
            for chunk in chunks
        ]
        return chunks_text , chunks_meta_data 


        
        
    