import pandas as pd
import pickle
import warnings


warnings.filterwarnings('ignore')

Cat_model_path = r'D:\SelTox_NP\MIC\Models\cat_boost\cat_boost_reg.pkl'

def model_load(path):
    with open(path, 'rb') as f:
        cat_model = pickle.load(f)
        return cat_model
mod = model_load(Cat_model_path)

def cat_predict(input_data):
    x = input_data
    predict = mod.predict(x)
    return predict