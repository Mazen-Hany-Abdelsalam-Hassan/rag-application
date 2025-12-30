from enum import Enum

class ResponseEnum(Enum):
    FILE_SIZE_EXCEEDED="The file size Exceeded"
    FILE_TYPE_NOT_SUPPORTED= "File type not supported"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_NOT_UPLOADED_SUCCESSFULLY = "File not uploaded successfully"
    FILE_PROCESSING_SUCCESS= "File processed successfully" 
    FILE_PROCESSING_FAIL = "File not processed successfully"
    
    WRONG_PROCESSING_PARAMETER = "File processing parameter is not right"
    WRONG_PROCESSING_METHOD = "File processing method is not True"
