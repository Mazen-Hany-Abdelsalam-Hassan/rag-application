from dataclasses import dataclass
from typing import Dict , List 
@dataclass
class VectorDBResponse:
    text_chunk:str
    score:float
    meta_data:Dict[str, str]
