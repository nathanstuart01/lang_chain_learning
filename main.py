from typing import List
import time
import random

import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = 'https://www.espn.com'
HEADERS = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.example'
    }

def split_list(list1, chunk_size):
    chunked_list = []
    for i in range(0, len(list1), chunk_size):
        chunk = list1[i:i + chunk_size]
        chunked_list.append(chunk)
    return chunked_list

def sort_table_data(collected_table_data: dict, key_name: str) -> list[dict]:
    sorted_table_data = []
    if 'Defensive' in key_name:
        cleaned_categories = collected_table_data['team_data_categories'][4:]
        cleaned_categories[0] = 'TOT TACKLES'
        cleaned_categories[1] = 'SOLO TACKLES'
    else:
        cleaned_categories = collected_table_data['team_data_categories'][1:]
    split_stats = split_list(collected_table_data['stats'], len(cleaned_categories))
    for i, player in enumerate(collected_table_data['players']):
        data = {'Player Name': player}
        stats = dict(zip(cleaned_categories, split_stats[i]))
        data.update(stats)
        sorted_table_data.append(data)
    return sorted_table_data

def collect_table_data(box_score_data: BeautifulSoup, key_name: str, team_index: int) -> List:
    collected_table_data = {}
    team_table_data = box_score_data.select('.Boxscore__Team')[team_index]
    team_stats = team_table_data.select('.Table__TBODY')
    collected_table_data['team_data_categories'] = [t.text for t in team_table_data.select('.Table__TH')]
    collected_table_data['players'] = [t.text for t in team_stats[0]] if team_stats else []
    collected_table_data['stats'] = [t.text for t in team_stats[1].select('.Table__TD')] if team_stats else []
    return sort_table_data(collected_table_data, key_name)

def get_individual_team_boxscores(team_data: BeautifulSoup):
    box_scores = team_data.select('.Boxscore__Category')
    team_1_box_score = {}
    team_2_box_score = {}
    for box_score in box_scores:
        key_name = box_score.select('.TeamTitle__Name')[0].text
        team_1_box_score[key_name] = collect_table_data(box_score, key_name, 0)
        key_name = box_score.select('.TeamTitle__Name')[1].text
        team_2_box_score[key_name] = collect_table_data(box_score, key_name, 1)
    return [team_1_box_score, team_2_box_score]


def get_boxscores(url: str) -> List[dict]:
    soup = BeautifulSoup(requests.get(URL + url, headers=HEADERS).content, 'html.parser')
    data = soup.select('.Boxscore')[0]
    return get_individual_team_boxscores(data)


def get_games_data(soup: BeautifulSoup, week: int) -> pd.DataFrame:
    all_data = []
    games = soup.select('.ScoreboardScoreCell__Item')
    game_links = soup.select('.Scoreboard__Callouts')
    counter = 0
    game_number = 0
    for game in games:
        counter += 1
        box_scores = game_links[game_number].find_all('a', href=True)
        boxsore_url = box_scores[1]['href']
        box_scores = get_boxscores(boxsore_url)
        if counter % 2 != 0:
            title = game.find_previous(class_='Card__Header__Title').text
            team1 = [t.text for t in game.select('.ScoreCell__TeamName')][0]
            score1 = [t.text for t in game.select('.ScoreCell__Score')][0] or '-'
            quarter_scores1 = {f'q{i + 1}': int(t.text)  for i, t in enumerate(game.select('.ScoreboardScoreCell__Value'))}
            box_score_1 = box_scores[0]
            continue
        else:
            team2 = [t.text for t in game.select('.ScoreCell__TeamName')][0]
            score2 = [t.text for t in game.select('.ScoreCell__Score')][0] or '-'
            quarter_scores2 = {f'q{i + 1}': int(t.text)  for i, t in enumerate(game.select('.ScoreboardScoreCell__Value'))}
            box_score_2 = box_scores[1]
            game_number += 1
            all_data.append((week, title, team1, score1, quarter_scores1, team2, score2, quarter_scores2, box_score_1, box_score_2))
            continue
    
    return pd.DataFrame(all_data, columns=[
        'Week',
        'Date', 
        'Team 1', 
        'Score 1', 
        'Quarter Scores Team 1', 
        'Team 2', 
        'Score 2',
        'Quarter Scores Team 2',
        'Team 1 Box Score',
        'Team 2 Box Score'])


if __name__ == '__main__':
    reg_season_dfs = {}
    years = range(2013, 2024)
    weeks = range(1, 19)
    for year in years:
        reg_season_dfs[f'season year {year}'] = []
        for week in weeks:
            req = requests.get(f'{URL}/nfl/scoreboard/_/week/{week}/year/{year}/seasontype/2', headers=HEADERS)
            if req.status_code == 200:
                soup = BeautifulSoup(req.content, 'html.parser')
                reg_season_dfs[f'season year {year}'].append(get_games_data(soup, week))
                time.sleep(random.randint(3, 6))
            else:
                print(req.status_code)
                print(req.content)
    print('done')
