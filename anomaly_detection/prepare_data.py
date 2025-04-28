import os
import pandas as pd
from sklearn.metrics import accuracy_score
from tf_slim.metrics import accuracy
from xgboost import XGBRegressor
import numpy as np
import sklearn

dataset_dir_path = '../../../data/Care_To_Compare/Wind Farm A/Wind Farm A/datasets'
event_file_path = '../../../data/Care_To_Compare/Wind Farm A/Wind Farm A/event_info.csv'

def generate_train_prediction(rows, event_data, lagging = 0):
    train_data, prediction_data = {}, {}
    for row in rows:
        event_id = event_data.loc[row, 'event_id']

        turbine_data = pd.read_csv(dataset_dir_path + '/' + str(event_id) + '.csv', sep=';')


        turbine_data = create_lag_features(turbine_data, lagging)

        train_data_piece = turbine_data[turbine_data['train_test'] == 'train']
        prediction_data_piece = turbine_data[turbine_data['train_test'] == 'prediction']

        train_data[row] = train_data_piece
        prediction_data[row] = prediction_data_piece
    return train_data, prediction_data


def generate_ground_truth(event_data, prediction_data):
    for row, df in prediction_data.items():
        event_start = event_data.loc[row, 'event_start_id']
        event_end = event_data.loc[row, 'event_end_id']
        if event_data.loc[row, 'event_label'] == 'anomaly':
            df['is_anomaly'] = df['id'].between(event_start, event_end)
        else:
            df['is_anomaly'] = False

    return prediction_data

def create_lag_features(df, window_size=1):
    if window_size == 0:
        return df
    df_lag = df.copy()
    for i in range(1, window_size + 1):
        lagged = df.shift(i).add_suffix(f"_lag_{i}")
        df_lag = pd.concat([df_lag, lagged], axis=1)
    return df_lag.dropna()