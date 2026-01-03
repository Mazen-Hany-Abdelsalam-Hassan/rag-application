from ..base_controller import BaseController
from .data_processing_interface import DataProcessingInterface
from langchain_community.document_loaders import (PyMuPDFLoader,
                                                  TextLoader)
from models import (SimpleProcessingSchemaRequest,
                    AllowedFileExtension,ChunkSchema)

import os
import logging
from typing import List
from langchain_classic.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import ValidationError


class SimpleProcessing(BaseController,
                          DataProcessingInterface):
    def __init__(self ,
                 project:str,
                 file_id:str,
                 processing_parameter:dict):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.project = project
        self.file_id=file_id 
        self.project_path= os.path.join(self.save_path,self.project)
        self.file_path = os.path.join(self.project_path , self.file_id)
        self.processing_parameter = processing_parameter
        self.file_exist = self.validate_file_existence() 
        self.valid_processing = self.validate_processing_parameter()
        self.FingerPrint = self.create_fingerprint()

                
    
    def validate_file_existence(self):
        if not os.path.exists(self.file_path):
            self.logger.error("File Not Exist")
            return False
        return True
        
    
    def validate_processing_parameter(self):
        try:
            self.processing_parameter = SimpleProcessingSchemaRequest(**self.processing_parameter)
            return True
        except ValidationError as e:
            self.logger.error(e)
            return False
    
    def load_file(self): 
        extension = os.path.splitext(self.file_path)[-1]
        if extension == AllowedFileExtension.PDF.value:
            loader = PyMuPDFLoader(file_path=self.file_path)
            return loader.load()
        elif extension ==AllowedFileExtension.TXT.value:
            loader = TextLoader(file_path=self.file_path)
            return loader.load()
        else:
            self.logger.error("File type not processed")
            return None 
        
    def chunk_file(self,
        loaded_pdf:List[Document]):
        
        chunk_size = self.processing_parameter.chunk_size
        chunk_overlap = self.processing_parameter.chunk_overlap
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(loaded_pdf)
        

        chunks_in_schema = [
                
        ChunkSchema(process_id=self.FingerPrint,
            chunk_text=chunk.page_content,
            chunk_meta_data= chunk.metadata,
            chunk_order=i,)

            for i,chunk in enumerate(chunks)
        ]

        return chunks_in_schema
    
    
    def create_fingerprint(self):
        chunk_size = self.processing_parameter.chunk_size
        chunk_overlap = self.processing_parameter.chunk_overlap
        process_id = self.project+"_"+self.file_id+"_"+"Simple" \
             +"_"+str(chunk_size)+"_"+str(chunk_overlap)
        return process_id.replace('.','_')         
    