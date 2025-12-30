from abc import ABC, abstractmethod

class DataProcessingInterface(ABC):

    @abstractmethod
    def load_file(self, file_path:str,
        is_processed:bool,
        processed_path:str):
        pass

    @abstractmethod
    def chunk_file(self,
                   **processing_parameter):
        pass
    
    @abstractmethod
    def create_fingerprint(self):
        pass
    
    @abstractmethod
    def validate_processing_parameter(self):
        pass
    @abstractmethod
    def validate_file_existence(self):
        pass