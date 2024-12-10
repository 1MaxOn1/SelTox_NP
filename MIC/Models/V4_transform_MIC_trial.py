import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder


df_MIC = pd.read_csv(r'D:\SelTox_NP\MIC\data\MIC_before_preprocessed.csv')
df_model = df_MIC.drop(['Unnamed: 0'], axis=1)
all = df_model.reset_index(drop=True)

numerical = all.select_dtypes(include=['int', 'float64'])
categorical = all.select_dtypes(include=['object'])

cat_col = categorical.columns
num_col = numerical.columns


def transform(data):
    le = LabelEncoder()
    le.fit(categorical.values.flatten())  # Fit the encoder on all categorical data
    Xc_all = categorical.apply(le.transform)
    Xct = data[cat_col].apply(le.transform)

    sc = StandardScaler()
    X_all = sc.fit_transform(numerical)
    X_ss = sc.transform(data[num_col])
    X_sc = pd.DataFrame(X_ss, columns=num_col)
    join = pd.concat([Xct, X_sc], axis=1)
    return join


def first_transform(data):
    le = LabelEncoder()
    le.fit(data.select_dtypes(include=['object']).values.flatten())  # Fit the encoder on all categorical data
    Xct = data.select_dtypes(include=['object']).apply(le.transform)
    Xct.reset_index(drop=True)

    sc = StandardScaler()
    X_all = sc.fit_transform(data.select_dtypes(include=['int', 'float64']))
    X_ss = sc.transform(data[data.select_dtypes(include=['int', 'float64']).columns])
    X_sc = pd.DataFrame(X_ss, columns=data.select_dtypes(include=['int', 'float64']).columns)
    join = pd.concat([Xct, X_sc], axis=1)
    return join