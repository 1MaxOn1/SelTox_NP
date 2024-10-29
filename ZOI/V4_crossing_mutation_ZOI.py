import random
import pandas as pd
from V4_ga_compd_generation_ZOI import fitness, population
from V4_cross_modified_ZOI import crossover, mutation

population_size = 100
mutation_rate = 0.3
cross_over_rate = 0.3

df = fitness(population(population_size)).sort_values('Fitness', ascending = False)
df = df.reset_index(drop=True)

def evolve_crossing(df_compound_list, cross_over_rate, mutation_rate):
    original = df_compound_list
    unique = list()
    length = len(original) - 1
    j = 0
    while j < length:
        if str(original.iloc[[j], [0]].values) == str(original.iloc[[j+1], [0]].values):
            unique.append(original.iloc[j].values.tolist())
            j += 1
        else:
            unique.append(original.iloc[j].values.tolist())
        j+=1
    dff = pd.DataFrame(unique, columns=original.columns)
    
    i = 0
    selected_ind = list()
    while i < len(dff):
        individual1 = dff.iloc[i].values.tolist()
        individual2 = dff.iloc[random.randint(0, len(dff) -1)].values.tolist()
        cross_individual = crossover(individual1, individual2, cross_over_rate)
        mutate_individual = mutation(cross_individual, mutation_rate)
        selected_ind.append(mutate_individual)
        i+=1
    dframe = pd.DataFrame(selected_ind, columns=df_compound_list.columns)
    dframe_copy = dframe.copy(deep=True)
    dframe_copy = dframe_copy.iloc[:, :-4]
    dframe_evolved = fitness(dframe_copy)
    
    selecetion = list()
    
    for i in range(len(dff)):
        if dff.iloc[i, -1] >= dframe_evolved.iloc[i,-1]:
            selecetion.append(dff.iloc[i].values.tolist())
        else:
            selecetion.append(dframe_evolved.iloc[i].values.tolist())
            
    select_single = list()
    
    df_new = pd.DataFrame(selecetion, columns=df_compound_list.columns)
    
    all_sort = df_new.sort_values('Fitness', ascending=False)
    all_sort.reset_index(drop=True, inplace=True)
    
    without_selecction = pd.DataFrame(dframe_evolved, columns=df_compound_list.columns)
    
    return all_sort