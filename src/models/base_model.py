from utils import Settings , get_settings

class BaseDataModel:
    def __init__(self):
        self.environment_variable = get_settings()