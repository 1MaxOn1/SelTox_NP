import pandas as pd
import numpy as np
import V4_models
import random
from Models.V4_transform_ZOI import transform

population_size = 100
df_ZOI = pd.read_csv(r'D:\SelTox_NP\ZOI\data\preprocessed_ZOI_dataset.csv')
X = df_ZOI.drop(columns=['NP', 'Unnamed: 0'])
uniq_bacteria_data = X.copy(deep=True)
uniq_bacteria_data = X.drop_duplicates('Bacteria')

"""uniq value dataset"""
uniq = list() # stores all the unique characters available in the dataset, it helps to make a new population with random parameters
for column in X.columns:
    uni = pd.unique(X[column])
    uniq.append(uni)
    
"""create individual with values that are picked from the uniq array above"""
def individuals():
    indv = list()
    for feat_index in range(len(uniq)):
        uniqs = random.choice(uniq[feat_index])
        if uniqs is not np.nan:
            indv.append(uniqs)
    return indv
  
"""generate population with specific population size"""
def population(size):
    pops = list()
    for indv in range(2*size):
        single = individuals()
        pops.append(single)
    new_one = pd.DataFrame(data=pops, columns=X.columns)
    new = new_one.head(size)
    new = new.reset_index(drop=True)
    return new
    
df_population = population(population_size)


def bacteria_type(population_df):
    single_bacteria_pathogen = uniq_bacteria_data.loc[uniq_bacteria_data['Bacteria'] == 'Escherichia coli']
    single_bacteria_nonpathogen = uniq_bacteria_data.loc[uniq_bacteria_data['Bacteria'] == 'Bacillus subtilis']
    pop_non_pathogen = pd.concat([single_bacteria_nonpathogen] * len(population_df), ignore_index=True)
    pop_pathogen = pd.concat([single_bacteria_pathogen] * len(population_df), ignore_index=True)
    df_pathogen = population_df.copy()
    df_non_pathogen = population_df.copy()
    df_non_pathogen[['Bacteria', 'bac_type', 'Phylum', 'Class', 'Order', 'Family', 'gram', 'min_Incub_period, h', 'growth_temp, C','isolated_from']] = pop_non_pathogen[['Bacteria', 'bac_type', 'Phylum', 'Class', 'Order', 'Family', 'gram', 'min_Incub_period, h', 'growth_temp, C','isolated_from']]
    df_pathogen[['Bacteria', 'bac_type', 'Phylum', 'Class', 'Order', 'Family', 'gram', 'min_Incub_period, h', 'growth_temp, C','isolated_from']] = pop_pathogen[['Bacteria', 'bac_type', 'Phylum', 'Class', 'Order', 'Family', 'gram', 'min_Incub_period, h', 'growth_temp, C','isolated_from']]
    return df_non_pathogen, df_pathogen

df_eee = bacteria_type(df_population)

df_e = transform(df_eee[0])
df_e.to_csv('df_bac_type_non_p.csv')
df_e = transform(df_eee[1])
df_e.to_csv('df_bac_type_p.csv')

def fitness(df):
    n_path, path_gen = bacteria_type(df)
    np = transform(n_path)
    p = transform(path_gen)
    normal_b = V4_models.xgb_predict(np)
    pathogen_b = V4_models.xgb_predict(p)
    fitness = list()
    norm_v = list()
    path_v = list()
    for i in range(len(normal_b)):
        n = normal_b[i]
        c = pathogen_b[i]
        fit = c - n
        fittn = fit.tolist()
        norm_v.append(n)
        path_v.append(c)
        fitness.append(fittn)
    copy = n_path.assign(pred_ZOI_norm = norm_v)
    copy1 = copy.assign(pathogenic_bacteria = path_gen['Bacteria'].tolist())
    copy2 = copy1.assign(pred_ZOI_pathogen = path_v)
    copy3 = copy2.assign(Fitness = fitness)
    copy3 = copy3.sort_values('Fitness', ascending = False)
    return copy3






