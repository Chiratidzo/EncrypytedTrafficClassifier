import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix_inner(y_true, y_pred, classes,
                                normalize=False,
                                title=None,
                                cmap=plt.cm.binary):
    """
    Plots a confusion matrix given a list of ground-truth values and 
    corresponding predictions.
    """
    np.set_printoptions(precision=2)

    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    fig, ax = plt.subplots(figsize=(7, 7))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)

    # Show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # Label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


def plot_conf_mtx(model, X, y, df, normalize=False, title="2D-CNN confusion matrix"):
    """
    Plots a confusion matrix using our given X and y numpy arrays e.g X_val, y_val
    """
    # Making predictions
    y_pred = np.argmax(model.predict(X), axis=-1)
    y_true = np.argmax(y, axis=1)

    # Extract label corresponding to each integer prediction
    label_map = dict(enumerate(df['label'].astype('category').cat.categories))
    class_names = [label_map[i] for i in range(10)]

    # Plotting normalized confusion matrix
    plot_confusion_matrix_inner(y_true, y_pred, classes=class_names, normalize=normalize,
                                title=title, cmap=plt.cm.binary)
