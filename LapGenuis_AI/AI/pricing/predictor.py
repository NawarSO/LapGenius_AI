from AI.pricing.pre_processing import prepare_data_for_ml
from AI.pricing.model_loader import load_model

class PricePredictor:

    def __init__(self):
        self.model, self.training_columns = load_model()

    def predict(self, df):
        df = df.copy()
        df = prepare_data_for_ml(df,self.training_columns)
        prediction = self.model.predict(df)

        return prediction



"""import pandas as pd
import numpy as np
def test():

    test_sample = pd.DataFrame([np.zeros(6)], columns=['brand', 'cpu', 'ram', 'hard', 'gpu', 'new'])

    test_sample['brand'] = 'Lenovo'
    test_sample['cpu'] = 'intel core i7 9750 h'
    test_sample['ram'] = '16'
    test_sample['hard'] = '256 ssd'
    test_sample['gpu'] = 'nvidia'
    test_sample['new'] = 'false'

    predict = PricePredictor()
    val = predict.predict(test_sample)
    return val

print(test())"""

    
