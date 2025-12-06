from fastapi import FastAPI
from routes.base_route import base_route
from utils import Settings ,get_settings
from controllers import Factory
import logging
from openai import OpenAI
logging.basicConfig(
    level=logging.INFO,
    filename='log.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
config = get_settings()

factory = Factory(config)

llm = factory.create(config.LLM_BACKEND)
llm.set_generation_model(llm_model_id=config.LLM_MODEL)


embedding = factory.create(config.EMBEDDING_MODEL_BACKEND)
embedding.set_embedding_model(embedding_model_id=config.EMBEDDING_MODEL_NAME
                        ,embedding_dim=config.EMBEDDING_MODEL_DIM)


print(embedding.embed_text("What is the Machine Learning in 50 word???"))
print(llm.generate_text("What is the Machine Learning in 50 word???" , history=[]))

