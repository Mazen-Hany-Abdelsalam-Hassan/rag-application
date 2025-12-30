from pydantic import BaseModel, Field, model_validator

class SimpleProcessingSchemaRequest(BaseModel):
    chunk_size: int = Field(..., ge=100)
    chunk_overlap: int = Field(..., ge=0)
    
    @model_validator(mode='after')
    def validate_overlap(self):
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                f"chunk_overlap ({self.chunk_overlap}) must be less than "
                f"chunk_size ({self.chunk_size})"
            )
        return self