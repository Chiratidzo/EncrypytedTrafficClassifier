import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_results(results):
    """
    Plots accuracy and prediction speed (PPS) against number of bytes of payload used.
    """
    fig, ax1 = plt.subplots()

    # x data is number of bytes
    x_data = np.sqrt(np.array(results['num_bytes']))

    # 1) Plot accuracy resuls:
    color = 'black'
    ax1.set_title(
        'Accuracy and Average Packets Per Second vs $\sqrt{\mathrm{Input\ Size}}$')
    ax1.set_xlabel(
        '$\sqrt{\mathrm{Size\ of\ input\ (number\ of\ bytes\ of\ payload\ used)}}$')
    ax1.set_ylabel('Packets per second', color=color)
    ax1.plot(x_data, results['test_prediction_times'], markersize=5,
             marker='o', ls='--', color=color, label='Reduced input')

    # Row 21 contains the deep 2D-CNN with 32 filters per layer results
    full_payload_results = pd.read_csv(
        'experiment-results/Exp1_Results.csv').iloc[21]
    full_acc = full_payload_results['TestAccuracy']
    full_pps = full_payload_results['PPS']
    full_pps_err = full_payload_results['PPS_StdError']

    ax1.scatter(np.sqrt(1480), full_pps, s=100, marker='x',
                color=color, label='Full input')
    ax1.tick_params(axis='y', labelcolor=color)

    ax1.legend(loc='upper center')

    ax1.set_ylim(0, 35000)

    # 2) Plot prediction speed resuls:

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'red'
    ax2.set_ylabel('Test accuracy', color=color)
    ax2.plot(x_data, results['test_accuracies'],
             marker='o', ls='--', markersize=5, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.scatter(np.sqrt(1480), full_acc, s=100, marker='x', color=color)
    ax2.set_xticks(x_data)
    ax2.set_ylim(0.76, 0.9)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig(f"experiment-results/Exp2_Bytes.png", dpi=300)

    plt.show()


def main():
    results = pd.read_csv('experiment-results/Exp2_Results.csv')

    plot_results(results)


if __name__ == "__main__":
    main()
