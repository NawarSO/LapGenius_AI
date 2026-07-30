from AI.recommendation_system.recommendation_steps import (
    filter_by_budget,
    add_performance_score,
    filter_by_min_performance,
    add_value_score,
    rank_by_value,
    get_best
)
from AI.recommendation_system.feature_engineering import (
    prepare_recommendation_data,
    compute_performance_score,
    compute_value_score
)

from AI.recommendation_system.explainability import generate_explanation

from AI.recommendation_system.config import use_case_weights

import time

class LaptopRecommender:

    def __init__(self):
        self.engine = RecommendationEngine()

    def recommend(self, df, budget, use_case):
        t = time.time()
        df = prepare_recommendation_data(df)
        print(f"Time taken to prepare recommendation data (LaptopRecommender in recommendation_engine.py): {time.time() - t} seconds")

        return self.engine.recommend(df, budget, use_case)





class RecommendationEngine:

    def __init__(self):
        self.use_case_weights = use_case_weights
    
    def recommend(self, df, budget, use_case, top_k=5):
        config = self.use_case_weights[use_case]
        weights = config['weights']
        min_score = config['min_score']
        t = time.time()
        # Step 1: Budget filter
        df = filter_by_budget(df, budget)

        if df.empty:
            return {
                "best_performance": None,
                "best_value": None,
                "top_k": [],
                "meta": {
                    "status": "no_results",
                    "budget": budget,
                    "use_case": use_case
                }
            }

        # Step 2: Performance
        df = add_performance_score(df, weights, compute_performance_score)

        # Step 3: Min threshold
        df = filter_by_min_performance(df, min_score)

        if df.empty:
            return {
                "best_performance": None,
                "best_value": None,
                "top_k": [],
                "meta": {
                    "status": "no_results",
                    "budget": budget,
                    "use_case": use_case
                }
            }

        # Step 4: Value score
        df = add_value_score(df, compute_value_score)

        df = self._add_explanations(df, weights)

        # Step 5: Results
        best_performance = get_best(df, "performance")
        best_value = get_best(df, "value")
        top_k_df = rank_by_value(df, top_k)
        print(f"Time taken to recommend laptops (RecommendationEngine in recommendation_engine.py): {time.time() - t} seconds")
        return {
            "best_performance": best_performance.to_dict(orient="records")[0],
            "best_value": best_value.to_dict(orient="records")[0],
            "top_k": top_k_df.to_dict(orient="records"),
            "meta": {
                "budget": budget,
                "use_case": use_case,
                "candidates": len(df)
            }
        }
        
    def _add_explanations(self, df, weights):
        df = df.copy()

        df["reasons"] = df.apply(generate_explanation, axis=1)

        return df
    
