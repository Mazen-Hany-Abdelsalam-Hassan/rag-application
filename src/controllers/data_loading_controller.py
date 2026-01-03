from .base_controller import BaseController
from  fastapi import UploadFile
from models import ResponseEnum
import logging
import os

class DataLoadingController(BaseController):
    def __init__(self , Project:str):
        super().__init__()
        self.project = Project
        self.logger = logging.getLogger(__name__)
    
    def _is_valid_type(self,file:UploadFile):
        if file.content_type in self.environment_variable.ALLOWED_FILE_TYPES:      
            return True 
        else:
            self.logger.error(ResponseEnum.FILE_TYPE_NOT_SUPPORTED.value)
            return False 
    def _is_valid_size(self , file:UploadFile):
        if file.size  <= self.max_size:   
            return True
        else:
            self.logger.error(ResponseEnum.FILE_SIZE_EXCEEDED.value)
            return False  
    
    
    def is_valid_file(self,file:UploadFile):
        if self._is_valid_type(file) and self._is_valid_size(file):
            file_name =DataLoadingController.clean_file_name(file.filename)
            file_name, extension = file_name.split('.')
            file_name = file_name+"_"+DataLoadingController.random_string()
            self.project_directory = os.path.join(self.save_path,self.project)
            os.makedirs(self.project_directory , exist_ok=True)
            return file_name +'.'+extension
        else :
            return  False