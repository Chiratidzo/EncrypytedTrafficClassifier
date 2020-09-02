import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.utils import to_categorical


DEFAULT_FILE_SUFFIX = "10_10000"  # Dataset with 10 classes, 10000 packets in each
DEFAULT_DATA_PATH = f"../../data/{DEFAULT_FILE_SUFFIX}"
MAX_BYTE_VALUE = 255


def read_in_data(data_path=DEFAULT_DATA_PATH, file_suffix=DEFAULT_FILE_SUFFIX):
    """
    Returns df_train, df_val, df_test corresponding to the csv at the specified file path.

    e.g. data_path = "../../data/" and file_suffix = "12_10000" for data stored in 
         folder `data` named with `12_10000` suffix. 

    Example usage:

    df_train, df_val, df_test = read_in_data()
    """
    df_train = pd.read_csv(f"{data_path}/train_{file_suffix}.csv")
    df_val = pd.read_csv(f"{data_path}/val_{file_suffix}.csv")
    df_test = pd.read_csv(f"{data_path}/test_{file_suffix}.csv")

    return df_train, df_val, df_test


def preprocess_2d_cnn(df_train, df_test, df_val):
    """
    Takes in train, val, and test data frames with columns "label" 
    and 1480 further columns with each byte from an IP payload.

    Returns numpy arrays: X_train, y_train, X_val, y_val, X_test, y_test 

    X_train is of shape (m, 40, 37, 1) (m training examples, which are 40 x 37, with 1 depth layer)
    y_train is of shape (m, k) (m training examples, one hot-encoded label with k classes)

    Example usage:

    (X_train, y_train), (X_val, y_val), (X_test, y_test) = preprocess_2d_cnn(df_train, df_test, df_val)
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
        'label', axis=1), df_train_copy["label"]
    X_val, y_val = df_val_copy.drop('label', axis=1), df_val_copy["label"]
    X_test, y_test = df_test_copy.drop('label', axis=1), df_test_copy["label"]

    # 4) Normalize the data
    X_train /= MAX_BYTE_VALUE
    X_val /= MAX_BYTE_VALUE
    X_test /= MAX_BYTE_VALUE

    # 5) Reshape the data for CNN
    X_train = X_train.values.reshape(X_train.shape[0], 40, 37, 1)
    X_val = X_val.values.reshape(X_val.shape[0], 40, 37, 1)
    X_test = X_test.values.reshape(X_test.shape[0], 40, 37, 1)

    # 6) Encode labels as integers
    y_train = y_train.astype('category').cat.codes.values
    y_val = y_val.astype('category').cat.codes.values
    y_test = y_test.astype('category').cat.codes.values

    # 7) One hot encode
    y_train = to_categorical(y_train)
    y_val = to_categorical(y_val)
    y_test = to_categorical(y_test)

    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def create_tf_datasets(X_train, y_train, X_val, y_val, X_test, y_test):
    """
    Example usage: train_dataset, val_dataset, test_dataset = 
                    create_tf_datasets(X_train, y_train, X_val, y_val, X_test, y_test)
    """
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val))
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))
    return train_dataset, val_dataset, test_dataset


def test():
    # Read in the data
    df_train, df_val, df_test = read_in_data()

    # Create (X_train, y_train), (X_val, y_val), (X_test, y_test)
    (X_train, y_train), (X_val, y_val), (X_test,
                                         y_test) = preprocess_2d_cnn(df_train, df_test, df_val)

    # TF datasets
    train_dataset, val_dataset, test_dataset = create_tf_datasets(
        X_train, y_train, X_val, y_val, X_test, y_test)


if __name__ == "__main__":
    test()
