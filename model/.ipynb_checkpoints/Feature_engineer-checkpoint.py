
import numpy as np 
import pandas as pd
from datetime import datetime
#feature engineering 
# create another column to have Manhattan distance on customer and terminal Lat and log 
# create column to check if terminal_id is in available terminals
# create column to have difference between mean amount and amount
# create column to have difference between mean number of transaction and the number of transaction
# the day that the transaction belongs to
def location_difference(df, allow_range=0.3):
    df['location_different'] = np.sqrt(abs((abs(df['lat_terminal'] - df['lat_customer'])**2-abs(df['log_terminal'] - df['log_customer'])**2)))
    return df
def using_available_terminals(df):    
    df['using_available_terminals'] = df.apply(lambda row: row['terminal_id'] in row['available_terminals'], axis=1)
    return df
def convert_timestamp(df):
    df['post_ts'] = pd.to_datetime(df['post_ts'])
    df['timestamp_numeric'] = df['post_ts'].apply(lambda x: datetime.timestamp(x))
    return df
def amt_mean_difference(df):
    df['mean_difference'] = df['amt'] - df['mean_amount']
    return df
    
def mean_transaction_per_day_difference(df):
    
    df['timestamp'] = pd.to_datetime(df['post_ts'])
    df['date'] = df['timestamp'].dt.date
    
    df['per_day_difference_count'] = df.groupby(['customer_id', 'date'])['transaction_id'].transform('count')
    
    return df

def convert_category(df):
    one_hot_encoded_df = pd.get_dummies(df, columns=['entry_mode','network_id']) #one hot encoding for categorical data
    train_X = one_hot_encoded_df.drop(['fraud','fraud_scenario'], axis=1)
    train_y = one_hot_encoded_df[['fraud']]    
    return train_X, train_y

def feature_engineer_steps(df):
    df = location_difference(df)
    df = using_available_terminals(df)
    df = mean_transaction_per_day_difference(df)
    df = amt_mean_difference(df)
    df = convert_timestamp(df)
    train_X, train_y = convert_category(df)
    return train_X, train_y

def remove_unwanted_col(train):
    
    columns =  list(train.columns)
    entries_to_remove = ['transaction_id', # remove unwanted column, and all the mostly IDs
                         'bin_y',
                         'mcc',
                         'bin_x',
                         'customer_id', 
                         'available_terminals',
                         'terminal_id',
                         'timestamp',                     
                         #'lat_terminal',
                         #'log_terminal',
                         #'lat_customer',
                         #'log_customer',
                         #'mean_amount',
                         #'mean_nb_tx_per_day',
                         'date',
                         'post_ts',
                         'using_available_terminals',
                            #'timestamp_numeric',
                         #'per_day_difference_count',
                         
                         ] 
    features = [col for col in columns if col not in entries_to_remove]
    train = train[features]
    return train