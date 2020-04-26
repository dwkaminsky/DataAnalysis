import pandas as pd
import numpy as np
from test_class_algos.fetch_data import get_clean_game_data
from config import base_path
from neural_net_game_pressure import run_neural_net
idx = 1013


def get_player_score(player_name, team_name, cutoff_time, cutoff_score):
    train_df = pd.DataFrame()
    for team in ['Hawks', 'Knicks', 'Nets', 'Celtics', 'Bucks', 'Heat', 'Warriors', 'Pacers',
                 'Mavericks', 'Wizards', 'Bulls', 'Raptors', 'Magic', 'Thunder', 'Pelicans',
                 'Trail Blazers', 'Grizzlies', 'Pistons', '76ers', 'Hornets', 'Cavaliers', 'Suns',
                 'Jazz', 'Nuggets', 'Lakers', 'Rockets', 'Timberwolves', 'Spurs', 'Clippers',
                 'Kings']:
        team_df = pd.read_csv(base_path() + f'/data/team_dfs/{team}.csv').drop(columns=[
            'Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'Team', 'Opponent', 'Secondary Player'])
        team_df['Jumper?'] = team_df['Shot Type'] == 'Jumper'
        team_df['Distance'] = pd.to_numeric(team_df['Distance'], errors='coerce')
        team_df = team_df.drop(columns=['Shot Type', 'Won?']).dropna(axis=0)
        if team != team_name:
            train_df = pd.concat([train_df, team_df])
        else:
            focus_team_df = team_df
    focus_player_df = focus_team_df[focus_team_df['Player'] == player_name]
    focus_player_df = focus_player_df[focus_player_df['Score'] <= cutoff_score]
    focus_player_df = focus_player_df[focus_player_df['Score'] >= (-1 * cutoff_score)]
    focus_player_df = focus_player_df[focus_player_df['Clock'] <= cutoff_time]
    X_TEST = focus_player_df[['Home?', 'Distance', 'Points', 'Jumper?']]
    X_TRAIN = train_df[['Home?', 'Distance', 'Points', 'Jumper?']]
    Y_TEST = focus_player_df['Made?']
    Y_TRAIN = train_df['Made?']
    prediction_average, Y_TEST = run_neural_net(X_TRAIN, X_TEST, Y_TRAIN, Y_TEST)
    return Y_TEST, prediction_average


# For Luka Doncic, when he was playing for the Mavericks, analyze plays with <=300 seconds with
# the game within 5 points
actual_makes, predicted_makes = get_player_score('Luka Doncic', 'Mavericks', 300, 5)
print(actual_makes)
print(predicted_makes)
