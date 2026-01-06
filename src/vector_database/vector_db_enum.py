from enum import Enum
from qdrant_client.models import Distance
from typing import Literal


class QdrantDistanceEnum(Enum):
    cosine= Distance.COSINE
    euclid = Distance.EUCLID
    
class VectorDatabaseProvider(Enum):
    Qdrant= "Qdrant"
