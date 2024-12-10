import pandas as pd
import V4_ga_compd_generation
import V4_crossing_mutation
import time
import os

mutation_rate = 0.2
cross_over_rate = 0.2

def new_generations(Gen, population_size):
    half = int((population_size * 0.5)+1)
    selected = Gen.iloc[:half,:]
    new = [selected, V4_ga_compd_generation.fitness(V4_ga_compd_generation.population(half))]
    new_generation_input = pd.concat(new)
    new_generation_input.reset_index(drop=True, inplace=True)
    new_gen = V4_crossing_mutation.evolve_crossing(new_generation_input, cross_over_rate, mutation_rate)
    new_gen.reset_index(drop=True, inplace=True)
    return new_gen


means = []
maxs = []
def Genetic_Algorithm(generation_number, population_size, output_dir):
    Generation1 = V4_ga_compd_generation.fitness(V4_ga_compd_generation.population(population_size)).sort_values('Fitness', ascending=False)
    mean1 = Generation1['Fitness'].mean()
    max1 = Generation1['Fitness'].max()
    Generation1.to_csv(f'{output_dir}/pop_size_{population_size}_Generation_1.csv')
    Generation2 = V4_crossing_mutation.evolve_crossing(Generation1, cross_over_rate, mutation_rate)
    mean2 = Generation2['Fitness'].mean()
    max2 = Generation2['Fitness'].max()
    Generation2.to_csv(f'{output_dir}/pop_size_{population_size}_Generation_2.csv')
    Generation_next = Generation2
    means = [ mean1, mean2]
    maxs = [max1, max2]
    g = 3
    while g in range(generation_number + 1):
        Generation_next = new_generations(Generation_next, population_size)
        mean = Generation_next['Fitness'].mean()
        max = Generation_next['Fitness'].max()
        Generation_next.to_csv(f'{output_dir}/pop_size_{population_size}_Generation_{g}.csv')
        means.append(mean)
        maxs.append(max)

        g += 1

    genn = generation_number + 1
    gens = list(range(1,genn))
    summary = pd.DataFrame( list(zip( gens, means, maxs)), columns= ['generations','mean', 'max'] )
    print(summary)
    summary.to_csv(f'{output_dir}/summary_pop_size_{population_size}_gen_{generation_number}.csv')
    return Generation_next


# def final_loop():
#     pop_col = []
#     time_all = []
#     gen_col = []
#     gen = 100
#     while gen <= 100:
#         population_size = 70
#         while population_size <= 70:
#             st = time.time()
#             Genetic_Algorithm(gen, population_size)
#             gen_col.append(gen)
#             escape_time = time.time() - st
#             time_all.append(escape_time)
#             pop_col.append(population_size)
#             print('Escape time:', escape_time)
#             population_size += 10
#         gen +=10
#         et = pd.DataFrame(list(zip(pop_col, gen_col, time_all)), columns=['population_size','Generation number', 'Time'])
#         et.to_csv(r'MIC/output/B_sub_vs_a_pleuroneumoniae/Time_' + str(population_size) + '.csv')

# final_loop()


def final_loop(bacteria_df):
    base_output_dir = 'MIC/output'
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    pop_col = []
    time_all = []
    gen_col = []
    gen = 100 

    while gen <= 100:
        population_size = 50  
        while population_size <= 80:
            for _, row in bacteria_df.iterrows():
                bacteria_name = row['Bacteria']
                bac_type = row['bac_type']
                bacteria_output_dir = f'{base_output_dir}/{bacteria_name}_{bac_type}'
                os.makedirs(bacteria_output_dir, exist_ok=True)
                st = time.time()
                Genetic_Algorithm(gen, population_size, bacteria_output_dir)
                escape_time = time.time() - st
                gen_col.append(gen)
                time_all.append(escape_time)
                pop_col.append(population_size)

            population_size += 10
        gen += 10

    et = pd.DataFrame(list(zip(pop_col, gen_col, time_all)), columns=['population_size', 'Generation number', 'Time'])
    et.to_csv(f'{base_output_dir}/Time_summary.csv', index=False)


bacteria_df = pd.read_csv('MIC\data\MIC_before_preprocessed.csv')
final_loop(bacteria_df)

