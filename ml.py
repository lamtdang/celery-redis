import json
import pickle
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import numpy as np
from multiprocessing import Manager


def train_model(data_source):
    names = ['sepal-length', 'sepal-width',
             'petal-length', 'petal-width', 'class']
    dataset = read_csv(data_source, names=names)
    # Split-out validation dataset
    array = dataset.values
    X = array[:, 0:4]
    y = array[:, 4]
    X_train, X_validation, Y_train, Y_validation = train_test_split(
        X, y, test_size=0.20, random_state=1)
    # Make predictions on validation dataset
    model = SVC(gamma='auto')
    model.fit(X_train, Y_train)

    return pickle.dumps(model)


def predict(model_bin, data_source):
    model = pickle.loads(model_bin)
    pred_input = np.array(data_source)
    pred_result = model.predict(pred_input)
    return pred_result
