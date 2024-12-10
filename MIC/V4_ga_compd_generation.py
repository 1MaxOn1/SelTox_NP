import time

import pandas as pd
import V4_models
import random
from  Models import  V4_transform_MIC_trial

population_size = 100
df_MIC = pd.read_csv(r'D:\SelTox_NP\MIC\data\MIC_before_preprocessed.csv')
# df_MIC = df_MIC[df_MIC['np_synthesis'].isin(['green_synthesis','chemical_synthesis'])]
X = df_MIC.drop(['Unnamed: 0'], axis=1) 
uniq_bacteria_data = X.drop_duplicates('Bacteria')
uniq = [] 
for a in range(len(X.columns)):
  uni = pd.unique(X.iloc[:, a])
  uniq.append(uni)
  
uniq_bacs_path = X[(X['bac_type'] == 'opportunistic pathogen') | 
                   (X['bac_type'] == 'pathogenic')]['Bacteria'].unique()
uniq_bacs_non_path = X[(X['bac_type'] == 'non-pathogenic')]['Bacteria'].unique()


def individuals():
  indv = []
  for a in range(len(X.columns)):
    uniqas = random.choice(uniq[a])
    indv.append(uniqas)
  return indv

def population(size):
  pops = []
  for indv in range(2*size):
    single = individuals()
    pops.append(single)
  new_one = pd.DataFrame(data=pops, columns=X.columns)
  neww = new_one[(new_one['NP size_min (nm)'] > 5)]
  new = neww.head(size)
  new = new.reset_index(drop=True)
  material_descriptor = X.iloc[[random.randrange(0, len(X)) for _ in range(len(new))]]
#   material_descriptor = material_descriptor.reset_index(drop=True)
#   new[['np', 'mol_weight (g/mol)', 'Valance_electron','labuteASA', 'tpsa', 'CrippenMR', 'chi0v']] = material_descriptor[['np', 'mol_weight (g/mol)', 'Valance_electron', 'labuteASA', 'tpsa', 'CrippenMR', 'chi0v']]
  return new

def bacteria_type(population_df):
  single_bacteria_pathogen = uniq_bacteria_data.loc[uniq_bacteria_data['Bacteria'] == 'Escherichia coli']
  single_bacteria_nonpathogen = uniq_bacteria_data.loc[uniq_bacteria_data['Bacteria'] == 'Bacillus subtilis']
  pop_non_pathogen =pd.concat([single_bacteria_nonpathogen]*len(population_df), ignore_index=True)
  pop_pathogen = pd.concat([single_bacteria_pathogen] * len(population_df), ignore_index=True)
  df_pathogen= population_df.copy()
  df_non_pathogen = population_df.copy()
  # print(population_df)
  df_non_pathogen[['Bacteria', 'bac_type', 'Superkingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'gram', 'min_Incub_period, h', 'growth_temp, C ']] = pop_non_pathogen[['Bacteria', 'bac_type', 'Superkingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'gram', 'min_Incub_period, h', 'growth_temp, C ']]
  df_pathogen[['Bacteria', 'bac_type', 'Superkingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'gram', 'min_Incub_period, h', 'growth_temp, C ']] = pop_pathogen[['Bacteria', 'bac_type', 'Superkingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'gram', 'min_Incub_period, h', 'growth_temp, C ']]
  return df_non_pathogen, df_pathogen


def fitness(df):
  # start_time = time.time()
  n_path, path_gen = bacteria_type(df)
  np = V4_transform_MIC_trial.transform(n_path)
  p = V4_transform_MIC_trial.transform(path_gen)
  normal_b = V4_models.cat_predict(np)
  pathogen_b = V4_models.cat_predict(p)
  fitness = []
  norm_v = []
  path_v = []
  for a in range(len(normal_b)):
    n = normal_b[a]
    c = pathogen_b[a]
    fit = n - c 
    fitnn = fit.tolist()
    norm_v.append(n)
    path_v.append(c)
    fitness.append(fitnn)
  copy = n_path.assign(pred_MIC_norm=norm_v)
  copy1 = copy.assign(pathogenic_bacteria = path_gen['Bacteria'].tolist())
  copy2 = copy1.assign(pred_MIC_pathogen=path_v)
  copy3 = copy2.assign(Fitness = fitness)
  copy3 = copy3.sort_values('Fitness', ascending=False)
  copy3['pred_norm_MIC_original'] = 10** copy3['pred_MIC_norm']
  copy3['pred_path_MIC_original'] = 10** copy3['pred_MIC_pathogen']
  return copy3