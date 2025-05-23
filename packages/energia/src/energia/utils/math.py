"""Utilities to perform mathematical operations
"""

from math import erf, exp, pi, sqrt

import numpy
from pandas import DataFrame, concat
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def norm_constant(p, mu, sigma) -> float:
    """Calculates the normal constant

    Args:
        p (float): level of complaince
        mu (float): mean
        sigma (float): standard deviation

    Returns:
        float: normal constant
    """
    x = mu + erf(1 / sqrt(2) * p) * sigma * sqrt(2)
    return 1 / (sigma * sqrt(2 * pi)) * exp(-((x - mu) ** 2) / (2 * sigma**2))


def scaler(input_df: DataFrame, scale: list, child_scale: list = None) -> DataFrame:
    """creates a scaled list from a DataFrame object

    Args:
        input_df (DataFrame): df with values to be scaled
        parent_scale (list): scale to project into
        child_scale (list): scale to project

    Returns:
        DataFrame: scaled values
    """

    cols = list(input_df.columns)
    scaled_df = DataFrame()
    for col in cols:
        if child_scale is not None:
            col_names = [str(col) + '-' + str(i) for i in range(len(child_scale))]
            reshaped_df = numpy.reshape(
                input_df[col].values, (len(scale), len(child_scale))
            )
        else:
            col_names = [col]
            # reshaped_df = input_df
            if len(cols) > 1:
                reshaped_df = numpy.reshape(input_df[col].values, (len(scale), 1))
            else:
                reshaped_df = input_df

        scaler = StandardScaler().fit(reshaped_df)

        scaled_iter = DataFrame(scaler.transform(reshaped_df), columns=col_names)
        scaled_df = concat([scaled_df, scaled_iter], axis=1)
    return scaled_df


def find_euclidean_distance(cluster_node_a: list, cluster_node_b: list) -> float:
    """finds euclidean distances between two cluster nodes

    Args:
        cluster_node_a (float): index tag for cluster node a
        cluster_node_b (float): index tag for cluster node b

    Returns:
        float: euclidean distance
    """
    euclidean_distance_ = [(a - b) ** 2 for a, b in zip(cluster_node_a, cluster_node_b)]
    euclidean_distance_ = sum(euclidean_distance_)
    return euclidean_distance_


def generate_connectivity_matrix(scale_len) -> numpy.array:
    """generates a connectivity matrixto maintain chronology [..1,0,1..]

    Returns:
        numpy.array: matrix with connectivity relations
    """
    connect_ = numpy.zeros((scale_len, scale_len), dtype=int)
    for i_ in range(len(connect_)):

        if i_ == 0:
            # connect_[i,364] = 1 #uncomment these to generate a cyclic matrix
            connect_[i_, 1] = 1
        elif i_ == scale_len - 1:
            connect_[i_, scale_len - 2] = 1
            # connect_[i,0] = 1
        else:
            connect_[i_, i_ - 1] = 1
            connect_[i_, i_ + 1] = 1
    return connect_


def min_max(data: numpy.array | DataFrame) -> numpy.array | DataFrame:
    """min max for data

    Args:
        data (numpy.array | DataFrame): time-series data

    Returns:
        numpy.array | DataFrame: min-maxed data array
    """
    min_data = numpy.min(data)
    max_data = numpy.max(data)
    data = (data - numpy.min(data)) / (max_data - min_data)

    return data


def normalize(data: numpy.array | DataFrame) -> numpy.array | DataFrame:
    """normalizes data

    Args:
        data (numpy.array | DataFrame): time-series data

    Returns:
        numpy.array | DataFrame: min-maxed data array
    """
    scaler = MinMaxScaler()
    data = numpy.array(data).reshape(-1, 1)
    data = scaler.fit_transform(data)
    # max_data = numpy.max(data)
    # data = data / max_data

    return data
