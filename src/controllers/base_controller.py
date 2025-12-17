from utils import get_settings
import os
import re

class BaseController:
    def __init__(self):
        self.environment_variable = get_settings()
        self.source_path = os.path.dirname(os.path.dirname(__file__))
        self.max_size = 1_048_576 * self.environment_variable.MAXIMUM_ALLOWED_SIZE
    @staticmethod
    def clean_file_name(file_name:str):
        cleaned = re.sub(r'[\/:*?"<>|]', '', file_name)
        cleaned = re.sub(r'\s+', '_', cleaned)
        cleaned = cleaned.strip('_')
    
        return cleaned