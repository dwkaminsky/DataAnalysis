import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt


def process_df_for_nn(df_unprocessed):
    df_unprocessed['Processed_Time'] = 0
    df_unprocessed['Processed_Score'] = 0
    df_unprocessed['Processed_Distance'] = 0
    for shot_index in range(len(df_unprocessed)):
        score = df_unprocessed.loc[shot_index, 'Score'].split()
        _time = df_unprocessed.loc[shot_index, 'Time'].split(':')
        if len(_time) == 1:
            df_unprocessed.loc[shot_index, 'Processed_Time'] = float(_time[0])
        elif len(_time) == 2:
            df_unprocessed.loc[shot_index, 'Processed_Time'] = int(_time[0]) * 60 + int(_time[1])
        else:
            print('Invalid Time at ', shot_index)
        df_unprocessed.loc[shot_index, 'Processed_Distance'] = np.ceil(
            df_unprocessed.loc[shot_index, 'Distance']) / 5
        if df_unprocessed.loc[shot_index, 'Home?'] == 1:
            df_unprocessed.loc[shot_index, 'Processed_Score'] = np.floor(
                (int(score[2]) - int(score[0])) / 3)
        else:
            df_unprocessed.loc[shot_index, 'Processed_Score'] = np.floor(
                (int(score[0]) - int(score[2])) / 3)
    return df_unprocessed


def get_nn_data_from_processed_df(df_processed):
    X_TRAIN = []
    Y_TRAIN = []
    X_TEST = []
    Y_TEST = []
    for shot_index in range(len(df_processed)):
        sample_x = [df_processed.loc[shot_index, 'Distance'],
                    df_processed.loc[shot_index, 'Points'],
                    df_processed.loc[shot_index, 'Processed_Time'],
                    df_processed.loc[shot_index, 'Quarter'],
                    df_processed.loc[shot_index, 'Home?'],
                    df_processed.loc[shot_index, 'Processed_Score'], ]
        sample_y = df_processed.loc[shot_index, 'Made?']
        if shot_index < len(df_processed) * 0.7:
            X_TRAIN.append(sample_x)
            Y_TRAIN.append(sample_y)
        else:
            X_TEST.append(sample_x)
            Y_TEST.append(sample_y)
    return X_TRAIN, X_TEST, Y_TRAIN, Y_TEST


def run_neural_net(X_TRAIN, X_TEST, Y_TRAIN, Y_TEST):
    scaler = StandardScaler()
    scaler.fit(X_TRAIN)
    X_TRAIN = scaler.transform(X_TRAIN)
    X_TEST = scaler.transform(X_TEST)
    prediction_average = 0
    for random_state in range(5):
        clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                            hidden_layer_sizes=(5,), random_state=1)
        clf = clf.fit(X_TRAIN, Y_TRAIN)
        prediction = clf.predict_proba(X_TEST)
        if random_state == 0:
            prediction_average = np.mean(prediction)
        else:
            prediction_average = prediction_average + np.mean(prediction)
    prediction_average = prediction_average / 5
    return prediction_average, Y_TEST


def run_SVC():
    df_19_20_unprocessed = pd.read_csv(
        'C:/Users/DannyDell/Documents/NBADataProject/data/2019-20_mavs_shot_data.csv')
    df_18_19 = pd.read_csv(
        'C:/Users/DannyDell/Documents/NBADataProject/data/2018-19_mavs_shot_data-nn.csv')
    df_19_20 = pd.read_csv(
        'C:/Users/DannyDell/Documents/NBADataProject/data/2019-20_mavs_shot_data-nn.csv')
    X_TRAIN0, X_TEST0, Y_TRAIN0, Y_TEST0 = get_nn_data_from_processed_df(df_18_19)
    X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = get_nn_data_from_processed_df(df_19_20)
    X_TEST = X_TRAIN + X_TEST
    Y_TEST = Y_TRAIN + Y_TEST
    X_TRAIN = X_TRAIN0 + X_TEST0
    Y_TRAIN = Y_TRAIN0 + Y_TEST0
    clf = LinearSVC(random_state=0, tol=1e-5)
    clf.fit(X_TRAIN, Y_TRAIN)
    diff = abs(clf.decision_function(X_TEST)-Y_TEST)
    print(np.mean(diff))
    print(clf.decision_function(X_TEST))


def main():
    df_19_20_unprocessed = pd.read_csv(
        'C:/Users/DannyDell/Documents/DataAnalysis/data/2019-20_mavs_shot_data.csv')
    df_18_19 = pd.read_csv(
        'C:/Users/DannyDell/Documents/DataAnalysis/data/2018-19_mavs_shot_data-nn.csv')
    df_19_20 = pd.read_csv(
        'C:/Users/DannyDell/Documents/DataAnalysis/data/2019-20_mavs_shot_data-nn.csv')
    X_TRAIN0, X_TEST0, Y_TRAIN0, Y_TEST0 = get_nn_data_from_processed_df(df_18_19)
    X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = get_nn_data_from_processed_df(df_19_20)
    X_TEST = X_TRAIN + X_TEST
    Y_TEST = Y_TRAIN + Y_TEST
    X_TRAIN = X_TRAIN0 + X_TEST0
    Y_TRAIN = Y_TRAIN0 + Y_TEST0
    prediction, actual = run_neural_net(X_TRAIN, X_TEST, Y_TRAIN, Y_TEST)
    prediction = prediction[:, 1]
    df_19_20_unprocessed['Make_Probability'] = prediction
    df_19_20_unprocessed = df_19_20_unprocessed.drop(columns=['Unnamed: 0'])
    df_Luka = df_19_20_unprocessed[df_19_20_unprocessed['Player'] == 'Luka Doncic']
    df_Luka_late_close = pd.DataFrame(columns=df_Luka.columns)
    for i, row in df_Luka.iterrows():
        if abs(int(row['Score'].split()[2]) - int(row['Score'].split()[0])) < 6:
            if len(row['Time'].split(':')) == 2 and int(row['Time'].split(':')[0]) < 5:
                df_Luka_late_close = df_Luka_late_close.append(row)
            elif len(row['Time'].split(':')) == 1:
                df_Luka_late_close = df_Luka_late_close.append(row)
    df_Luka_late_close = df_Luka_late_close[df_Luka_late_close['Quarter'] == 4]
    fig, ax = plt.subplots()
    for idx, color in enumerate(['tab:red', 'tab:green']):
        x = df_Luka_late_close[df_Luka_late_close['Made?'] == idx]['Distance']
        y = df_Luka_late_close[df_Luka_late_close['Made?'] == idx]['Make_Probability']
        ax.scatter(x, y, c=color, label=color,
                   alpha=0.3, edgecolors='none')

    ax.legend()
    ax.grid(True)

    plt.show()


# main()

