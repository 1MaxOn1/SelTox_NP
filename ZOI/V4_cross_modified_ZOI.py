import random
from V4_ga_compd_generation_ZOI import fitness, population

in1 = ['Ag', 'Bacillus subtilis', 'non-pathogenic', 'chemical_synthesis', 'disk_diffusion', 'rod-shaped', 'Bacteria', 'Bacillota', 'Bacilli', 'Bacillales', 'Bacillaceae', 'Bacillus', 'p', 'soil', 7.6, 44.45, 0.16, 7.08, 30, 11, 63.546, 1, 1.519480519, 0.444480519, 4.219480519, 0.675379491, 15.570224, 'Staphylococcus aureus', 15.375084, -0.19513988494873047]
in2 = ['Ag', 'Bacillus subtilis', 'non-pathogenic', 'green_synthesis', 'disc_diffusion', 'cubic', 'Bacteria', 'Bacillota', 'Bacilli', 'Bacillales', 'Bacillaceae', 'Bacillus', 'p', 'soil', 7.95454, 34.0, 0.16, 7.08, 30, 16, 79.865, 3, 3.314285714, 2.314285714, 2.314285714, 2.556734694, 3.2289157, 'Staphylococcus aureus', 7.373609, 4.144693374633789]

indv2_list = fitness(population(size=50))

cross_over_frequency = 0.2
mutation_rate = 0.2

def crossover(indv1, indv2, cross_over_frequency):
    a = random.random()
    
    for each in range(1, len(indv1)):
        if each == 3 or each == 4 or each == 5 or each == 14 or each == 15:
            if random.random() < cross_over_frequency:
                indv1[each] = indv2[each]
            continue
        if a < cross_over_frequency:
            indv1[each] = indv2[each]
            
        return indv1
    
    
def mutation(individual1, mutation_rate):
    print
    individual2 = indv2_list.iloc[random.randrange(20)].values.tolist()
    mut = crossover(individual1, individual2, mutation_rate)
    return mut