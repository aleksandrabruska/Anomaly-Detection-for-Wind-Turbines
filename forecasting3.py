import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import os
from sklearn.metrics import precision_score, recall_score, accuracy_score
import warnings

warnings.filterwarnings("ignore")

# Lista plików
train_files = ["25.csv", "69.csv", "13.csv", "24.csv", "3.csv", "17.csv", "38.csv", "71.csv", "14.csv", "92.csv"]
test_files = ["68.csv", "22.csv", "72.csv", "73.csv", "0.csv", "26.csv", "40.csv", "42.csv", "10.csv", "45.csv",
              "84.csv", "51.csv"]
all_files = train_files + test_files

# Wykorzystywane sensory
sensors = ["power_29_avg", "power_29_max", "power_29_min", "power_29_std",
           "power_30_avg", "power_30_max", "power_30_min", "power_30_std"]
base_path = r"Wind Farm A\zAnomaliami"


# Funkcje metryk
def CARE_coverage(y_true, y_pred):
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    beta = 0.5
    if precision + recall == 0:
        return 0
    f_beta = (1 + beta ** 2) * (precision * recall) / (beta ** 2 * precision + recall)
    return f_beta


def CARE_accuracy(y_true, y_pred):
    return accuracy_score(y_true, y_pred)


def CARE_reliability(event_true, event_pred):
    precision = precision_score(event_true, event_pred)
    recall = recall_score(event_true, event_pred)
    beta = 0.5
    if precision + recall == 0:
        return 0
    f_beta_event = (1 + beta ** 2) * (precision * recall) / (beta ** 2 * precision + recall)
    return f_beta_event


def CARE_earliness(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    if not np.any(y_true):
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


def compute_event_label_resampled(y_pred, y_true, threshold=72):
    criticality = 0
    max_criticality = 0
    for pred, true in zip(y_pred, y_true):
        if true == 0:
            if pred == 1:
                criticality += 1
            else:
                criticality = max(criticality - 1, 0)
        max_criticality = max(max_criticality, criticality)
    return int(max_criticality >= threshold)


# Trening modelu
def train_model(column_name):
    print(f"Training model for {column_name}")
    series_list = []
    for filename in train_files:
        file_path = os.path.join(base_path, filename)
        df = pd.read_csv(file_path, sep=";", parse_dates=['time_stamp'])
        df = df[['time_stamp', column_name]].dropna()
        df = df.set_index('time_stamp').resample('10T').mean().dropna()
        series_list.append(df[column_name])
    train_series = pd.concat(series_list, ignore_index=True)
    model = ARIMA(train_series, order=(3, 1, 2))
    fitted_model = model.fit()
    fitted_values = fitted_model.predict(start=0, end=len(train_series) - 1)
    train_error = np.abs(train_series - fitted_values)
    threshold = train_error.mean() + 1.5 * train_error.std()
    return fitted_model, threshold


def get_y_true(df):
    if 'ANOMALIA' in df.columns:
        df['anomaly'] = df['ANOMALIA'].astype(int)
    else:
        raise ValueError("Brakująca kolumna 'ANOMALIA' w danych.")
    y_true_resampled = df['anomaly'].resample('10T').max()
    return y_true_resampled



# Testowanie i ocena
def test_model(file_path, column_name, fitted_model, threshold):
    df = pd.read_csv(file_path, sep=";", parse_dates=['time_stamp'])
    df = df.set_index('time_stamp')

    sensor_resampled = df[column_name].resample('10T').mean()
    y_true_resampled = get_y_true(df)
    common_index = sensor_resampled.index.intersection(y_true_resampled.index)
    sensor_data = sensor_resampled.loc[common_index].dropna()
    y_true = y_true_resampled.loc[common_index].dropna()
    forecast = fitted_model.forecast(steps=len(sensor_data))
    forecast.index = sensor_data.index
    error = np.abs(sensor_data - forecast)
    y_pred_sensor = (error > threshold).astype(int)

    return y_true, y_pred_sensor


# Trening modeli dla każdego sensora
models = {sensor: train_model(sensor) for sensor in sensors}
true_events = []
pred_events = []

for file in all_files:
    print(f"\nPrzetwarzanie pliku: {file}")
    file_path = os.path.join(base_path, file)

    y_true = None
    y_pred_sensors = {}
    for sensor in sensors:
        y_true_sensor, y_pred_sensor = test_model(file_path, sensor, models[sensor][0], models[sensor][1])
        if y_true is None:
            y_true = y_true_sensor
        y_pred_sensors[sensor] = y_pred_sensor.reindex(y_true.index)

    y_pred_combined = np.any([y_pred_sensors[sensor].values for sensor in sensors], axis=0).astype(int)

    true_event = int(np.any(y_true))
    pred_event = compute_event_label_resampled(y_pred_combined, y_true)
    true_events.append(true_event)
    pred_events.append(pred_event)

    if true_event == 1:
        coverage = CARE_coverage(y_true, y_pred_combined)
        earliness = CARE_earliness(y_true, y_pred_combined)
        print(f"Plik anomalny - Coverage: {coverage:.4f}, Earliness: {earliness:.4f}")
    else:
        accuracy = CARE_accuracy(y_true, y_pred_combined)
        print(f"Plik normalny - Accuracy: {accuracy:.4f}")

# Obliczanie niezawodności dla wszystkich plików
reliability = CARE_reliability(true_events, pred_events)
print(f"\nCARE_reliability dla wszystkich zbiorów danych: {reliability:.4f}")
