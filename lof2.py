import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.impute import SimpleImputer
import warnings

warnings.filterwarnings("ignore") 

folder_path = 'Wind Farm A\datasets'
event_info_path = os.path.join('Wind Farm A', 'event_info.csv') 
all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

sensors = [
    'sensor_0_avg', 'sensor_1_avg', 'sensor_2_avg',
    'sensor_5_avg', 'sensor_5_min','sensor_5_std',
    'sensor_6_avg', 'sensor_7_avg', 'sensor_8_avg', 'sensor_9_avg', 'sensor_10_avg', 'sensor_11_avg',
    'sensor_12_avg', 'sensor_13_avg', 'sensor_14_avg', 'sensor_15_avg', 'sensor_16_avg', 'sensor_17_avg', 'sensor_18_avg',
    'sensor_18_max', 'sensor_18_min', 'sensor_18_std', 'sensor_19_avg', 'sensor_20_avg', 'sensor_21_avg', 'sensor_22_avg',
    'sensor_23_avg', 'sensor_24_avg', 'sensor_25_avg', 'sensor_26_avg', 'sensor_31_avg',
    'sensor_31_max', 'sensor_31_min', 'sensor_31_std', 'sensor_32_avg', 'sensor_33_avg', 'sensor_34_avg', 'sensor_35_avg', 'sensor_36_avg', 
    'sensor_37_avg', 'sensor_38_avg', 'sensor_39_avg', 'sensor_40_avg', 'sensor_41_avg', 'sensor_42_avg', 'sensor_43_avg', 'sensor_44', 
    'sensor_45', 'sensor_46', 'sensor_47', 'sensor_48', 'sensor_49', 'sensor_50', 'sensor_51', 'sensor_52_avg', 'sensor_52_max', 'sensor_52_min', 
    'sensor_52_std', 'sensor_53_avg'
]

def CARE_coverage(y_true, y_pred):
    y_true = (y_true > 0).astype(int)
    y_pred = (y_pred > 0).astype(int)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    beta = 0.5
    if precision + recall == 0:
        return 0
    f_beta = (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)
    return f_beta

def CARE_accuracy(y_true, y_pred):
    y_true = (y_true > 0).astype(int)
    y_pred = (y_pred > 0).astype(int)
    return accuracy_score(y_true, y_pred)

def CARE_reliability(event_true, event_pred):
    event_true = (np.array(event_true) > 0).astype(int)
    event_pred = (np.array(event_pred) > 0).astype(int)

    precision = precision_score(event_true, event_pred, zero_division=1)
    recall = recall_score(event_true, event_pred, zero_division=1)

    beta = 0.5
    if precision + recall == 0:
        return 0
    f_beta_event = (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)
    return f_beta_event


def CARE_earliness(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    if not np.any(y_true):  # no anomaly
        return 0

    anomaly_indices = np.where(y_true == 1)[0]
    start = anomaly_indices[0]
    end = anomaly_indices[-1]
    length = end - start + 1

    weights = np.ones(length)
    halfway = start + length // 2
    weights[length // 2:] = np.linspace(1, 0, length - length // 2)

    weighted_hits = sum(weights[i - start] for i in range(start, end + 1) if y_pred[i] == 1)
    total_weight = sum(weights)

    if total_weight == 0:
        return 0
    return weighted_hits / total_weight

def compute_event_label(y_pred, threshold):
    criticality = 0
    max_criticality = 0
    for pred in y_pred:
        if pred == 1: 
            criticality += 1
        else: 
            criticality = max(criticality - 1, 0) 
        max_criticality = max(max_criticality, criticality)

    return int(max_criticality >= threshold)

event_info_df = pd.read_csv(event_info_path, sep=";")
event_info_df['event_id_str'] = event_info_df['event_id'].astype(str)
event_info_df = event_info_df.set_index('event_id_str')

true_events = []
pred_events = []

event_detection_threshold = 25

for file in all_files:
    print(f"\nPlik: {file}")
    file_path = os.path.join(folder_path, file)
    event_id_from_filename = file.split('.')[0]

    df_original = pd.read_csv(file_path, sep=";", parse_dates=['time_stamp'])

    event_data_row = event_info_df.loc[event_id_from_filename]

    event_start = event_data_row['event_start_id']
    event_end = event_data_row['event_end_id']
    event_label = event_data_row['event_label']

    df_original['anomaly'] = 0 

    if event_label == 'anomaly':
        if event_end + 1 <= len(df_original):
             df_original.iloc[event_start : event_end + 1, df_original.columns.get_loc('anomaly')] = 1
        elif event_start < len(df_original):
             df_original.iloc[event_start : , df_original.columns.get_loc('anomaly')] = 1

    df = df_original.set_index('time_stamp')
    y_true_original_res = df['anomaly'].fillna(0).astype(int)

    sensor_data = []
    common_idx = df.index

    for sensor in sensors:
        series = df[sensor].reindex(common_idx)
        series.replace([np.inf, -np.inf], np.nan, inplace=True)
        sensor_data.append(series.values)

    X = np.vstack(sensor_data).T

    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)

    pca = PCA(n_components=15)
    X_pca = pca.fit_transform(X)

    lof = LocalOutlierFactor(n_neighbors=100, contamination='auto')
    lof.fit(X_pca)
    outlier_scores = lof.negative_outlier_factor_

    threshold_score = np.percentile(outlier_scores, 5)
    preds = (outlier_scores <= threshold_score).astype(int) 

    y_pred_original_res = pd.Series(preds, index=common_idx)
    y_true = y_true_original_res.reindex(y_pred_original_res.index).fillna(0).astype(int)

    true_event = int(np.any(y_true))

    pred_event = compute_event_label(
        y_pred_original_res.values, 
        event_detection_threshold 
    )

    if pred_event == 1:
        print(f"  -> Przewidziano zdarzenie anomalii")
    else:
        print(f"  -> Nie przewidziano zdarzenia anomalii")
    
    if true_event == 1: 
        coverage = CARE_coverage(y_true, y_pred_original_res)
        earliness = CARE_earliness(y_true, y_pred_original_res)
        print(f"Anomalia: Coverage: {coverage:.4f}, Earliness: {earliness:.4f}")
    else: 
        accuracy = CARE_accuracy(y_true, y_pred_original_res)
        print(f"Normalny: Accuracy: {accuracy:.4f}")

    true_events.append(true_event)
    pred_events.append(pred_event)

if true_events:
    reliability = CARE_reliability(true_events, pred_events)
    print(f"\nCARE_reliability (Globalnie): {reliability:.4f}")
else:
    print("\nNie przetworzono żadnych plików danych.")