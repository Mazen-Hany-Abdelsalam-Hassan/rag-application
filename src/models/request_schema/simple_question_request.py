from pydantic import BaseModel
from typing import List

class SimpleQuestionRequest(BaseModel):
    question:str
    process_ids:List[str]
    topk:int=5
    temperature:float=.2
    