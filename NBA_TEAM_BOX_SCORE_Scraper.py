import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
from config import base_path
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import *

base_path = base_path()
# Render Page
browser = webdriver.Chrome()
url = 'https://stats.nba.com/teams/boxscores/'
browser.get(url)

years_tuple = (
     '1967-68',
    '1968-69', '1969-70', '1970-71', '1971-72', '1972-73', '1973-74', '1974-75', '1975-76',
    '1976-77',
    '1977-78',
    '1978-79', '1979-80', '1980-81', '1981-82', '1982-83', '1983-84', '1984-85', '1985-86',
    '1986-87', '1987-88', '1988-89', '1989-90', '1990-91', '1991-92', '1992-93', '1993-94',
    '1994-95',
    '1995-96', '1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03',
    '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11',
    '2011-12',
    '2012-13', '2013-14',
    '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20')

year_select = Select(browser.find_element_by_xpath(
    '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select'))


table = browser.find_element_by_class_name('nba-stat-table__overflow')

# Parse Data
column_labels = []
for line_index, line in enumerate(table.text.split('\n')):
    if line_index == 0:
        for column_label in line.split(' '):
            column_labels.append(column_label)

column_labels[1] = 'LOCATION'
column_labels[2] = 'OPPONENT'
column_labels.__delitem__(3)
df = pd.DataFrame(columns=column_labels)

year_select.select_by_visible_text('All Seasons')
time.sleep(20)
browser.find_element_by_xpath(
    '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]/i').click()
table = browser.find_element_by_class_name('nba-stat-table__overflow')

table_pages = 600
for i in range(table_pages):
    if i != 0:
        browser.find_element_by_xpath(
        '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]/i').click()
        time.sleep(0.300)
        browser.implicitly_wait(0.300)
    table = browser.find_element_by_class_name('nba-stat-table__overflow')
    line_list = []
    for line_index, line in enumerate(table.text.split('\n')):
        if line_index != 0:
            line_list.append(line)
    for line_index, line in enumerate(line_list):
        box_score_as_list = []
        for element_index, table_element in enumerate(line.split()):
            box_score_as_list.append(table_element)
        box_score_as_list.__delitem__(1)
        if box_score_as_list[1] == 'vs.':
            box_score_as_list[1] = 'Home'
        else:
            box_score_as_list[1] = 'Away'
        try:
            df.loc[i*50 + line_index] = box_score_as_list
        except ValueError:
            print('Incomplete Data at Line ', i*50 + line_index)
print(df)
df.to_csv(r'C:/Users/DannyDell/Documents/NBADataProject/data/nba_team_box_score_data.csv')
