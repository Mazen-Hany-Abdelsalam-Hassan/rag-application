from .inference_service_factory import OpenaiInferenceProvider
from .llm_enum import Backend

from .inference_service_factory_interface import InferenceServiceFactoryInterface
from utils import Settings
class Factory:
    def __init__(self ,config:Settings):
        self.config=config
    def create(self , backend)->InferenceServiceFactoryInterface:
        if backend == Backend.openai.value:
            return OpenaiInferenceProvider(base_url=self.config.OPENAI_URL,
                                    api_key=self.config.OPENAI_KEY,
                                    max_input_token= self.config.MAX_INPUT_TOKEN,
                                    max_output_token=self.config.MAX_OUTPUT_TOKEN,
                                    temperature=self.config.TEMPERATURE)
        else:
            raise NotImplementedError(f'{backend} is not implemented')
            


        