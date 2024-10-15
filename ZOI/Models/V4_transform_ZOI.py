import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

preprocessed_data = pd.read_csv(r'ZOI\data\preprocessed_ZOI_dataset.csv')
X = preprocessed_data.drop(columns=['ZOI', 'reference'], axis=1)

columns_order = ['NP_Synthesis', 'shape', 'method', 'Bacteria', 'Phylum', 'Class', 'Order', 'Family', 'Superkingdom', 'bac_type', 'gram', 'isolated_from', 'Genus', 'Species', 'time (hr)', 'NP_concentration (μg/ml)', 'NP size_min (nm)', 'NP size_max (nm)', 'min_Incub_period, h', 'growth_temp, C', 'biosafety_level']

numerical_data = X.select_dtypes(include=['float', 'int'])
categorical_data = X.select_dtypes(include=['object'])

def transform(df):
    le = LabelEncoder()
    sc = StandardScaler()
    cat_transformed = df.select_dtypes(include = 'object').apply(le.fit_transform)
    num_transfromed = pd.DataFrame(
        data = sc.fit_transform(df.select_dtypes(include = 'number')),
        columns = df.select_dtypes(include = 'number').columns
    )
    return cat_transformed.join(num_transfromed).reset_index(drop = True).reindex(columns = columns_order)
    
    
