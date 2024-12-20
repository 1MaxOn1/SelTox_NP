import random
import V4_ga_compd_generation


in1 = ['Ag', 'Bacillus subtilis', 'non-pathogenic', 'green_synthesis', 'MBEC', 'tetragonal', 'Bacteria', 'Bacillota', 'Bacilli', 'Bacillales', 'Bacillaceae', 'Bacillus', 'p', 'carious dentine', 81.3794, 25.0, 24, 0.16, 30, 8, 22.60496136, 17.07, 0.6865, 4.082482905, 1.1264576600390903, 'Klebsiella pneumoniae', 1.1556311111157527, -0.02917345107666236, 13.380047648872358, 14.309719181697213]
in2 = ['Ag', 'Bacillus subtilis', 'non-pathogenic', 'green_synthesis', 'MBEC', 'spheroidal', 'Bacteria', 'Bacillota', 'Bacilli', 'Bacillales', 'Bacillaceae', 'Bacillus', 'p', 'soil', 107.8682, 20.0, 4, 0.16, 30, 11, 23.00188061, 0.0, 0.0, 1.78376517, 1.6384681472503022, 'Klebsiella pneumoniae', 1.3850132076587593, 0.25345493959154286, 43.497885651648765, 24.266838936839733]

indv2_list = V4_ga_compd_generation.fitness(V4_ga_compd_generation.population(size=50))
cross_over_frequency = 0.2
mutation_rate = 0.2


def to_crossover(indv1, indv2, cross_over_frequency):
    a = random.random()

    for each in range(1,len(indv1)):
        if (each ==4) or (each ==5) or (each == 15) or (each ==16):
            if random.random()< cross_over_frequency:
                indv1[each] = indv2[each]
            continue
        if a < cross_over_frequency:
            indv1[each] = indv2[each]

    return indv1


def to_mutation(individual1, mutation_rate):
    individual2 = indv2_list.iloc[random.randrange(20)].values.tolist()
    mut = to_crossover(individual1, individual2, mutation_rate)
    return mut