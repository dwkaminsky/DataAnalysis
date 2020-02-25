import time

import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import *

mavs_roster_19_20 = ['Dorian Finney-Smith', 'Luka Doncic', 'Tim Hardaway', 'Maxi Kleber',
                     'Kristaps Porzingis', 'Seth Curry', 'Delon Wright', 'Dwight Powell',
                     'Jalen Brunson',
                     'Justin Jackson', 'J.J. Barea', 'Boban Marjanovic', 'Ryan Broekhoff',
                     'Courtney Lee',
                     'Willie Cauley-Stein', 'Antonius Cleveland', 'Michael Kidd-Gilchrist',
                     'Josh Reaves']

mavs_roster_18_19 = ['Kostas Antetokounmpo', 'J.J. Barea', 'Harrison Barnes', 'Ryan Broekhoff',
                     'Jalen Brunson', 'Trey Burke', 'Luka Doncic', 'Dorian Finney-Smith',
                     'Tim Hardaway', 'Devin Harris', 'Justin Jackson', 'DeAndre Jordan',
                     'Maxi Kleber', 'Courtney Lee', 'Daryl Macon', 'Wesley Matthews', 'Salah Mejri',
                     'Dirk Nowitzki', 'Dwight Powell', 'Dennis Smith', 'Ray Spalding']

mavs_game_links_2020 = ['https://www.espn.com/nba/game?gameId=401161468',
                        'https://www.espn.com/nba/game?gameId=401161456',
                        'https://www.espn.com/nba/game?gameId=401161440',
                        'https://www.espn.com/nba/game?gameId=401161420',
                        'https://www.espn.com/nba/game?gameId=401161412',  # @Wiz
                        'https://www.espn.com/nba/game?gameId=401161403',
                        'https://www.espn.com/nba/game?gameId=401161385',
                        'https://www.espn.com/nba/game?gameId=401161375',
                        'https://www.espn.com/nba/game?gameId=401161364',
                        'http://www.espn.com/nba/game?gameId=401161348',  # vs Suns
                        'http://www.espn.com/nba/game?gameId=401161339',
                        'http://www.espn.com/nba/game?gameId=401161322',
                        'http://www.espn.com/nba/game?gameId=401161310',
                        'http://www.espn.com/nba/game?gameId=401161295',
                        'http://www.espn.com/nba/game?gameId=401161267',
                        'http://www.espn.com/nba/game?gameId=401161254',
                        'http://www.espn.com/nba/game?gameId=401161244',
                        'http://www.espn.com/nba/game?gameId=401161223',
                        'http://www.espn.com/nba/game?gameId=401161214',
                        'http://www.espn.com/nba/game?gameId=401161201',  # vs DEN
                        'http://www.espn.com/nba/game?gameId=401161187',
                        'http://www.espn.com/nba/game?gameId=401161172',
                        'http://www.espn.com/nba/game?gameId=401161155',
                        'http://www.espn.com/nba/game?gameId=401161155',
                        'http://www.espn.com/nba/game?gameId=401161132',
                        'http://www.espn.com/nba/game?gameId=401161124',
                        'http://www.espn.com/nba/game?gameId=401161105',  # vs SA
                        'http://www.espn.com/nba/game?gameId=401161081',
                        'http://www.espn.com/nba/game?gameId=401161067',
                        'http://www.espn.com/nba/game?gameId=401161067',
                        'http://www.espn.com/nba/game?gameId=401161040',
                        'http://www.espn.com/nba/game?gameId=401161026',  # vs MIA
                        'http://www.espn.com/nba/game?gameId=401161011',
                        'http://www.espn.com/nba/game?gameId=401160982',
                        'http://www.espn.com/nba/game?gameId=401160972',
                        'http://www.espn.com/nba/game?gameId=401160955',
                        'http://www.espn.com/nba/game?gameId=401160944',
                        'http://www.espn.com/nba/game?gameId=401160929',
                        'http://www.espn.com/nba/game?gameId=401160919',  # @PHX
                        'http://www.espn.com/nba/game?gameId=401160893',
                        'http://www.espn.com/nba/game?gameId=401160877',
                        'http://www.espn.com/nba/game?gameId=401160863',
                        'http://www.espn.com/nba/game?gameId=401160863',
                        'http://www.espn.com/nba/game?gameId=401160850',  # vs GS
                        'http://www.espn.com/nba/game?gameId=401160836',
                        'http://www.espn.com/nba/game?gameId=401160822',
                        'http://www.espn.com/nba/game?gameId=401160804',
                        'http://www.espn.com/nba/game?gameId=401160783',
                        'http://www.espn.com/nba/game?gameId=401160772',
                        'http://www.espn.com/nba/game?gameId=401160764',
                        'http://www.espn.com/nba/game?gameId=401160751',  # vs ORL
                        'http://www.espn.com/nba/game?gameId=401160731',
                        'http://www.espn.com/nba/game?gameId=401160716',
                        'http://www.espn.com/nba/game?gameId=401160695',
                        'http://www.espn.com/nba/game?gameId=401160680',
                        'http://www.espn.com/nba/game?gameId=401160663',
                        'http://www.espn.com/nba/game?gameId=401160631',
                        ]

# Play Types
play_FG_UNASSISTED = 'FG_UNASSISTED'
play_FG_ASSISTED = 'FG_ASSISTED'
play_FG_MISS = 'FG_MISS'
play_FT = 'FT'
play_FT_MISS = 'FT_MISS'
play_TURNOVER = 'TURNOVER'
play_FOUL_ON_FLOOR = 'FOUL_ON_FLOOR'
play_FOUL_SHOOTING = 'FOUL_SHOOTING'
play_FOUL_TECHNICAL = 'FOUL_TECHNICAL'
play_FOUL_FLAGRANT_1 = 'FOUL_FLAGRANT_1'
play_FOUL_FLAGRANT_2 = 'FOUL_FLAGRANT_2'
play_DEF_3_SECONDS = 'DEF_3_SECONDS'
play_OFFENSIVE_REBOUND = 'OFFENSIVE_REBOUND'
play_DEFENSIVE_REBOUND = 'DEFENSIVE_REBOUND'
play_SUBSTITUTION = 'SUBSTITUTION'
play_JUMP_BALL = 'JUMP_BALL'
play_TIMEOUT = 'TIMEOUT'

play_types = {play_FG_UNASSISTED, play_FG_ASSISTED, play_FG_MISS, play_FT, play_FT_MISS,
              play_TURNOVER, play_FOUL_ON_FLOOR, play_FOUL_SHOOTING, play_FOUL_TECHNICAL,
              play_FOUL_FLAGRANT_1, play_FOUL_FLAGRANT_2, play_DEF_3_SECONDS,
              play_OFFENSIVE_REBOUND, play_DEFENSIVE_REBOUND, play_SUBSTITUTION, play_JUMP_BALL,
              play_TIMEOUT}

fg_play_types = {play_FG_UNASSISTED, play_FG_ASSISTED, play_FG_MISS}

secondary_player_play_types = {
    play_FG_ASSISTED, play_SUBSTITUTION, play_TURNOVER, play_FG_MISS
}

turnover_words = {'traveling', 'bad pass', 'steal', 'lost ball',
                  'turnover', 'charge', 'shot clock'}

# Play Attributes (DF Columns)
PLAYER = 'Player'
PLAYER_2 = 'Secondary Player'
CLOCK = 'Clock'
QUARTER = 'Quarter'
TEAM = 'Team'
OPPONENT = 'Opponent'
SCORE = 'Score'
DISTANCE = 'Distance'
POINTS = 'Points'
PLAY_TYPE = 'Play Type'
SHOT_TYPE = 'Shot Type'
HOME = 'Home?'

play_attributes = [PLAYER, PLAY_TYPE, PLAYER_2, CLOCK, QUARTER, TEAM, OPPONENT, SCORE, HOME,
                   DISTANCE, POINTS, SHOT_TYPE]

# Shot Types
SHOT_TYPE_DUNK = 'Dunk'
SHOT_TYPE_LAYUP = 'Layup'
SHOT_TYPE_JUMPER = 'Jumper'

shot_types = {SHOT_TYPE_DUNK, SHOT_TYPE_JUMPER, SHOT_TYPE_LAYUP}


def parseLine(line):
    word_list = line.split()
    timestamp = word_list[0]
    player_name = word_list[1] + ' ' + word_list[2]
    distance = 0
    points = 0
    turnover_first_words = ['bad', 'loses']
    if word_list[3] == 'offensive':
        play_type = 'OREB'
    elif word_list[3] == 'defensive':
        play_type = 'DREB'
    elif word_list[3] == 'misses':
        if word_list[4] == 'free':
            play_type = 'FTMISS'
        else:
            play_type = 'FGMISS'
            if word_list[5] == 'three':
                points = 3
            else:
                points = 2
            try:
                distance = int(word_list[4].split('-')[0])
            except:
                distance = 0
    elif word_list[3] == 'makes':
        if word_list[4] == 'free':
            play_type = 'FTMAKE'
        else:
            play_type = 'FGMAKE'
            if word_list[5] == 'three':
                points = 3
            else:
                points = 2
            try:
                distance = int(word_list[4].split('-')[0])
            except:
                distance = 0
    elif word_list[3] in turnover_first_words:
        play_type = 'TURN'
    elif word_list[-4] in ['foul', 'foul)']:
        if word_list[-5] in ['technical foul', '(technical']:
            play_type = 'TFOUL'
        else:
            play_type = 'FOUL'
    elif word_list[3] == 'defensive':
        play_type = 'DREB'
    else:
        play_type = 'NONE'
    net_score = int(word_list[-1]) - int(word_list[-3])
    play = {
        'timestamp': timestamp,
        'player_name': player_name,
        'play_type': play_type,
        'score': word_list[-1] + ' - ' + word_list[-3],
        'net_score': net_score,
    }
    if play_type == 'FGMAKE':
        if word_list[-4] == 'assists)':
            play['assister'] = word_list[-6][1:] + ' ' + word_list[-5]
    if play_type in ['FGMAKE', 'FGMISS']:
        play['distance'] = distance
        play['points'] = points
    return play


def parseQuarter(quarter, url, browser):
    xpath = '//*[@id="gp-quarter-' + str(quarter) + '"]/table/tbody'
    quarter_table = browser.find_element_by_xpath(xpath)
    line_list = []
    for row in quarter_table.find_elements_by_xpath(".//tr"):
        line_list.append([row.text,
                          row.find_element_by_class_name('team-logo').get_attribute('src')])
    return line_list


def getQuarterFieldGoalDF(quarter, url, browser):
    parsed_quarter = parseQuarter(quarter, url, browser)
    df = pd.DataFrame(
        columns=['Player', 'Made?', 'Distance', 'Points', 'Time', 'Score', 'Assister'])
    fg_index = -1
    for play in parsed_quarter:
        if play['play_type'] in ['FGMAKE', 'FGMISS']:
            fg_index = fg_index + 1
            if play['play_type'] == 'FGMAKE':
                made = 1
            else:
                made = 0
            try:
                assister = play['assister']
            except KeyError:
                assister = 'None'
            play_as_list = [play['player_name'], made, play['distance'], play['points'],
                            play['timestamp'], play['score'], assister]
            df.loc[fg_index] = play_as_list
    df['Quarter'] = quarter
    return df


def get_detailed_df_from_line_list(line_list, home_img, away_img, quarter, home_team, away_team):
    df = pd.DataFrame(columns=play_attributes)
    for idx_line, line in enumerate(line_list):
        home = 0
        team = home_team
        opponent = away_team
        try:
            if home_img == line[1]:
                home = 1
                team = home_team
                opponent = away_team
            else:
                home = 0
                team = away_team
                opponent = away_team
        except:
            if away_img == line[1]:
                home = 0
                team = away_team
                opponent = away_team
        else:
            home = 1
            team = home_team
            opponent = away_team
        line = line[0].replace(' Jr. ', ' ')
        split_line = line.split()
        name = split_line[1] + ' ' + split_line[2]
        time = split_line[0]
        score = split_line[-3] + ' - ' + split_line[-1]
        play_type = 'Unknown'
        if 'foul' in line:
            if 'technical' in line:
                play_type = play_FOUL_TECHNICAL
            elif 'flagrant foul type 1' in line:
                play_type = play_FOUL_FLAGRANT_1
            elif 'flagrant foul type 2' in line:
                play_type = play_FOUL_FLAGRANT_2
            elif 'defensive 3-seconds' in line:
                play_type = play_DEF_3_SECONDS
            elif 'free throw' in line_list[idx_line + 1]:
                play_type = play_FOUL_SHOOTING
            else:
                play_type = play_FOUL_ON_FLOOR
        elif 'enters the game' in line:
            play_type = play_SUBSTITUTION
        elif 'vs.' in line:
            play_type = play_JUMP_BALL
        elif 'makes' in line:
            if 'free throw' in line:
                play_type = play_FT
            else:
                if 'assist' in line:
                    play_type = play_FG_ASSISTED
                else:
                    play_type = play_FG_UNASSISTED
        elif 'miss' in line:
            if 'free throw' in line:
                play_type = play_FT_MISS
            else:
                play_type = play_FG_MISS
        elif 'block' in line:
            play_type = play_FG_MISS
        elif 'rebound' in line:
            if 'offensive' in line:
                play_type = play_OFFENSIVE_REBOUND
            else:
                play_type = play_DEFENSIVE_REBOUND
        else:
            turnover_bool = False
            for turnover_word in turnover_words:
                if turnover_word in line:
                    turnover_bool = True
                    break
            if turnover_bool:
                play_type = play_TURNOVER
        if play_type in fg_play_types:
            distance = '0'
            points = '2'
            if 'layup' in line:
                shot_type = SHOT_TYPE_LAYUP
            elif 'dunk' in line:
                shot_type = SHOT_TYPE_DUNK
            else:
                shot_type = SHOT_TYPE_JUMPER
                if line[line.find('foot') - 3:line.find('foot') - 1].isnumeric():
                    distance = line[line.find('foot') - 3:line.find('foot') - 1]
                else:
                    distance = line[line.find('foot') - 2]
                if line[line.find(' point ') - 3:line.find(' point ') - 1] != 'two':
                    points = '3'
        else:
            distance = 'N/A'
            if play_type in [play_FT, play_FT_MISS]:
                points = '1'
            else:
                points = 'N/A'
            shot_type = 'N/A'
        df = df.append({
            PLAYER: name,
            CLOCK: time,
            HOME: home,
            QUARTER: quarter,
            PLAY_TYPE: play_type,
            TEAM: team,
            OPPONENT: opponent,
            SCORE: score,
            DISTANCE: distance,
            POINTS: points,
            SHOT_TYPE: shot_type
        }, ignore_index=True)
    return df


def get_game_DF_detailed(url):
    browser = webdriver.Chrome()
    browser.get(url)
    quarter_2 = browser.find_element_by_css_selector(
        '#gamepackage-qtrs-wrap > ul > li:nth-child(2) > div.accordion-header > a')
    quarter_2.click()
    time.sleep(0.5 + np.random.rand() * 2)
    quarter_3 = browser.find_element_by_css_selector(
        '#gamepackage-qtrs-wrap > ul > li:nth-child(3) > div.accordion-header > a')
    quarter_3.click()
    time.sleep(0.5 + np.random.rand() * 2)
    quarter_4 = browser.find_element_by_css_selector(
        '#gamepackage-qtrs-wrap > ul > li:nth-child(4) > div.accordion-header > a')
    quarter_4.click()
    time.sleep(1 * np.random.rand())
    home_img = browser.find_element_by_xpath('//*[@id="gamepackage-matchup-wrap"]/'
                                             'header/div/div[3]/div/div[3]/'
                                             'div[1]/div/a/img').get_attribute('src')
    away_img = browser.find_element_by_xpath('//*[@id="gamepackage-matchup-wrap"]/header/div/div['
                                             '1]/ '
                                             'div/div[2]/div[2]/div/a/img').get_attribute('src')
    home = browser.find_element_by_xpath('//*[@id="gamepackage-matchup-wrap"]/header/div/div[3]'
                                         '/div/div[3]/div[2]/div[1]/a/span[2]').text
    away = browser.find_element_by_xpath('//*[@id="gamepackage-matchup-wrap"]/header/div/div[1]'
                                         '/div/div[2]/div[1]/div[1]/a/span[2]').text
    quarter_1_line_list = parseQuarter(1, url, browser)
    quarter_2_line_list = parseQuarter(2, url, browser)
    quarter_3_line_list = parseQuarter(3, url, browser)
    quarter_4_line_list = parseQuarter(4, url, browser)
    df_quarter_1 = get_detailed_df_from_line_list(quarter_1_line_list, home_img, away_img, 1, home,
                                                  away)
    df_quarter_2 = get_detailed_df_from_line_list(quarter_2_line_list, home_img, away_img, 2,
                                                  home, away)
    df_quarter_3 = get_detailed_df_from_line_list(quarter_3_line_list, home_img, away_img, 3,
                                                  home, away)
    df_quarter_4 = get_detailed_df_from_line_list(quarter_4_line_list, home_img, away_img, 4,
                                                  home, away)
    df_game = pd.concat([df_quarter_1, df_quarter_2, df_quarter_3, df_quarter_4])
    browser.close()
    return df_game


def getGameFieldGoalDF(url):
    browser = webdriver.Chrome()
    browser.get(url)
    quarter_2 = browser.find_element_by_css_selector(
        '#gamepackage-qtrs-wrap > ul > li:nth-child(2) > div.accordion-header > a')
    quarter_2.click()
    time.sleep(1)
    quarter_3 = browser.find_element_by_css_selector(
        '#gamepackage-qtrs-wrap > ul > li:nth-child(3) > div.accordion-header > a')
    quarter_3.click()
    time.sleep(1)
    quarter_4 = browser.find_element_by_css_selector(
        '#gamepackage-qtrs-wrap > ul > li:nth-child(4) > div.accordion-header > a')
    quarter_4.click()
    df = getQuarterFieldGoalDF(1, url, browser)
    df = pd.concat([df, getQuarterFieldGoalDF(2, url, browser)])
    df = pd.concat([df, getQuarterFieldGoalDF(3, url, browser)])
    df = pd.concat([df, getQuarterFieldGoalDF(4, url, browser)])
    browser.close()
    return df


def getFGDFFromGameLinks(game_links):
    df = pd.DataFrame
    for game_index, game_link in enumerate(game_links):
        play_by_play_link = game_link[:-21] + 'playbyplay' + game_link[-17:]
        if game_index == 0:
            df = getGameFieldGoalDF(play_by_play_link)
        else:
            new_df = getGameFieldGoalDF(play_by_play_link)
            df = pd.concat([df, new_df])
    return df


def add_team_home_to_df(df, roster):
    df['TOI Home?'] = 0
    last_shot_of_game_indeces = [0]
    for idx_row in range(len(df) - 1):
        try:
            if df.loc[idx_row, 'Quarter'] > df.loc[idx_row + 1, 'Quarter']:
                last_shot_of_game_indeces.append(idx_row)
        except ValueError:
            print('ValueError: these should be ints')
            print(df.loc[idx_row, 'Quarter'])
            print(df.loc[idx_row + 1, 'Quarter'])

    for idx_game in range(len(last_shot_of_game_indeces) - 1):
        game_not_finished = True
        idx_row = last_shot_of_game_indeces[idx_game] + 10
        while game_not_finished:
            if df.loc[idx_row, 'Made?'] == 1 and df.loc[idx_row, 'Player'] in roster:
                if int(df.loc[idx_row, 'Score'].split()[2]) > \
                        int(df.loc[idx_row - 1, 'Score'].split()[2]):
                    team_home = True
                    game_not_finished = False
                else:
                    team_home = False
                    game_not_finished = False
            idx_row = idx_row + 1
        try:
            if team_home:
                df.loc[last_shot_of_game_indeces[idx_game]:last_shot_of_game_indeces[idx_game + 1],
                'TOI Home?'] = 1
            else:
                df.loc[last_shot_of_game_indeces[idx_game]:last_shot_of_game_indeces[idx_game + 1],
                'TOI Home?'] = 0
        except IndexError:
            print('Error')
    df['Home?'] = df['TOI Home?']
    for shot_index in range(len(df)):
        if df.loc[shot_index, 'Player'] not in roster:
            df.loc[shot_index, 'Player'] = 1 - df.loc[shot_index, 'Player']
    df = df.drop(columns=['TOI Home?'])
    return df


def saveFGDF(link_list, path, roster):
    times_to_finish = []
    for link_index, link in enumerate(link_list):
        start_time = time.time()
        try:
            df = pd.read_csv(path)
            new_df = getFGDFFromGameLinks([link])
            df = pd.concat([df, new_df])
        except FileNotFoundError:
            df = getFGDFFromGameLinks([link])
        time_to_finish = time.time() - start_time
        times_to_finish.append(time_to_finish)
        print('Game ' + str(link_index) + ' took ' + str(time_to_finish) + ' seconds')
        time_remaining = (len(link_list) - link_index) * np.mean(times_to_finish)
        print('Time Remaining :' + str(np.floor(time_remaining / 60)) + 'm ' +
              str(np.floor(time_remaining) - np.floor(time_remaining / 60) * 60) + 's')
        df.to_csv(path)
    df = add_team_home_to_df(df, roster)
    df.to_csv(path)


def get_nba_rosters_and_ESPN_links(year):
    df = pd.read_csv('C:/Users/DannyDell/Documents/NBADataProject/data/2018-19nba_rosters.csv')
    team_list = list(set(df['Team']))
    rosters = dict()
    link_list = []
    for team in team_list:
        rosters[team] = df[df['Team'] == team]
    for team in rosters.keys():
        rosters[team] = rosters[team]['First'] + ' ' + rosters[team]['Last']
        rosters[team] = list(rosters[team])
        link_list.append([team, 'https://www.espn.com/nba/team/schedule?name=' + team +
                          '&season=' + str(year)])
    return rosters, link_list


def get_link_list_from_ESPN_link(espn_link):
    driver = webdriver.Chrome()
    driver.get(espn_link)
    select_season = Select(driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]'
                                                        '/div[1]/div/section/div/section/div[2]/div[2]'
                                                        '/select[1]'))
    select_season.select_by_visible_text('Regular Season')
    time.sleep(3)
    link_list = []
    for i in range(82):
        try:
            xpath = '//*[@id="fittPageContainer"]/div[2]/div[5]/div[1]/div/section/div/section/section' \
                    '/section/div/div/div[2]/table/tbody/tr[' + str(i + 2) + ']/td[3]/span[2]/a'
            link_list.append(driver.find_element_by_xpath(xpath).get_attribute('href'))
        except:
            xpath = '//*[@id="fittPageContainer"]/div[2]/div[5]/div[1]/div/section/div/section/section/section/' \
                    'div/div/div[2]/table/tbody/tr[' + str(i + 2) + ']/td[3]/span[2]/a'
            link_list.append(driver.find_element_by_xpath(xpath).get_attribute('href'))
    return link_list


def scrape_data():
    rosters, espn_link_list = get_nba_rosters_and_ESPN_links(2019)
    espn_links = []
    teams = []
    for idx_team in range(30):
        espn_links.append(espn_link_list[idx_team][1])
        teams.append(espn_link_list[idx_team][0])
    for team in teams:
        roster_list = []
        roster = rosters[team]
        for player_name in roster:
            if type(player_name) is type('string'):
                if player_name[0] == ' ':
                    player_name = player_name[1:]
                roster_list.append(player_name)
        rosters[team] = roster_list
    teams.remove('MIN')
    teams.remove('WAS')
    print(teams)
    for idx_team, team in enumerate(teams):
        link_list = get_link_list_from_ESPN_link(espn_links[idx_team])
        path = 'C:/Users/DannyDell/Documents/NBADataProject/data/2018-19_' + team + '_shot_data.csv'
        roster = rosters[team]
        saveFGDF(link_list, path, roster)


def main():
    browser = webdriver.Chrome()
    browser.get('https://www.espn.com/nba/team/schedule?name=DAL&season=2019')
    link_list = []
    for game_index in range(2, 84):
        xpath = '//*[@id="fittPageContainer"]/div[2]/div[5]/div[1]/div/section/div/section/section' \
                '/section/div/div/div[2]/table/tbody/tr[' + str(game_index) + ']/td[3]/span[2]/a'
        link = browser.find_element_by_xpath(xpath).get_attribute('href')
        link_list.append(link)
    browser.close()
    saveFGDF(link_list, 'C:/Users/DannyDell/Documents/NBADataProject/data/2018-19_mavs_shot_data'
                        '.csv')

line = ['11:65 Devin Booker Jr. 6-foot three point pullup jump shot 27 - 25',' ']
home_team = 'Mavericks'
away_team = 'Suns'
home_img = ' '
away_img = 'false'
home = 0
team = home_team
opponent = away_team
df = pd.DataFrame(columns=play_attributes)
idx_line = 0
try:
    if home_img == line[1]:
        home = 1
        team = home_team
        opponent = away_team
    else:
        home = 0
        team = away_team
        opponent = away_team
except:
    if away_img == line[1]:
        home = 0
        team = away_team
        opponent = away_team
    else:
        home = 1
        team = home_team
        opponent = away_team
line = line[0].replace(' Jr. ', ' ')
line_list = []
quarter = 1
split_line = line.split()
name = split_line[1] + ' ' + split_line[2]
time = split_line[0]
score = split_line[-3] + ' - ' + split_line[-1]
play_type = 'Unknown'
if 'foul' in line:
    if 'technical' in line:
        play_type = play_FOUL_TECHNICAL
    elif 'flagrant foul type 1' in line:
        play_type = play_FOUL_FLAGRANT_1
    elif 'flagrant foul type 2' in line:
        play_type = play_FOUL_FLAGRANT_2
    elif 'defensive 3-seconds' in line:
        play_type = play_DEF_3_SECONDS
    elif 'free throw' in line_list[idx_line + 1]:
        play_type = play_FOUL_SHOOTING
    else:
        play_type = play_FOUL_ON_FLOOR
elif 'enters the game' in line:
    play_type = play_SUBSTITUTION
elif 'vs.' in line:
    play_type = play_JUMP_BALL
elif 'makes' in line:
    if 'free throw' in line:
        play_type = play_FT
    else:
        if 'assist' in line:
            play_type = play_FG_ASSISTED
        else:
            play_type = play_FG_UNASSISTED
elif 'miss' in line:
    if 'free throw' in line:
        play_type = play_FT_MISS
    else:
        play_type = play_FG_MISS
elif 'block' in line:
    play_type = play_FG_MISS
elif 'rebound' in line:
    if 'offensive' in line:
        play_type = play_OFFENSIVE_REBOUND
    else:
        play_type = play_DEFENSIVE_REBOUND
if play_type in fg_play_types:
    distance = '0'
    points = '2'
    if 'layup' in line:
        shot_type = SHOT_TYPE_LAYUP
    elif 'dunk' in line:
        shot_type = SHOT_TYPE_DUNK
    else:
        shot_type = SHOT_TYPE_JUMPER
        if line[line.find('foot') - 3:line.find('foot') - 1].isnumeric():
            distance = line[line.find('foot') - 3:line.find('foot') - 1]
        else:
            distance = line[line.find('foot') - 2]
        if line[line.find(' point ') - 3:line.find(' point ') - 1] != 'two':
            points = '3'
else:
    distance = 'N/A'
    if play_type in [play_FT, play_FT_MISS]:
        points = '1'
    else:
        points = 'N/A'
    shot_type = 'N/A'
secondary_player = 'N/A'
if play_type in secondary_player_play_types:
    secondary_player = 'None'
    # play_FG_ASSISTED, play_SUBSTITUTION, play_TURNOVER, play_FG_MISS
    if play_type == play_FG_MISS and 'block' in line:
        secondary_player = name
        name = split_line[4] + ' ' + split_line[5]

df = df.append({
            PLAYER: name,
            CLOCK: time,
            PLAYER_2: secondary_player,
            HOME: home,
            QUARTER: quarter,
            PLAY_TYPE: play_type,
            TEAM: team,
            OPPONENT: opponent,
            SCORE: score,
            DISTANCE: distance,
            POINTS: points,
            SHOT_TYPE: shot_type
        }, ignore_index=True)
print(df.iloc[0])
# link_list = get_link_list_from_ESPN_link('https://www.espn.com/nba/team/schedule'
#                                          '?name=DAL&season=2019')
# for idx, link in enumerate(link_list):
#     link = link[:-21] + 'playbyplay' + link[-17:]
#     try:
#         df = get_game_DF_detailed(link)
#         df.to_csv('C:/Users/DannyDell/Documents/NBADataProject/data/test_game_'
#                   + str(idx) + '_detailed_plays.csv')
#     except:
#         do_nothing = 0

#get_game_DF_detailed('https://www.espn.com/nba/playbyplay?gameId=401161489')

#
# main()
# # getFGDFFromGameLinks(mavs_game_links_2020).to_csv(
# #     'C:/Users/DannyDell/Documents/NBADataProject/data/2019-20_mavs_shot_data-quarters.csv')


# add_quarters_and_location( 'C:/Users/DannyDell/Documents/NBADataProject/data/2019
# -20_mavs_shot_data.csv', mavs_roster, 8938)
