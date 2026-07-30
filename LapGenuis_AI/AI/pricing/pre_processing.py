from AI.common.hardware_parser import extract_hardware_features
import pandas as pd

def one_hot_encode(df):
    df = df.copy()
    df = pd.get_dummies(df)
    return df

def align_columns(df, training_columns):
    df = df.copy()
    return df.reindex(columns=training_columns, fill_value=0)




def prepare_data_for_ml(df, training_columns):
    df = df.copy()
    df = df.drop(columns=["id"], errors="ignore")
    df = extract_hardware_features(df)
    df = one_hot_encode(df)
    df = align_columns(df, training_columns)
    return df
                                    
