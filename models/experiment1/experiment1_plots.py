import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

color_dict = {
    "Shallow-MLP": "blue",
    "Deep-MLP": "green",
    "Shallow-CNN": "red",
    "Deep-CNN": "black",
    "SVM": "grey"
}


def create_accuracy_plot(df_results,  models=["Shallow-MLP", "Deep-MLP", "Shallow-CNN", "Deep-CNN", "SVM"]):
    """
    Plots accuracy against number of parameters for each model.
    """
    plt.figure()

    for model in models:
        df_mod = df_results[df_results["Model"] == model]
        if model != "SVM":
            plt.plot(np.log2(df_mod["NumParams"]), df_mod["TestAccuracy"],
                     color=color_dict[model], marker='o', ls='--', label=model.replace('-', ' '))
        else:
            plt.scatter(np.log2(
                df_mod["NumParams"]), df_mod["TestAccuracy"], s=100, marker='x', c='grey', label='SVM')

    plt.xticks([i for i in range(10, 22)])
    plt.xlabel("Log$_2$ of Number of Parameters")

    plt.ylabel("Test Accuracy")
    plt.title("Test Accuracy vs Log$_2$ of Number of Parameters")
    plt.ylim(0, 1)
    plt.legend(loc="lower right")

    plt.savefig(f"experiment-results/Exp1_Acc.png", dpi=300)


def create_pps_plot(df_results,  models=["Shallow-MLP", "Deep-MLP", "Shallow-CNN", "Deep-CNN", "SVM"]):
    """
    Plots packets per second (PPS) against number of parameters for each model.
    """
    fig, ax = plt.subplots()

    for model in models:
        df_mod = df_results[df_results["Model"] == model]
        if model != "SVM":
            ax.plot(np.log2(df_mod["NumParams"]), df_mod["PPS"],
                    color=color_dict[model], marker='o', ls='--', label=model.replace('-', ' '))
        else:
            ax.scatter(np.log2(
                df_mod["NumParams"]), df_mod["PPS"], s=100,  marker='x', c='grey', label='SVM$^*$')

    ax.set_xticks([i for i in range(10, 22)])
    ax.set_xlabel("Log$_2$ of Number of Parameters")

    ax.set_ylabel("Packets per second")
    ax.set_title(
        "Average Packets Predicted Per Second vs Log$_2$ of Number of Parameters")
    ax.set_ylim(-1000, 51000)

    ax.legend(loc="upper right")

    df_svm = df_results[df_results["Model"] == "SVM"]
    svm_pps = df_svm["PPS"].values[0]
    svm_pps_se = df_svm["PPS_StdError"].values[0]
    plt.figtext(0.05, 0.01, '$^*$SVM recorded {} $\pm$ {} packets per second, but has been omitted from the plot for readability.'.format(
        round(svm_pps, 1), round(svm_pps_se, 1)), horizontalalignment='left', fontsize=8, style='italic')

    plt.tight_layout(rect=[0, 0.03, 0.9, 0.9])

    plt.savefig(f"experiment-results/Exp1_PPS.png", dpi=300)


if __name__ == "__main__":
    df_results = pd.read_csv("experiment-results/Exp1Results.csv")
    create_accuracy_plot(df_results)
    create_pps_plot(df_results)
