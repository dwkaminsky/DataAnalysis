from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from config import base_path
from test_class_algos.fetch_data import get_test_df, split_into_test_train
import pandas as pd
import numpy as np


def test_all_models():
    df = pd.read_csv(base_path() + '/data/test_data.csv')
    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST = split_into_test_train(df)
    scaler = StandardScaler()
    scaler.fit(X_TRAIN)
    X_TRAIN = scaler.transform(X_TRAIN)
    scaler_1 = StandardScaler()
    scaler_1.fit(X_TEST)
    X_TEST = scaler_1.transform(X_TEST)
    #    ADA
    # ada_clf = AdaBoostClassifier(n_estimators=200, random_state=0, learning_rate=0.5)
    # ada_clf.fit(X_TRAIN, Y_TRAIN)
    # test_output = ada_clf.predict(X_TEST)
    # print(np.mean(abs(test_output - Y_TEST)))
    # gbm_clf = GradientBoostingClassifier()
    # gbm_clf.fit(X_TRAIN, Y_TRAIN)
    # test_output = gbm_clf.predict(X_TEST)
    # print(np.mean(abs(test_output - Y_TEST)))
    # #    LOGREG
    # logreg_clf = LogisticRegression(random_state=0, max_iter=1000)
    # logreg_clf.fit(X_TRAIN, Y_TRAIN)
    # test_output = logreg_clf.predict_proba(X_TEST)[:, 1]
    # print(np.mean(abs(test_output - Y_TEST)))
    # #    Nonlin SVC
    # nonlin_svc_clf = GaussianNB()
    # print('Started fit')
    # nonlin_svc_clf.fit(X_TRAIN, Y_TRAIN)
    # print('Started predict')
    # test_output = nonlin_svc_clf.predict_proba(X_TEST)[:, 1]
    # print(np.mean(abs(test_output - Y_TEST)))
    #    NN
    nn_clf = MLPClassifier(alpha=1, max_iter=1000, hidden_layer_sizes=(20, 10, 5, 2))
    nn_clf.fit(X_TRAIN, Y_TRAIN)
    test_output = nn_clf.predict_proba(X_TEST)[:, 1]
    print(np.mean(abs(test_output - Y_TEST)))


def get_model(X_TRAIN, Y_TRAIN):
    gbm_clf = GradientBoostingClassifier()
    gbm_clf.fit(X_TRAIN, Y_TRAIN)
    return gbm_clf


def train_against_other_players(df, X, Y, player):
    X_TRAIN = []
    Y_TRAIN = []
    X_player_and_prev = []
    Y_player_and_prev = []
    for idx in range(len(df)):
        if df.loc[idx, 'Player'] != player:
            X_TRAIN.append(list(X.iloc[idx]))
            Y_TRAIN.append(Y[idx])
        elif idx>0:
            X_player_and_prev.append(list(X.iloc[idx]))
            X_player_and_prev.append(list(X.iloc[idx-1]))
            Y_player_and_prev.append(Y[idx])
            Y_player_and_prev.append(Y[idx-1])

    clf = get_model(X_TRAIN, Y_TRAIN)
    return (clf, X_player_and_prev, Y_player_and_prev)


def get_player_play_scores(player):
    df = pd.read_csv(base_path() + '/data/test_data.csv')
    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST = split_into_test_train(df)
    X = pd.concat([X_TRAIN, X_TEST])
    clf, X_player_and_prev, Y_TEST = train_against_other_players(df, X, (Y_TRAIN + Y_TEST), player)
    percents = clf.predict_proba(X_player_and_prev)[:, 1]
    scores = []
    for idx in range(int(len(percents)/2)):
        if abs(percents[2*idx] - percents[2*idx+1]) > 0.5:
            prev_score = 1 - percents[2*idx+1]
        else:
            prev_score = percents[2*idx+1]
        scores.append([percents[2*idx] - prev_score])
    return scores


print(get_player_play_scores('Luka Doncic'))