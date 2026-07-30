import joblib 
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

def load_model():
    model = joblib.load(BASE_DIR /'laptop_price_model.pkl')
    training_columns = joblib.load(BASE_DIR / 'training_columns.pkl')
    return model, training_columns