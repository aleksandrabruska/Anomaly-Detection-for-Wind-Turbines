import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

folder_path = 'Wind Farm A\datasets'
all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

event_labels_df = pd.read_csv('Wind Farm A\event_info.csv', sep=';')
event_label_map = event_labels_df.set_index('event_id')['event_label'].to_dict()

results = {}
predicted_labels = []
true_labels = []
file_names_processed = []

# wybrane cechy
selected_features = [
    'sensor_0_avg', 'sensor_1_avg', 'sensor_2_avg',
    'wind_speed_3_avg', 'wind_speed_4_avg', 'wind_speed_3_max', 'wind_speed_3_min', 'wind_speed_3_std',
    'sensor_5_avg', 'sensor_5_min','sensor_5_std',
    'sensor_6_avg', 'sensor_7_avg', 'sensor_8_avg', 'sensor_9_avg', 'sensor_10_avg', 'sensor_11_avg',
    'sensor_12_avg', 'sensor_13_avg', 'sensor_14_avg', 'sensor_15_avg', 'sensor_16_avg', 'sensor_17_avg', 'sensor_18_avg',
    'sensor_18_max', 'sensor_18_min', 'sensor_18_std', 'sensor_19_avg', 'sensor_20_avg', 'sensor_21_avg', 'sensor_22_avg',
    'sensor_23_avg', 'sensor_24_avg', 'sensor_25_avg', 'sensor_26_avg', 'sensor_31_avg',
    'reactive_power_27_avg', 'reactive_power_27_max', 'reactive_power_27_min', 'reactive_power_27_std',
    'reactive_power_28_avg', 'reactive_power_28_max', 'reactive_power_28_min', 'reactive_power_28_std',
    'power_29_avg', 'power_29_max', 'power_29_min', 'power_29_std',
    'power_30_avg', 'power_30_max', 'power_30_min', 'power_30_std',
    'sensor_31_max', 'sensor_31_min', 'sensor_31_std', 'sensor_32_avg', 'sensor_33_avg', 'sensor_34_avg', 'sensor_35_avg', 'sensor_36_avg', 
    'sensor_37_avg', 'sensor_38_avg', 'sensor_39_avg', 'sensor_40_avg', 'sensor_41_avg', 'sensor_42_avg', 'sensor_43_avg', 'sensor_44', 
    'sensor_45', 'sensor_46', 'sensor_47', 'sensor_48', 'sensor_49', 'sensor_50', 'sensor_51', 'sensor_52_avg', 'sensor_52_max', 'sensor_52_min', 
    'sensor_52_std', 'sensor_53_avg'
]


for file_name in all_files:
    try:
        event_id_str = file_name.replace('.csv', '')
        if not event_id_str.isdigit():
            print(f"Pomijam plik o nieprawidłowej nazwie: {file_name}")
            continue
        event_id = int(event_id_str)

        df = pd.read_csv(os.path.join(folder_path, file_name), sep=';')
        print(f"\nPrzetwarzanie pliku: {file_name} (event_id: {event_id})")
        df['time_stamp'] = pd.to_datetime(df['time_stamp'])

        if df.empty:
            print(f"Plik {file_name} jest pusty.")
            results[file_name] = {'predicted_anomaly': False, 'true_anomaly': False}
            continue

        # Tylko wybrane kolumny i bez brakujacych danych
        data_for_clustering = df[selected_features].copy().dropna()

        predicted_anomaly = False
        if not data_for_clustering.empty:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data_for_clustering)
            
            n_components = 15 # na podstawie pliku pca.py
            pca = PCA(n_components=n_components)
            principal_components = pca.fit_transform(scaled_data)  

            #
            #TODO: nie wiadomo jak wykryc anomalie w plikach
            #

            # lof opisane w artykule
            lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
            y_pred = lof.fit_predict(principal_components)

            # -1 -> anomalia
            n_anomalies = np.sum(y_pred == -1)
            if n_anomalies > 0:
                predicted_anomaly = True
                print(f"  Wykryto {n_anomalies} anomalii w pliku xdd.")
            else:
                predicted_anomaly = False
                print(f"  Nie wykryto anomalii.")

        # faktyczna etykieta
        true_label = event_label_map.get(event_id)
        true_anomaly = True if true_label == 'anomaly' else False
        print(f"  Rzeczywista etykieta z event_labels.csv: {true_label}")

        results[file_name] = {'predicted_anomaly': predicted_anomaly, 'true_anomaly': true_anomaly}
        predicted_labels.append(predicted_anomaly)
        true_labels.append(true_anomaly)
        file_names_processed.append(file_name)

    except Exception as e:
        print(f"Błąd podczas przetwarzania pliku {file_name}: {e}")

print("\nOcena wyników:")

accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels)
recall = recall_score(true_labels, predicted_labels)
f1 = f1_score(true_labels, predicted_labels)

print(f"Dokładność: {accuracy:.2f}")