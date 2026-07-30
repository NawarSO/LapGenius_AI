from pydantic import BaseModel

class LaptopRequest(BaseModel):
    brand: str
    cpu: str
    ram: str
    hard: str
    gpu: str
    new: bool

class RecommendationRequest(BaseModel):
    use_case: str
    budget: float