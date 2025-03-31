from sklearn import metrics
import matplotlib.pyplot as plt

#1 - anomaly
#0 - normal

def calculate_f1(y_true, y_pred):
    return metrics.f1_score(y_true, y_pred)

def calculate_precision(y_true, y_pred):
    return metrics.precision_score(y_true, y_pred)

#FRD: Fault Detection Rate
#(Recall, true positive rate)
def calculate_FDR(y_true, y_pred):
    return metrics.recall_score(y_true, y_pred)

#MAR: Missed Alarm Rate
def calculate_MAR(y_true, y_pred):
    return 1 - calculate_FDR(y_true, y_pred)

#FAR: False Alarm Rate
#1 - specifity
def calculate_FAR(y_true, y_pred):
    return 1 - metrics.recall_score(y_true, y_pred, pos_label=0)

def create_confusion_matrix(y_true, y_pred, disp = True):
    cm = metrics.confusion_matrix(y_true, y_pred)
    classes = ['Normal', 'Anomaly']
    if disp:
        disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cm,
                           display_labels=classes)
        disp.plot()
        plt.show()
    return cm

#y_scores are probabilities
def create_PR_curve(y_true, y_scores, disp = True):
    precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_scores)
    if disp:
        plt.figure(figsize=(6, 6))
        plt.plot(recall, precision, marker='.', label='Precision-Recall Curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend()
        plt.grid()
        plt.show()
    return precision, recall, thresholds

#true positive rate vs false positive rate
def create_ROC_curve(y_true, y_scores, disp = True):
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_scores)
    if disp:
        plt.figure(figsize=(6, 6))
        plt.plot(fpr, tpr, marker='.')
        plt.ylabel('Fault Detection Rate (True Positive Rate)')
        plt.xlabel('False Alarm Rate(False Positive Rate)')
        plt.title('Precision-Recall Curve')
        plt.legend()
        plt.grid()
        plt.show()
    return fpr, tpr, thresholds

#example
"""
true = [0,0,0,1,1]
pred = [0,1,0,1,1]
prob = [0.2, 0.4, 0.2, 0.3, 0.8]
print(calculate_FDR(true, pred))
print(calculate_MAR(true, pred))
print(calculate_FAR(true, pred))
print(create_confusion_matrix(true, pred))
print(create_PR_curve(true, prob))
print(create_ROC_curve(true, prob))
"""

