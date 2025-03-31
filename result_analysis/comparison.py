import metrics
import numpy as np
import matplotlib.pyplot as plt

#TODO: Add other metrices to comparison
def compare(metric,true, **arg):
    f1, precision = dict.fromkeys(arg.keys()), dict.fromkeys(arg.keys())
    for key in arg.keys():
        f1[key] = metrics.calculate_f1(true, arg[key])
        precision[key] = metrics.calculate_precision(true, arg[key])

    results = {"F1": f1, "Precision" :precision}
    return results

def print_comparison(results):
    matrix = [list(results['F1'].values()), list(results['Precision'].values())]
    is_max = []
    for row in matrix:
        is_max.append([1 if v == max(row) else 0 for v in row])

    matrix = np.array(matrix)
    colors = np.where(matrix == 1, "green", "black")
    fig, ax = plt.subplots()
    ax.imshow(matrix, cmap="coolwarm", alpha=0.3)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, matrix[i, j].round(2), ha="center", va="center", color=colors[i, j], fontsize=14)

    row_labels = ["F1", "Precision"]
    col_labels = ["Approach no. " + str(i+1) for i in range(matrix.shape[1])]
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticklabels(row_labels)
    ax.set_xticklabels(col_labels)
    plt.show()

true = [0,0,0,1,1]
pred = [0,1,0,1,1]
pred2 = [1,1,0,1,1]
pred3 = [0,0,0,1,1]
pred4 = [0,0,0,1,1]

results = compare(1, true, predictions1 = pred, predictions2 = pred2, predictions3 = pred3, predictions4 = pred4)
print_comparison(results)