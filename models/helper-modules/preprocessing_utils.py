import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from math import sqrt


DEFAULT_FILE_SUFFIX = "10_10000"  # Dataset with 10 classes, 10000 packets in each
DEFAULT_DATA_PATH = f"../../data/{DEFAULT_FILE_SUFFIX}"
MAX_BYTE_VALUE = 255


def read_in_data(data_path=DEFAULT_DATA_PATH, file_suffix=DEFAULT_FILE_SUFFIX):
    """
    Returns df_train, df_val, df_test corresponding to the csv at the specified file path.

    e.g. data_path = "../../data/" and file_suffix = "10_10000" for data stored in 
         folder `data` named with `10_10000` suffix. 

    Example usage:

    df_train, df_val, df_test = read_in_data()
    """
    df_train = pd.read_csv(f"{data_path}/train_{file_suffix}.csv")
    df_val = pd.read_csv(f"{data_path}/val_{file_suffix}.csv")
    df_test = pd.read_csv(f"{data_path}/test_{file_suffix}.csv")

    return df_train, df_val, df_test


def preprocess(model_str, df_train, df_test, df_val):
    """
    Takes in train, val, and test data frames with columns `label`,
    and 1480 further columns with each byte from an IP payload.

    Returns numpy arrays: X_train, y_train, X_val, y_val, X_test, y_test 

    If model_str contains "MLP":
        X_train is of shape (m, 1480, 1) (m training examples, which are 1480 bytes in length)
        y_train is of shape (m, k, 1) (m training examples, one hot-encoded label with k classes)

    Else if model_str contains "CNN":
        X_train is of shape (m, 40, 37, 1) (m training examples, which are 40 x 37 byte images)
        y_train is of shape (m, k) (m training examples, one hot-encoded label with k classes)

    Else if model_str contains e.g. "SVM":
        X_train is of shape (m, 1480  1) (m training examples, which are 1480 bytes in length)
        y_train is of shape (m, ) (m training examples, with an integer encoded label)

    Example usage:

    (X_train, y_train), (X_val, y_val), (X_test, y_test) = preprocess("SVM", df_train, df_test, df_val)
    """
    # 1) Make copies so that that preprocessing changes leave original data frames unchanged
    df_train_copy = df_train.copy()
    df_val_copy = df_val.copy()
    df_test_copy = df_test.copy()

    # 2) Mask first 20 bytes
    df_train_copy[df_train_copy.columns[1:21]] = 0
    df_val_copy[df_val_copy.columns[1:21]] = 0
    df_test_copy[df_test_copy.columns[1:21]] = 0

    # 3) Create X_train, y_train, X_val, y_val, X_test, y_test
    X_train, y_train = df_train_copy.drop(
        'label', axis=1).values, df_train_copy["label"]
    X_val, y_val = df_val_copy.drop(
        'label', axis=1).values, df_val_copy["label"]
    X_test, y_test = df_test_copy.drop(
        'label', axis=1).values, df_test_copy["label"]

    # 4) Normalize the data
    X_train /= MAX_BYTE_VALUE
    X_val /= MAX_BYTE_VALUE
    X_test /= MAX_BYTE_VALUE

    # 5) Reshape the data into 2D image for CNNs
    if "CNN" in model_str:
        X_train = X_train.reshape(X_train.shape[0], 40, 37, 1)
        X_val = X_val.reshape(X_val.shape[0], 40, 37, 1)
        X_test = X_test.reshape(X_test.shape[0], 40, 37, 1)

    # 6) Encode labels as integers
    y_train = y_train.astype('category').cat.codes.values
    y_val = y_val.astype('category').cat.codes.values
    y_test = y_test.astype('category').cat.codes.values

    # 7) One hot encode for CNNs and MLPs
    if "CNN" in model_str or "MLP" in model_str:
        y_train = to_categorical(y_train)
        y_val = to_categorical(y_val)
        y_test = to_categorical(y_test)

    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def preprocess_varying_payloads(df_train, df_test, df_val, num_bytes=256):
    """
    Performs the preprocessing for a 2D-CNN given a specified payload size: `num_bytes`

    Note: `num_bytes` must be a perfect square

    Takes in train, val, and test data frames with columns `label`,
    and 1480 further columns with each byte from an IP payload.

    Returns numpy arrays: X_train, y_train, X_val, y_val, X_test, y_test 

    X_train is of shape (m, sqrt(num_bytes), sqrt(num_bytes), 1) (m training examples, which are sqrt(num_bytes) x sqrt(num_bytes) byte images)
    y_train is of shape (m, k) (m training examples, one hot-encoded label with k classes)
    """
    if int(sqrt(num_bytes))**2 != num_bytes:
        raise Exception("`num_bytes` must be a perfect square")

    # 1) Make copies so that that preprocessing changes leave original data frames unchanged
    df_train_copy = df_train.copy()
    df_val_copy = df_val.copy()
    df_test_copy = df_test.copy()

    # 2) Create X_train, y_train, X_val, y_val, X_test, y_test
    X_train, y_train = df_train_copy[df_train_copy.columns[21:21 +
                                                           num_bytes]].values, df_train_copy["label"]
    X_val, y_val = df_val_copy[df_val_copy.columns[21:21 +
                                                   num_bytes]].values, df_val_copy["label"]
    X_test, y_test = df_test_copy[df_test_copy.columns[21:21 +
                                                       num_bytes]].values, df_test_copy["label"]

    # 3) Normalize the data
    X_train /= MAX_BYTE_VALUE
    X_val /= MAX_BYTE_VALUE
    X_test /= MAX_BYTE_VALUE

    # 4) Reshape the data for CNN
    X_train = X_train.reshape(X_train.shape[0], int(
        sqrt(num_bytes)), int(sqrt(num_bytes)), 1)
    X_val = X_val.reshape(X_val.shape[0], int(
        sqrt(num_bytes)), int(sqrt(num_bytes)), 1)
    X_test = X_test.reshape(X_test.shape[0], int(
        sqrt(num_bytes)), int(sqrt(num_bytes)), 1)

    # 5) Encode labels as integers
    y_train = y_train.astype('category').cat.codes.values
    y_val = y_val.astype('category').cat.codes.values
    y_test = y_test.astype('category').cat.codes.values

    # 6) One hot encode
    y_train = to_categorical(y_train)
    y_val = to_categorical(y_val)
    y_test = to_categorical(y_test)

    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def read_in_test_data(data_path=DEFAULT_DATA_PATH, file_suffix=DEFAULT_FILE_SUFFIX):
    """
    Returns df_test corresponding to the csv at the specified file path.

    More efficient for memory purposes than `read_in_data` since does not require
    training and validation data in memory.

    e.g. data_path = "../../data/" and file_suffix = "10_10000" for data stored in 
         folder `data` named with `10_10000` suffix. 

    Example usage:

    df_test = read_in_test_data()
    """
    df_test = pd.read_csv(f"{data_path}/test_{file_suffix}.csv")

    return df_test


def preprocess_test(model_str, df_test):
    """
    Takes in train, val, and test data frames with columns "label" 
    and 1480 further columns with each byte from an IP payload.

    Returns numpy arrays: X_test, y_test 


    e.g. If model_str == "Shallow-MLP":
        X_test is of shape (m, 1480) (m training examples, which are 1480 bytes in length)
        y_test is of shape (m, k) (m training examples, one hot-encoded label with k classes)

    Example usage:

    (X_test, y_test) = preprocess("CNN", df_train, df_test, df_val)
    """
    MAX_BYTE_VALUE = 255

    # 1) Make copies so that that preprocessing changes leave original data frames unchanged
    df_test_copy = df_test.copy()

    # 2) Mask first 20 bytes
    df_test_copy[df_test_copy.columns[1:21]] = 0

    # 3) Create X_train, y_train, X_val, y_val, X_test, y_test
    X_test, y_test = df_test_copy.drop(
        'label', axis=1).values, df_test_copy["label"]

    # 4) Normalize the data
    X_test /= MAX_BYTE_VALUE

    # 5) Reshape the data for CNN
    if "CNN" in model_str:
        X_test = X_test.reshape(X_test.shape[0], 40, 37, 1)

    # 6) Encode labels as integers
    y_test = y_test.astype('category').cat.codes.values

    # 7) One hot encode
    if "CNN" in model_str or "MLP" in model_str:
        y_test = to_categorical(y_test)

    return (X_test, y_test)
