from .base_controller import BaseController
from  fastapi import UploadFile
from models import ResponseEnum
import logging
import os

class DataLoadingController(BaseController):
    def __init__(self , User:str):
        super().__init__()
        self.user = User
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
            self.logger.error(ResponseEnum.FILE_SIZE_EXCEDED.value)
            return False  
    
    
    def is_valid_file(self,file:UploadFile):
        if self._is_valid_type(file) and self._is_valid_size(file):
            file_name =DataLoadingController.clean_file_name(file.filename)
            file_name, extension = file_name.split('.')
            file_name = file_name+"_"+DataLoadingController.random_string()
            self.user_directory = os.path.join(self.save_path,self.user)
            os.makedirs(self.user_directory , exist_ok=True)
            return (ResponseEnum.FILE_UPLOADED_SUCCESSFULLY.value,
                    file_name +'.'+extension)
        else :

            return (ResponseEnum.FILE_NOT_UPLOADED_SUCCESSFULLY.value,
                    False)