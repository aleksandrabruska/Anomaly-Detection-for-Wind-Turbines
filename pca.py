import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

folder_path = 'Wind Farm A\datasets'
# folder_path = 'C:\Szkola\sem6\Projekt Grupowy\Wind Farm A\datasets'
all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]


results = {}
predicted_labels = []
true_labels = []
file_names_processed = []

# Lista wybranych cech
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

            # Wybierz tylko wybrane cechy i usuń wiersze z brakami
            data_for_clustering = df[selected_features].copy().dropna()

            if not data_for_clustering.empty:
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(data_for_clustering)
                
                pca = PCA(n_components=40)
                X2D = pca.fit_transform(scaled_data)

                # plt.plot(pca.explained_variance_ratio_, '.b')
                # plt.show()

                plt.plot(np.cumsum(pca.explained_variance_ratio_), '.r')
                a = np.linspace(0, 40, 100)
                b = np.full_like(a, 0.95)
                plt.plot(a, b)
                plt.show()
    
        except Exception as e:
            print(f"Wystąpił błąd podczas przetwarzania pliku {file_name}: {e}")