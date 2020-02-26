import pandas as pd
import numpy as np
from config import base_path
from ESPN_GAME_DATA_RETRIEVAL.ESPN_GAME_DATA_PARSER import play_types


def get_clean_game_data(file_path):
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


def get_test_df():
    return get_clean_game_data(base_path() + '/data/detailed_game_data/2019/OKC_game0.csv')


def get_year_team_df(year, team):
    df_list = []
    for i in range(21):
        df_list.append(add_prev_play_counts_to_df(get_clean_game_data(base_path() + '/data/detailed_game_data/' + str(year)
                                           + '/' + str(team) + '_game0.csv')))
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


print(add_prev_play_counts_to_df(get_test_df()))
