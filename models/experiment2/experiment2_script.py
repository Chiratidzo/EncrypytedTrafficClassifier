
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import accuracy_score
import time
from math import sqrt
import sys
sys.path.append("../../helper-modules")
from preprocessing_utils import read_in_test_data, preprocess_test


MODELS_PATH = "trained-models/"


def get_best_model_nums(df_experiments):
    """ Extract from the experiment results, the indices (model number) of the highest validation accuracy model, for each given number of bytes. """
    return [df_experiments[df_experiments["NumBytes"] == num_bytes]["ValAccuracy"].idxmax() for num_bytes in df_experiments["NumBytes"].unique()]


def load_model_number(model_number):
    """ Loads the keras h5 file corresponding to a given model number."""
    return tf.keras.models.load_model(MODELS_PATH + f"Deep-CNN_{model_number}.h5")


def get_test_accuracy(model, X_test, y_test, verbose=False):
    """ Return the test accuracy for a given tf.keras model. """
    return model.evaluate(X_test, y_test, verbose=1 if verbose else 0)[1]


def get_model_num_bytes(df_experiments, model_number):
    """ Gets the number of bytes (payload size) used for a given model number. """
    return df_experiments[df_experiments.index == model_number]["NumBytes"].values[0]


def get_packets_per_sec(model, X_test_sample, n_trials=25):
    """ For a given model, return the average (of `n_trials` trials) packets that can be predicted per second,
        as well as the standard error. """

    # Track prediction time for each trial
    test_prediction_times = []
    num_packets = X_test_sample.shape[0]

    for i in range(n_trials+1):
        start = time.time()
        model.predict(X_test_sample)
        end = time.time()
        time_taken = (end - start)
        test_prediction_times.append(time_taken)

    test_prediction_times = test_prediction_times[1:]
    avg_packets = num_packets / np.mean(test_prediction_times)
    std_err = np.std(
        num_packets / np.array(test_prediction_times)) / (n_trials ** 0.5)

    return avg_packets, std_err


def extract_results(df_experiments, verbose=False):
    """
    Given the results of an experiment as a data frame, output for each given number of bytes, 
    the test accuracies and average prediction time for the such model that had the highest validation
    accuracy. 
    """
    # Get the best validation accuracy models for each number of parameters
    best_model_numbers = get_best_model_nums(
        df_experiments[df_experiments["NumFiltersPerLayer"] == ' (32, 32, 32, 32)'])

    # To store the results for each model
    test_accuracies = []
    test_prediction_times = []
    test_pred_time_errors = []

    # Read in the test data for use in the experiments
    df_test = read_in_test_data()

    # Loop through each best model
    for model_number in best_model_numbers:
        num_bytes = get_model_num_bytes(df_experiments, model_number)
        X_test, y_test = preprocess_test(df_test, num_bytes)

        # Sample 5000 packets from the test set to use for calculating average prediction times
        SEED = 42
        np.random.seed(SEED)
        NUM_TO_SAMPLE = 10000
        X_test_sample = X_test[np.random.choice(
            X_test.shape[0], NUM_TO_SAMPLE, replace=False)]

        # 1) Load the model
        if verbose:
            print(
                f"Loading model {model_number} with {df_experiments.loc[model_number, 'NumParams']} parameters and validation accuracy {round(df_experiments.loc[model_number, 'ValAccuracy'], 4)}")
        model = load_model_number(model_number)

        # 2) Calculate and store its test accuracy
        if verbose:
            print("Calculating test accuracy...")
        test_accuracies.append(get_test_accuracy(
            model, X_test, y_test, verbose))

        # 3) Compute its average packet prediction time
        if verbose:
            print("Calculating average packets that can be predicted per second...")
        pred_time, err = get_packets_per_sec(model, X_test_sample)
        if verbose:
            print(
                f"Average: {round(pred_time,2)} packets per second (sd. error: {round(err,2)})")
        test_prediction_times.append(pred_time)
        test_pred_time_errors.append(err)

    # Output the results
    if verbose:
        for mod_no, acc, pred_time in zip(best_model_numbers, test_accuracies, test_prediction_times):
            print(f"{mod_no}: {acc} accuracy, {pred_time}ms average prediction time")

    results_dict = {"num_bytes": [get_model_num_bytes(df_experiments, mod_no) for mod_no in best_model_numbers],
                    "test_accuracies": test_accuracies,
                    "test_prediction_times": test_prediction_times,
                    "test_pred_time_errors": test_pred_time_errors}

    return results_dict


def main():
    # Read in training results
    df_experiments = pd.read_csv(
        'ExperimentLogs_PayloadSizes.csv', sep=";").set_index('ModelNumber')

    # Run experiment and extract results
    results = extract_results(df_experiments, verbose=True)

    # Output results to a csv
    pd.DataFrame(results).sort_values('num_bytes').to_csv(
        'Exp2_Results.csv', index=False)


if __name__ == "__main__":
    main()
