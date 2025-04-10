import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import os
import warnings
warnings.filterwarnings("ignore")

train_files = ["25.csv", "69.csv", "13.csv", "24.csv", "3.csv", "17.csv", "38.csv", "71.csv", "14.csv", "92.csv"]
test_files = ["68.csv", "22.csv", "72.csv", "73.csv", "0.csv", "26.csv", "40.csv", "42.csv", "10.csv", "45.csv", "84.csv", "51.csv"]
sensor_date = [
    "sensor_0_avg", "sensor_1_avg", "sensor_2_avg", "wind_speed_3_avg", "wind_speed_4_avg",
    "wind_speed_3_max", "wind_speed_3_min", "wind_speed_3_std",
    "sensor_5_avg", "sensor_5_max", "sensor_5_min", "sensor_5_std",
    "sensor_6_avg", "sensor_7_avg", "sensor_8_avg", "sensor_9_avg", "sensor_10_avg", "sensor_11_avg",
    "sensor_12_avg", "sensor_13_avg", "sensor_14_avg", "sensor_15_avg", "sensor_16_avg", "sensor_17_avg",
    "sensor_18_avg", "sensor_18_max", "sensor_18_min", "sensor_18_std",
    "sensor_19_avg", "sensor_20_avg", "sensor_21_avg", "sensor_22_avg", "sensor_23_avg", "sensor_24_avg",
    "sensor_25_avg", "sensor_26_avg",
    "reactive_power_27_avg", "reactive_power_27_max", "reactive_power_27_min", "reactive_power_27_std",
    "reactive_power_28_avg", "reactive_power_28_max", "reactive_power_28_min", "reactive_power_28_std",
    "power_29_avg", "power_29_max", "power_29_min", "power_29_std",
    "power_30_avg", "power_30_max", "power_30_min", "power_30_std",
    "sensor_31_avg", "sensor_31_max", "sensor_31_min", "sensor_31_std",
    "sensor_32_avg", "sensor_33_avg", "sensor_34_avg", "sensor_35_avg", "sensor_36_avg", "sensor_37_avg",
    "sensor_38_avg", "sensor_39_avg", "sensor_40_avg", "sensor_41_avg", "sensor_42_avg", "sensor_43_avg",
    "sensor_44", "sensor_45", "sensor_46", "sensor_47", "sensor_48", "sensor_49", "sensor_50", "sensor_51",
    "sensor_52_avg", "sensor_52_max", "sensor_52_min", "sensor_52_std", "sensor_53_avg"
]

sensor_date = [
     "power_29_avg", "power_29_max", "power_29_min", "power_29_std",
    "power_30_avg", "power_30_max", "power_30_min", "power_30_std"]

base_path = r"Wind Farm A\datasets"



def train_model(column_name):
    print("Training model for " + column_name)
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


def test_model(test_file, column_name, fitted_model, threshold):
    file_path = os.path.join(base_path, test_file)
    test_df = pd.read_csv(file_path, sep=";", parse_dates=['time_stamp'])
    test_df = test_df[['time_stamp', column_name]].dropna()
    test_df = test_df.set_index('time_stamp').resample('10T').mean().dropna()

    forecast_steps = len(test_df)
    forecast = fitted_model.forecast(steps=forecast_steps)
    forecast.index = test_df.index
    error = np.abs(test_df[column_name] - forecast)
    anomalies = error > threshold
    percent = 100 * anomalies.sum() / len(anomalies)

    return percent






a_level = 42.0

models = []
for i in sensor_date:
    models.append(train_model(i))

correct_detection = 0

for i in range(0, len(test_files)):
    print("Testing file "+test_files[i])
    result = []
    for j in range(0, len(sensor_date)):

        result.append(test_model(test_files[i], sensor_date[j], models[j][0], models[j][1]))
        #print("     "+test_files[i] + " " + sensor_date[j] + " " + str(result[j]) + "%")

    anomaly_level = sum(result) / len(result)
    print("Average anomaly "+str(anomaly_level)+"%")
    if anomaly_level > a_level:
        correct_detection+=1
        print("FILE WITH ANOMALIES # correct")
    else: print("FILE WITHOUT ANOMALIES # wrong")


for i in range(0, len(train_files)):
    print("Testing file "+train_files[i])
    result = []
    for j in range(0, len(sensor_date)):

        result.append(test_model(train_files[i], sensor_date[j], models[j][0], models[j][1]))
        #print("     "+test_files[i] + " " + sensor_date[j] + " " + str(result[j]) + "%")

    anomaly_level = sum(result) / len(result)
    print("Average anomaly "+str(anomaly_level)+"%")
    if anomaly_level > a_level: print("FILE WITH ANOMALIES # wrong")
    else:
        correct_detection+=1
        print("FILE WITHOUT ANOMALIES # correct")

MODEL = correct_detection/len(train_files+test_files)
print("Accuracy: "+str(MODEL))
