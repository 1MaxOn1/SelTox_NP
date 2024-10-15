    copy = n_path.assign(pred_ZOI_norm = norm_v)
    copy1 = copy.assign(pathogenic_bacteria = path_gen['Bacteria'].tolist())
    copy2 = copy1.assign(pred_ZOI_pathogen = path_v)
    copy3 = copy2.assign(Fitness = fitness)
    copy3 = copy3.sort_values('Fitness', ascending = False)
    return copy3