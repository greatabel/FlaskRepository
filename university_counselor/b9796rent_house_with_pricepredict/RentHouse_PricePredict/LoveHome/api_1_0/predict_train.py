import numpy as np
import sklearn.preprocessing as sp
import sklearn.model_selection as ms
import sklearn.svm as svm
import sklearn.metrics as sm
import sklearn.naive_bayes as nb

import pickle

class MyEncoder:
    """
    数字与字符串互转
    """

    def fit_transform(self, y):
        return y.astype(float)

    def transform(self, y):
        return y.astype(float)

    def inverse_transform(self, y):
        return y.astype(str)




