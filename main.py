from typing import List

import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = 'https://www.espn.com'
HEADERS = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.example'  # This is another valid field
    }

def split_list(list1, chunk_size):
    chunked_list = []
    for i in range(0, len(list1), chunk_size):
        chunk = list1[i:i + chunk_size]
        chunked_list.append(chunk)
    return chunked_list

def sort_table_data(collected_table_data: dict) -> list[dict]:
    sorted_table_data = []
    cleaned_categories = collected_table_data['team_data_categories'][1:] if '' in collected_table_data['team_data_categories'] else collected_table_data['team_data_categories']
    split_stats = split_list(collected_table_data['stats'], len(cleaned_categories))
    for i, player in enumerate(collected_table_data['players']):
        data = {'Player Name': player}
        stats = dict(zip(cleaned_categories, split_stats[i]))
        data.update(stats)
        sorted_table_data.append(data)
    return sorted_table_data

def collect_table_data(box_score_data: BeautifulSoup, key_name: str, team_index: int) -> List:
    collected_table_data = {}
    # how to handle the 'No team name Kick Returns' or 'No team name Punt Returns'
    # just do a check on if 'No' in table data? pass? or return empty array?
    if 'Defensive' not in key_name:
        team_table_data = box_score_data.select('.Boxscore__Team')[team_index]
        team_stats = team_table_data.select('.Table__TBODY')
        collected_table_data['team_data_categories'] = [t.text for t in team_table_data.select('.Table__TH')]
        collected_table_data['players'] = [t.text for t in team_stats[0]]
        collected_table_data['stats'] = [t.text for t in team_stats[1].select('.Table__TD')]
        return sort_table_data(collected_table_data)
    else:
        print('the defensive table stuff')
        return []

def get_individual_team_boxscores(team_data: BeautifulSoup):
    box_scores = team_data.select('.Boxscore__Category')
    team_1_box_score = {}
    team_2_box_score = {}
    # just got passing and returned
    # probably just need to change it to not return and get all stats
    for box_score in box_scores:
        key_name = box_score.select('.TeamTitle__Name')[0].text
        team_1_box_score[key_name] = collect_table_data(box_score, key_name, 0)
        print(f'team 1 data: {key_name}')
        key_name = box_score.select('.TeamTitle__Name')[1].text
        team_2_box_score[key_name] = collect_table_data(box_score, key_name, 1)
        print(f'team 2 data: {key_name}')
        return [team_1_box_score, team_2_box_score]


def get_boxscores(df: pd.DataFrame) -> List[dict]:
    boxscores = []
    for index, row in df.iterrows():
        soup = BeautifulSoup(requests.get(URL + row['Box Score Url'],headers=HEADERS).content, 'html.parser')
        data = soup.select('.Boxscore')[0]
        boxscores.append(get_individual_team_boxscores(data))
    return boxscores

def get_games_data(soup: BeautifulSoup, week: int) -> pd.DataFrame:
    all_data = []
    games = soup.select('.ScoreboardScoreCell__Item')
    game_links = soup.select('.Scoreboard__Callouts')
    counter = 0
    game_number = 0
    for game in games:
        counter += 1
        if counter % 2 != 0:
            title = game.find_previous(class_='Card__Header__Title').text
            team1 = [t.text for t in game.select('.ScoreCell__TeamName')][0]
            score1 = [t.text for t in game.select('.ScoreCell__Score')][0] or '-'
            quarter_scores1 = {f'q{i + 1}': int(t.text)  for i, t in enumerate(game.select('.ScoreboardScoreCell__Value'))}
            continue
        else:
            team2 = [t.text for t in game.select('.ScoreCell__TeamName')][0]
            score2 = [t.text for t in game.select('.ScoreCell__Score')][0] or '-'
            quarter_scores2 = {f'q{i + 1}': int(t.text)  for i, t in enumerate(game.select('.ScoreboardScoreCell__Value'))}
            boxscores = game_links[game_number].find_all('a', href=True)
            boxsore_url = boxscores[1]['href']
            game_number += 1
            all_data.append((week, title, team1, score1, quarter_scores1, team2, score2, quarter_scores2, boxsore_url))
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
        'Box Score Url'])


if __name__ == '__main__':
    week = 18
    soup = BeautifulSoup(requests.get(f'{URL}/nfl/scoreboard/_/week/18/year/2023/seasontype/2', headers=HEADERS).content, 'html.parser')
    df = get_games_data(soup, week)
    boxscores = get_boxscores(df)
    import pdb;pdb.set_trace()
    print('done')
