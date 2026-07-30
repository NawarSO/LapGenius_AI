from fastapi import FastAPI
from AI.api.schemas import(
    LaptopRequest,
    RecommendationRequest
)
from AI.api.services import (
    recommend,
    predict
    )



app = FastAPI()

@app.get('/health')
def health():
    return {"status": "ok"}

@app.get('/')
def message():
    return {'message': 'Welcom to lapGenuis!'}


@app.post("/predict")
def predict_price(data: LaptopRequest):
    return predict(data)


@app.post("/recommend")
def recommend_laptops(request: RecommendationRequest):
    return recommend(request)