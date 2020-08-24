import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

# Read in the data to df_train, df_val and df_test
DEFAULT_FILE_SUFFIX = "12_10000"  # Dataset with 12 classes, 10000 packets in each
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

    Returns X_train, y_train, X_val, y_val, X_test, y_test numpy arrays

    Example usage:

    (X_train, y_train), (X_val, y_val), (X_test, y_test) = preprocess_2d_cnn(df_train, df_test, df_val)
    """
    # 1) Create X_train, y_train, X_val, y_val, X_test, y_test
    X_train, y_train = df_train.drop('label', axis=1), df_train["label"]
    X_val, y_val = df_val.drop('label', axis=1), df_val["label"]
    X_test, y_test = df_test.drop('label', axis=1), df_test["label"]

    # 2) Normalize the data
    X_train /= MAX_BYTE_VALUE
    X_val /= MAX_BYTE_VALUE
    X_test /= MAX_BYTE_VALUE

    # 3) Reshape the data for CNN
    X_train = X_train.values.reshape(X_train.shape[0], 40, 37, 1)
    X_val = X_val.values.reshape(X_val.shape[0], 40, 37, 1)
    X_test = X_test.values.reshape(X_test.shape[0], 40, 37, 1)

    # 4) Encode labels as integers
    y_train = y_train.astype('category').cat.codes.values
    y_val = y_val.astype('category').cat.codes.values
    y_test = y_test.astype('category').cat.codes.values

    # 5) One hot encode
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
    df_train, df_val, df_test = read_in_data("../../data/6_5000", "6_5000")
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = preprocess_2d_cnn(df_train,
                                                                             df_test,
                                                                             df_val)
    print(y_train.shape)
    print(type(X_train), type(y_train))
    train_dataset = create_tf_datasets(
        X_train, y_train, X_val, y_val, X_test, y_test)

    print(train_dataset)

    for feat, targ in train_dataset.take(5):
        print('Features: {}, Target: {}'.format(feat, targ))


if __name__ == "__main__":
    test()
