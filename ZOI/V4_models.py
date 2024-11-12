import pandas as pd
import pickle
from xgboost import plot_importance
import matplotlib.pyplot as plt

path_xgb = r'D:\SelTox_NP\ZOI\Models\XGB_model\xgb_res.pkl'
path_ens = r'ZOI\Models\Ensemble model\ensemble_model.pkl'

def load_model(path):
    try:
        return pickle.load(open(path, 'rb'))
    except Exception as e:
        print('Something went wrong')
        return e
    
model = load_model(path_xgb)

def xgb_predict(input_data):
    return model.predict(input_data)


def get_feature_importance(model, vis = False):
    if vis:
       plot_importance(model, importance_type='weight') 
       plt.show()
    else:   
        b = model.get_booster()
        feat_imp = b.get_score(importance_type='weight')
        print(feat_imp)
    


# get_feature_importance(model, True)