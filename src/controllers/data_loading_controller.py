from .base_controller import BaseController
from  fastapi import UploadFile
from models import DataControllerEnum
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
            self.logger.error(DataControllerEnum.FILE_TYPE_NOT_SUPPORTED.value)
            return False 
    def _is_valid_size(self , file:UploadFile):
        if file.size  <= self.max_size:   
            return True
        else:
            self.logger.error(DataControllerEnum.FILE_SIZE_EXCEDED.value)
            return False  
    
    
    def is_valid_file(self,file:UploadFile):
        if self._is_valid_type(file) and self._is_valid_size(file):
            file_name =DataLoadingController.clean_file_name(file.filename)
            save_path = os.path.join(self.source_path,'assets' ,self.user )
            os.makedirs(save_path , exist_ok=True)
            save_path = os.path.join(save_path,file_name )
            return (DataControllerEnum.FILE_UPLOADED_SUCCESSFULLY.value
                    , save_path)
        else :

            return (DataControllerEnum.FILE_NOT_UPLOADED_SUCCESSFULLY.value,
                    False)