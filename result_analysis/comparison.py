import metrics
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from metrics import create_confusion_matrix, create_PR_curve



def compare(true, **arg):
    f1, precision, fdr, mar, far = (dict.fromkeys(arg.keys()) for i in range(5))
    for key in arg.keys():
        f1[key] = metrics.calculate_f1(true, arg[key])
        precision[key] = metrics.calculate_precision(true, arg[key])
        fdr[key] = metrics.calculate_FDR(true, arg[key])
        mar[key] = metrics.calculate_MAR(true, arg[key])
        far[key] = metrics.calculate_FAR(true, arg[key])
    results = {"F1": f1, "Precision": precision, "FDR": fdr, "MAR": mar, "FAR": far}
    return results

def print_comparison(results):
    matrix = [list(results['F1'].values()), list(results['Precision'].values()), list(results['FDR'].values()), list(results['MAR'].values()), list(results['FAR'].values())]
    is_best = []
    for row in matrix[0:3]:
        is_best.append([1 if v == max(row) else 0 for v in row])
    for row in matrix[3:5]:
        is_best.append([1 if v == min(row) else 0 for v in row])
    matrix = np.array(matrix)
    is_best = np.array(is_best)
    colors = np.where(is_best == 1, "green", "black")

    fig, ax = plt.subplots()
    ax.imshow(matrix, cmap="coolwarm", alpha=0.3)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, matrix[i, j].round(2), ha="center", va="center", color=colors[i, j], fontsize=14)

    row_labels = ["F1", "Precision", "FDR", "MAR", "FAR"]
    col_labels = list(results['F1'].keys())
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticklabels(row_labels)
    ax.set_xticklabels(col_labels, rotation=45)
    plt.show(bbox_inches='tight')

def compare_PR(true, **kwargs):
    for key in kwargs.keys():
        precision, recall, threshold = create_PR_curve(true, kwargs[key], False)
        plt.plot(recall, precision, marker='.', label=key)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend()
    plt.grid()
    plt.show()

def compare_ROC(true, **kwargs):
    for key in kwargs.keys():
        fpr, tpr, thresholds = metrics.create_ROC_curve(true, kwargs[key], False)
        plt.plot(fpr, tpr, marker='.', label=key)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.grid()
    plt.show()

def compare_confusion_matrices(true, **kwargs):
    size = len(kwargs.keys())
    fig, axs = plt.subplots(size,1, figsize=(10, 10 * size) )
    i = 1
    for key in kwargs.keys():
        cm = create_confusion_matrix(true, kwargs[key], False)
        classes = ['Normal', 'Anomaly']
        disp = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm,
                                              display_labels=classes)
        disp.plot(ax = axs[i-1])
        i += 1
    plt.tight_layout()
    plt.show()


#example
"""
true = [0,0,0,1,1]
pred = [0,1,0,1,1]
pred2 = [1,1,0,1,1]
pred3 = [0,0,0, 0,1]
pred4 = [0,0,0,1,1]

score = [0.2, 0.3, 0.4, 0.5, 0.4]
score2 = [0.2, 0.0, 0.4, 0.5, 0.4]
score3 = [0.2, 0.3, 0.1, 0.3, 0.4]
score4 = [0.3, 0.3, 0.6, 0.5, 0.6]

results = compare(true, predictions1 = pred, predictions2 = pred2, predictions3 = pred3, predictions4 = pred4)
print(results)
print_comparison(results)
compare_PR(true, predictions1 = score, predictions2 = score2, predictions3 = score3, predictions4 = score4)
compare_ROC(true, predictions1 = score, predictions2 = score2, predictions3 = score3, predictions4 = score4)
compare_confusion_matrices(true, predictions1 = pred, predictions2 = pred2, predictions3 = pred3, predictions4 = pred4)
"""