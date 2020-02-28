import pandas as pd
import numpy as np
from config import base_path
from ESPN_GAME_DATA_RETRIEVAL.ESPN_GAME_DATA_PARSER import play_types
import os


def get_clean_game_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df = df.drop(columns=['Unnamed: 0'])
        df['Won?'] = 1
        if int(df.loc[len(df) - 1, 'Score'].split()[0]) > int(df.loc[len(df) - 1, 'Score'].split()[2]):
            homeWon = False
        else:
            homeWon = True
        for idx in range(len(df)):
            if not homeWon and df.loc[idx, 'Home?']:
                df.loc[idx, 'Won?'] = 0
            elif homeWon and not df.loc[idx, 'Home?']:
                df.loc[idx, 'Won?'] = 0
        df = df[df['Play Type'] != 'Unknown']
        for play_type in play_types:
            df[play_type] = df['Play Type'] == play_type
        df = df.drop(columns=['Play Type'])
        df = df.reset_index()
        for idx in range(len(df)):
            if df.loc[idx, 'Home?'] == 1:
                df.loc[idx, 'Score'] = int(df.loc[idx, 'Score'].split()[2]) - \
                                   int(df.loc[idx, 'Score'].split()[0])
            else:
                df.loc[idx, 'Score'] = int(df.loc[idx, 'Score'].split()[0]) - \
                                   int(df.loc[idx, 'Score'].split()[2])
            if len(df.loc[idx, 'Clock'].split(':')) != 2:
                df.loc[idx, 'Clock'] = float(df.loc[idx, 'Clock'])
            else:
                df.loc[idx, 'Clock'] = 60 * float(df.loc[idx, 'Clock'].split(':')[0]) + \
                                   float(df.loc[idx, 'Clock'].split(':')[1])
        return df
    except:
        return pd.DataFrame(columns=play_types)


def get_test_df():
    df = get_year_team_df(2019, 'BOS')
    df = add_prev_play_counts_to_df(get_clean_game_data(df))
    return df


def get_year_team_df(year, team):
    df_list = []
    for file in os.listdir(base_path()+'/data/2019'):
        print(file)
        try:
            df_list.append(add_prev_play_counts_to_df(get_clean_game_data(base_path()+'/data/2019/'
                                                                      + file)))
        except:
            print('File not found')
    df = pd.concat(df_list)
    df = df.drop(columns=['index'])
    df = df.reset_index()
    return df


def add_prev_play_counts_to_df(df):
    for play_type in play_types:
        df['PREV_TEAM_' + play_type] = 0
        df['PREV_OPP_' + play_type] = 0
    for idx_row in range(len(df)):
        prev_df = df[df['index'] < idx_row]
        if df.loc[idx_row, 'Home?'] == 1:
            team_prev_df = prev_df[prev_df['Home?'] == 1]
            opp_prev_df = prev_df[prev_df['Home?'] == 0]
        else:
            team_prev_df = prev_df[prev_df['Home?'] == 0]
            opp_prev_df = prev_df[prev_df['Home?'] == 1]
        for play_type in play_types:
            df.loc[idx_row, 'PREV_TEAM_' + play_type] = np.sum(team_prev_df[play_type])
            df.loc[idx_row, 'PREV_OPP_' + play_type] = np.sum(opp_prev_df[play_type])
    return df


def split_into_test_train(df):
    Y = df['Won?']
    X = df.drop(columns=['Won?'])
    X_TEST = pd.DataFrame(columns=X.columns)
    X_TRAIN = pd.DataFrame(columns=X.columns)
    Y_TEST = []
    Y_TRAIN = []
    for row_idx in range(len(df)):
        if np.random.rand() < 0.7:
            X_TRAIN = X_TRAIN.append(X.iloc[row_idx])
            Y_TRAIN.append(Y.iloc[row_idx])
        else:
            X_TEST = X_TEST.append(X.iloc[row_idx])
            Y_TEST.append(Y.iloc[row_idx])
    return X_TRAIN, Y_TRAIN, X_TEST, Y_TEST


split_into_test_train(add_prev_play_counts_to_df(get_test_df()))
