import sys
from tensorflow.keras.utils import to_categorical
import matplotlib
import logging
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import time
from sklearn.metrics import accuracy_score
import pickle
sys.path.append("../../helper-modules")
from preprocessing_utils import read_in_test_data, preprocess_test


MODELS_PATH = "trained-models/"


def get_best_model_nums(df_experiments):
    """ Extract from the experiment results, the indices (model number) of the highest validation accuracy model, for each given number of parameters. """
    return [df_experiments[df_experiments["NumParams"] == num_params]["ValAccuracy"].idxmax() for num_params in df_experiments["NumParams"].unique()]


def get_test_accuracy(model_type, model, X_test, y_test, verbose=False):
    """ Return the test accuracy for a given tf.keras model. """
    if model_type == "SVM":
        return accuracy_score(y_test, model.predict(X_test))
    return model.evaluate(X_test, y_test, verbose=1 if verbose else 0)[1]


def get_packets_per_sec(model, X_test_sample, n_trials=25, verbose=False):
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


def load_model_number(model_type, model_number):
    if model_type == "SVM":
        with open(MODELS_PATH + f"{model_type}_{model_number}.pkl", 'rb') as file:
            return pickle.load(file)
    return tf.keras.models.load_model(MODELS_PATH + f"{model_type}_{model_number}.h5")


def extract_results(df_experiments, model_type, df_test, verbose=False):
    """
    Given the results of an experiment as a data frame, output for each given number of parameters, 
    the test accuracies and average prediction time for the such model that had the highest validation
    accuracy. 

    model_type: str
      Either "Shallow-CNN", "Deep-CNN", "SVM", "Deep-MLP" or "Shallow-MLP"
    """
    (X_test, y_test) = preprocess_test(model_type, df_test)

    # Get the best validation accuracy models for each number of parameters
    best_model_numbers = get_best_model_nums(df_experiments)

    # To store the results for each model
    test_accuracies = []
    test_prediction_times = []
    test_pred_time_errors = []

    # Sample 5000 packets from the test set to use for calculating average prediction times
    SEED = 42
    np.random.seed(SEED)
    NUM_TO_SAMPLE = 10000
    X_test_sample = X_test[np.random.choice(
        X_test.shape[0], NUM_TO_SAMPLE, replace=False)]

    # Loop through each best model
    for model_number in best_model_numbers:

        # 1) Load the model
        if verbose:
            print(
                f"Loading {model_type} model {model_number} with {df_experiments.loc[model_number, 'NumParams']} parameters and validation accuracy {round(df_experiments.loc[model_number, 'ValAccuracy'], 4)}")
        model = load_model_number(model_type, model_number)

        # 2) Calculate and store its test accuracy
        if verbose:
            print("Calculating test accuracy...")
        test_accuracies.append(get_test_accuracy(
            model_type, model, X_test, y_test, verbose))

        # 3) Compute its average packet prediction time
        if verbose:
            print("Calculating average packets that can be predicted per second...")
        pred_time, err = get_packets_per_sec(
            model, X_test_sample, verbose=verbose)
        if verbose:
            print(
                f"Average: {round(pred_time,2)} packets per second (sd. error: {round(err,2)})")
        test_prediction_times.append(pred_time)
        test_pred_time_errors.append(err)

    # Output the results
    if verbose:
        for mod_no, acc, pred_time in zip(best_model_numbers, test_accuracies, test_prediction_times):
            print(f"{mod_no}: {acc} accuracy, {pred_time}ms average prediction time")

    results_dict = {"best_model_numbers": best_model_numbers,
                    "test_accuracies": test_accuracies,
                    "test_prediction_times": test_prediction_times,
                    "test_pred_time_errors": test_pred_time_errors}

    return results_dict


def main():
    # Read in the test data using preprocessing helper functions
    df_test = read_in_test_data()

    # Read in trained model results
    df_shal_cnn_experiments = pd.read_csv(
        "model-results/ExperimentLogs_Shallow-CNN.csv", sep=";").set_index('ModelNumber')
    df_deep_cnn_experiments = pd.read_csv(
        "model-results/ExperimentLogs_Deep-CNN.csv", sep=";").set_index('ModelNumber')
    df_shal_mlp_experiments = pd.read_csv(
        "model-results/ExperimentLogs_Shallow-MLP.csv", sep=";").set_index('ModelNumber')
    df_deep_mlp_experiments = pd.read_csv(
        "model-results/ExperimentLogs_Deep-MLP.csv", sep=";").set_index('ModelNumber')
    df_svm_experiments = pd.read_csv(
        "model-results/ExperimentLogs_SVM.csv", sep=";").set_index('ModelNumber')

    # Run the test accuracy and prediction speed experiments and extract results
    svm_results_dict = extract_results(
        df_svm_experiments, "SVM", df_test, verbose=True)
    shal_mlp_results_dict = extract_results(
        df_shal_mlp_experiments, "Shallow-MLP", df_test, verbose=True)
    deep_mlp_results_dict = extract_results(
        df_deep_mlp_experiments, "Deep-MLP", df_test, verbose=True)
    shal_cnn_results_dict = extract_results(
        df_shal_cnn_experiments, "Shallow-CNN", df_test, verbose=True)
    deep_cnn_results_dict = extract_results(
        df_deep_cnn_experiments, "Deep-CNN", df_test, verbose=True)

    # Create a single csv with all the experiment results
    df1 = pd.concat([pd.Series("Shallow-MLP"), pd.Series(df_shal_mlp_experiments["NumParams"].unique()), pd.Series(
        shal_mlp_results_dict["test_accuracies"]), pd.Series(shal_mlp_results_dict["test_prediction_times"]), pd.Series(shal_mlp_results_dict["test_pred_time_errors"])], axis=1).fillna("Shallow-MLP")
    df2 = pd.concat([pd.Series("Deep-MLP"), pd.Series(df_deep_mlp_experiments["NumParams"].unique()), pd.Series(
        deep_mlp_results_dict["test_accuracies"]), pd.Series(deep_mlp_results_dict["test_prediction_times"]), pd.Series(deep_mlp_results_dict["test_pred_time_errors"])],  axis=1).fillna("Deep-MLP")
    df3 = pd.concat([pd.Series("Shallow-CNN"), pd.Series(df_shal_cnn_experiments["NumParams"].unique()), pd.Series(
        shal_cnn_results_dict["test_accuracies"]), pd.Series(shal_cnn_results_dict["test_prediction_times"]), pd.Series(shal_cnn_results_dict["test_pred_time_errors"])], axis=1).fillna("Shallow-CNN")
    df4 = pd.concat([pd.Series("Deep-CNN"), pd.Series(df_deep_cnn_experiments["NumParams"].unique()), pd.Series(
        deep_cnn_results_dict["test_accuracies"]), pd.Series(deep_cnn_results_dict["test_prediction_times"]), pd.Series(deep_cnn_results_dict["test_pred_time_errors"])], axis=1).fillna("Deep-CNN")
    df5 = pd.concat([pd.Series("SVM"), pd.Series(df_svm_experiments["NumParams"].unique()), pd.Series(
        svm_results_dict["test_accuracies"]), pd.Series(svm_results_dict["test_prediction_times"]), pd.Series(svm_results_dict["test_pred_time_errors"])], axis=1).fillna("SVM")
    df_results = pd.concat([df1, df2, df3, df4, df5])
    df_results.columns = ["Model", "NumParams",
                          "TestAccuracy", "PPS", "PPS_StdError"]
    df_results.to_csv('Exp1_Results.csv', index=False)


if __name__ == "__main__":
    main()
