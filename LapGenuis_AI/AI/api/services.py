from AI.pricing.predictor import PricePredictor
from AI.recommendation_system.recommendation_engine import LaptopRecommender
from AI.data_provider.repositery import get_all_laptops
import pandas as pd
import time

price_predictor = PricePredictor()
laptop_recommender = LaptopRecommender()

def predict(data):
    df = pd.DataFrame([data.model_dump()])
    prediction = price_predictor.predict(df)

    return {
        "predicted_price": float(prediction[0])
    }

def recommend(request):
    budget = request.budget
    use_case = request.use_case
    
    t = time.time()
    df = get_all_laptops() 
    print(f"Time taken to fetch laptops (services.py in api folder): {time.time() - t} seconds")

    print('++++++DEBUGGING+++++ \n file: services.py in api Folder')
    print(df.dtypes)
    print(df["price"].head())
    print(type(df["price"].iloc[0]))

    return laptop_recommender.recommend(df, budget, use_case)
