import numpy as np 
import pandas as pd
from sklearn import decomposition
from result_display import show_result,export_anomaly
from reject_anomalies import pred_baseon_threshold,make_use_reject_anomalies
from Feature_engineer import remove_unwanted_col,feature_engineer_steps
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from joblib import dump,load


def remove_duplicate(df):
    df = df.drop_duplicates()
    return df

## categorical data option
# 3 different method for dealing with categorical missing value
# drop - drop the row with missing categorical value
# imputation - replace missing value with the most common category
# missing -  treat missing values as separate category
def fill_missing_value_categorical(df, method):
    object_cols = df.select_dtypes(include=['object','category']).columns
    if method == 'drop':
 
        df_cleaned = df.dropna(subset=object_cols)
        return df_cleaned
    if method == 'imputation':
        for column in object_cols:
            df[column].fillna(df[column].mode()[0], inplace=True)

        return df
    if method == 'missing':
        for column in object_cols:
            df[column].fillna('Missing', inplace=True)
        return df
    
## numerical data option
# 2 different method for dealing with numerical missing value
# drop - drop the row with missing categorical value
# mean - replace missing value with mean value in the column
def fill_missing_value_numerical(df, method):
    object_cols = df.select_dtypes(include=['int64','float64']).columns
    if method == 'drop':
        df_cleaned = df.dropna(subset=object_cols)
        return df_cleaned
    if method == 'mean':
        for column in object_cols:
            df['column'].fillna(df['column'].mean(), inplace=True)
        return df
def apply_PCA(X,n_components):
    pca = decomposition.PCA(n_components)
    X_centered = X - X.mean(axis=0)
    pca.fit(X_centered)
    X_centered = pca.transform(X_centered)    
    return X_centered    
    
#unclean_df = pd.read_csv("data/unclean.csv")
#print(unclean_df.dtypes)
# print(unclean_df.head)

# unclean_df = remove_duplicate(unclean_df)
# unclean_df = fill_missing_value_categorical(unclean_df, 'drop')
# unclean_df = fill_missing_value_numerical(unclean_df, 'drop')


