from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import accuracy_score
import numpy as np

#TODO: For coverage data samples with abnormal ID should be ignored

#ONLY for anomalous datasets
def CARE_coverage(y_true, y_pred):
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    beta = 0.5
    if precision + recall == 0:
        return 0
    f_beta = (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)
    return f_beta

#ONLY normal datasets
def CARE_accuracy(y_true, y_pred):
    return accuracy_score(y_true, y_pred)

#for whole DATASETS, not points
def CARE_reliability(event_true, event_pred):
    # event_true and event_pred are binary labels (0: normal, 1: anomaly event) per dataset
    precision = precision_score(event_true, event_pred)
    recall = recall_score(event_true, event_pred)
    beta = 0.5
    if precision + recall == 0:
        return 0
    f_beta_event = (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)
    return f_beta_event

#ONLY for anomalous datasets
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


#required for computing reliability
def compute_event_label(y_pred, status_ids, threshold=72):
    criticality = 0
    max_criticality = 0

    for pred, status in zip(y_pred, status_ids):
        if status in [0, 2]:  # only normal operation or idling
            if pred == 1:
                criticality += 1
            else:
                criticality = max(criticality - 1, 0)
        # if status abnormal, do nothing
        max_criticality = max(max_criticality, criticality)

    return int(max_criticality >= threshold)


