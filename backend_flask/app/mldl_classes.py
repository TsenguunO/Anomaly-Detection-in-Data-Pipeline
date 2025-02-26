
import numpy as np 
import pandas as pd
from datetime import datetime

class ChinIsolationForestCls():
    def __init__(self, cc_trans_dataframe: pd.DataFrame) -> None:
        self.cc_trans_df = cc_trans_dataframe
        self.has_done_pipeline = False

    def _is_weekend(self, tx_datetime):
    
        # Transform date into weekday (0 is Monday, 6 is Sunday)
        weekday = tx_datetime.weekday()
        # Binary value: 0 if weekday, 1 if weekend
        is_weekend = weekday>=5
        
        return int(is_weekend)

    def _is_night(self, tx_datetime):
        
        # Get the hour of the transaction
        tx_hour = tx_datetime.hour
        # Binary value: 1 if hour less than 6, and 0 otherwise
        is_night = tx_hour<=6
        
        return int(is_night)

    def _get_customer_spending_behaviour_features(self, customer_transactions, windows_size_in_days=[1,7,30]):
        
        # Let us first order transactions chronologically
        customer_transactions=customer_transactions.sort_values('post_ts')
        
        # The transaction date and time is set as the index, which will allow the use of the rolling function 
        customer_transactions.index=customer_transactions.post_ts
        
        # For each window size
        for window_size in windows_size_in_days:
            
            # Compute the sum of the transaction amounts and the number of transactions for the given window size
            SUM_AMOUNT_TX_WINDOW=customer_transactions['amt'].rolling(str(window_size)+'d').sum()
            NB_TX_WINDOW=customer_transactions['amt'].rolling(str(window_size)+'d').count()
        
            # Compute the average transaction amount for the given window size
            # NB_TX_WINDOW is always >0 since current transaction is always included
            AVG_AMOUNT_TX_WINDOW=SUM_AMOUNT_TX_WINDOW/NB_TX_WINDOW
        
            # Save feature values
            customer_transactions['customer_id_nb_tx_'+str(window_size)+'day_window']=list(NB_TX_WINDOW)
            customer_transactions['customer_id_avg_amount_'+str(window_size)+'day_window']=list(AVG_AMOUNT_TX_WINDOW)
        
        # Reindex according to transaction IDs
        customer_transactions.index=customer_transactions.transaction_id
            
        # And return the dataframe with the new features
        return customer_transactions

    def _get_count_risk_rolling_window(self, terminal_transactions, delay_period=7, windows_size_in_days=[1,7,30], feature="terminal_id"):
        
        terminal_transactions=terminal_transactions.sort_values('post_ts')
        
        terminal_transactions.index=terminal_transactions.post_ts
        
        NB_FRAUD_DELAY=terminal_transactions['fraud'].rolling(str(delay_period)+'d').sum()
        NB_TX_DELAY=terminal_transactions['fraud'].rolling(str(delay_period)+'d').count()
        
        for window_size in windows_size_in_days:
        
            NB_FRAUD_DELAY_WINDOW=terminal_transactions['fraud'].rolling(str(delay_period+window_size)+'d').sum()
            NB_TX_DELAY_WINDOW=terminal_transactions['fraud'].rolling(str(delay_period+window_size)+'d').count()
        
            NB_FRAUD_WINDOW=NB_FRAUD_DELAY_WINDOW-NB_FRAUD_DELAY
            NB_TX_WINDOW=NB_TX_DELAY_WINDOW-NB_TX_DELAY
        
            RISK_WINDOW=NB_FRAUD_WINDOW/NB_TX_WINDOW
            
            terminal_transactions[feature+'_nb_tx_'+str(window_size)+'day_window']=list(NB_TX_WINDOW)
            terminal_transactions[feature+'_risk_'+str(window_size)+'day_window']=list(RISK_WINDOW)
            
        terminal_transactions.index=terminal_transactions.transaction_id
        
        # Replace NA values with 0 (all undefined risk scores where NB_TX_WINDOW is 0) 
        terminal_transactions.fillna(0,inplace=True)
        
        return terminal_transactions

    def ml_train_pipeline(self, is_train=True):
        # Load the dataset
        data = []
        y = None
        if is_train:
            data = self.cc_trans_df[self.cc_trans_df['post_ts'] > pd.Timestamp("2022-08-01")]
        else:
            data = self.cc_trans_df
        

        # Separate features (F1, F2, F3) and target (TARGET)
        columns =  list(self.cc_trans_df.columns)

        # Entries you want to remove
        entries_to_remove = ['transaction_id', 'customer_id', 'bin', 'entry_mode', 
                            'terminal_id', 'fraud', 'fraud_scenario',
                            'terminal_id_nb_tx_1day_window', 'terminal_id_risk_1day_window',
                            'terminal_id_nb_tx_7day_window', 'terminal_id_risk_7day_window',
                            'terminal_id_nb_tx_30day_window', 'terminal_id_risk_30day_window'
                            ]
        target = 'fraud'
        # Remove the entries
        features = [col for col in columns if col not in entries_to_remove]

        X = data[features]
        y = None
        try:
            y = data[target]
        except Exception as e:
            pass

        # Save feature names and target name to a JSON file
        ml_metadata = {
            'features': features,
            'target': target,
            'model_type':  'Scikit-Learn'
        }

        X_train = None
        y_train = None
        X_test = X
        y_test = y

        if is_train:
            # Define the traing range max limit
            end_training = pd.Timestamp('2023-03-31')

            # Split the data into training and testing sets
            X_train = X[X['post_ts'] <= end_training]
            y_train = y.loc[X_train.index]
            X_test = X[X['post_ts'] > end_training]
            y_test =  y.loc[X_test.index]

            # Drop teh column post_ts
            X_train = X_train.drop(columns=['post_ts'])
            X_test = X_test.drop(columns=['post_ts'])

        return X_train, y_train, X_test, y_test, ml_metadata

    
    def perform_pipeline(self):
        self.cc_trans_df['post_ts'] = pd.to_datetime(self.cc_trans_df['post_ts'])
        self.cc_trans_df['during_weekend']=self.cc_trans_df.post_ts.apply(self._is_weekend)
        self.cc_trans_df['during_night']=self.cc_trans_df.post_ts.apply(self._is_night)
        self.cc_trans_df=self.cc_trans_df.groupby('customer_id', group_keys=True).apply(self._get_customer_spending_behaviour_features, include_groups=False)
        self.cc_trans_df=self.cc_trans_df.sort_values('post_ts').reset_index(drop=True)
        self.cc_trans_df=self.cc_trans_df.groupby('terminal_id', group_keys=True).apply(self._get_count_risk_rolling_window, include_groups=False)
        self.cc_trans_df=self.cc_trans_df.sort_values('post_ts').reset_index(drop=True)


class IsolationForestCls():
    def __init__(self, cc_dataframe: pd.DataFrame) -> None:
        self.df = cc_dataframe

    def _location_difference(self, allow_range=0.3):
        self.df['location_different'] = np.sqrt(abs((abs(self.df['lat_terminal'] - self.df['lat_customer'])**2-abs(self.df['log_terminal'] - self.df['log_customer'])**2)))
    
    def _using_available_terminals(self):
        self.df['using_available_terminals'] = self.df.apply(lambda row: row['terminal_id'] in row['available_terminals'], axis=1)

    def _convert_timestamp(self):
        self.df['post_ts'] = pd.to_datetime(self.df['post_ts'])
        self.df['timestamp_numeric'] = self.df['post_ts'].apply(lambda x: datetime.timestamp(x))

    def _amt_mean_difference(self):
        self.df['mean_difference'] = self.df['amt'] - self.df['mean_amount']
        
    def _mean_transaction_per_day_difference(self):
        self.df['timestamp'] = pd.to_datetime(self.df['post_ts'])
        self.df['date'] = self.df['timestamp'].dt.date
        self.df['per_day_difference_count'] = self.df.groupby(['customer_id', 'date'])['transaction_id'].transform('count')

    def _convert_category(self):
        one_hot_encoded_df = pd.get_dummies(self.df, columns=['entry_mode','network_id']) #one hot encoding for categorical data
        train_X = one_hot_encoded_df.drop(['fraud','fraud_scenario'], axis=1)
        train_y = one_hot_encoded_df[['fraud']]    
        return train_X, train_y

    def feature_engineer_steps(self):
        self._location_difference()
        self._using_available_terminals()
        self._mean_transaction_per_day_difference()
        self._amt_mean_difference()
        self._convert_timestamp()
        train_X, train_y = self._convert_category()
        train_X = self._remove_unwanted_col(train_X)
        return train_X, train_y

    #  Feature selection as part of the default pipeline
    def _remove_unwanted_col(cc_dataframe: pd.DataFrame):
        columns =  list(cc_dataframe.columns)
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
        cc_dataframe = cc_dataframe[features]
        return cc_dataframe
    
