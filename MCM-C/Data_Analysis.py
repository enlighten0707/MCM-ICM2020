import numpy as np
from math import *
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def PCA(x, k):
    """
        The Principle Component Analysis (PCA) function computes uncorrelated linear combination of features.

        PCA takes two inputs:
            X (An m * n Matrix) - Initial Dataset (Feature Scaling Done),
            k (Postive Integer) - The Number of Principle Components.

        PCA returns two outputs:
            Z (An m * k Matrix) - Compressed Dataset (from X),
            W (An n * 1 Vector) - Weights of features in X. (Temporarily Banned)

        PCA also prints the proportion of varience retained in Compressed Dataset Z.
    """
    ss = StandardScaler()
    X = ss.fit_transform(x)
    m, n = np.shape(X)[0], np.shape(X)[1]
    sigma = 1 / m * np.transpose(X).dot(X)
    [U, S, V] = np.linalg.svd(sigma)
    U_reduce = U[:,0:k]
    init_weight = np.transpose(U_reduce)
    Z = np.transpose(init_weight.dot(np.transpose(X)))
    v_tot = np.sum(S)
    v_ret = np.sum(S[0:k])
    ret_percent = int(v_ret / v_tot * 10000) / 100
    print(str(ret_percent) + '%', 'of varience is retained.')
    print(init_weight)
    return -Z

def Entropy(X):
    """
        The Entropy function computes the weight of features based on the concept of information entropy.

        Entropy takes one input:
            X - Initial Data.

        Entropy returns one output:
            W - Weights of Featrues.
    """
    ss = MinMaxScaler()
    std_X = ss.fit_transform(X)
    sum_X = np.sum(std_X, 0)
    m, n = np.shape(X)[0], np.shape(X)[1]
    p, p_ln_p = np.zeros((m, n)), np.zeros((m, n))
    E, W = np.zeros(n), np.zeros(n)
    for i in range(m):
        for j in range(n):
            p[i][j] = std_X[i][j] / sum_X[j]
            if p[i][j] != 0:
                p_ln_p[i][j] = p[i][j] * log(p[i][j])
    for j in range(n):
        E[j] = np.sum(p_ln_p[:, j]) * (-1 / log(m))
    S = np.sum(E)
    for j in range(n):
        W[j] = (1 - E[j]) / (n - S)
    return W

def Squared_Error(y_test, y_pred):
    """
        Compute the Squared Error of Regression Prediction
    """
    m = np.shape(y_test)[0]
    error = y_pred - y_test
    se = 1 / m * np.sum(error * error)
    return se