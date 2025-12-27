from enum import Enum
from typing import Literal
class OpenaiEnumRole(Enum):
    assistant='assistant'
    user = 'user'
    system='system'

class Backend(Enum):
    openai = "OPENAI" 