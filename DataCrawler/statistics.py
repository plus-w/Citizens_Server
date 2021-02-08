from bs4 import BeautifulSoup
import requests
import pdb

from soupsieve.css_types import Selector
from .utils import *
# from utils import player_name_en_dict
# from utils import all_statistics_td_column_index
# from utils import epl_statistics_td_column_index
# from utils import ucl_statistics_td_column_index
# from utils import fa_statistics_td_column_index
# from utils import efl_statistics_td_column_index
# from utils import player_nationality_en_dict

def get_team_league_statistics(bs4_parse_tree, selector, statistics_td_column_index):
    tree = bs4_parse_tree.select(selector)[0]
    trs = tree.find_all('tr')
    tds = trs[0].find_all('td')

    data_key_list = [
        'age', 'games', 'goals', 'assists', 'pens_made', 'pens_att', 'cards_yellow', 
        'cards_red', 'goals_per90', 'assists_per90', 'goals_assists_per90', 
        'goals_pens_per90', 'goals_assists_pens_per90', 'xg', 'npxg', 'xa', 'xg_per90', 
        'xa_per90', 'xg_xa_per90', 'npxg_per90', 'npxg_xa_per90']

    data_key_list = [key for key in data_key_list if key in statistics_td_column_index]

    squad_total = {}
    for key in data_key_list:
        key_idx = statistics_td_column_index[key]
        squad_total[key] = tds[key_idx].contents[0] if len(tds[key_idx].contents) != 0 else '-'

    tds = trs[1].find_all('td')
    opponent_total = {}
    for key in data_key_list:
        key_idx = statistics_td_column_index[key]
        opponent_total[key] = tds[key_idx].contents[0] if len(tds[key_idx].contents) != 0 else '-'
    
    return squad_total, opponent_total

def get_player_statistics(bs4_parse_tree, selector, statistics_td_column_index):
    
    tree = bs4_parse_tree.select(selector)[0]
    player_data = []

    data_key_list = [
        'position', 'age', 'games', 'games_starts', 'minutes', 'minutes_90s',
        'goals', 'assists', 'pens_made', 'pens_att', 'cards_yellow', 
        'cards_red', 'goals_per90', 'assists_per90', 'goals_assists_per90', 
        'goals_pens_per90', 'goals_assists_pens_per90', 'xg', 'npxg', 'xa', 'xg_per90', 
        'xa_per90', 'xg_xa_per90', 'npxg_per90', 'npxg_xa_per90']

    data_key_list = [key for key in data_key_list if key in statistics_td_column_index]

    for index, tr in enumerate(tree.find_all('tr')):
        data = {}
        player_name_en = tr.find('th').find('a').contents[0]
        data['name'] = player_name_en_dict.get(player_name_en, [player_name_en])[0]
        
        
        tds = tr.find_all('td')
        nationality_en = tds[0].find('span').contents[1].strip()
        data['nationality'] = player_nationality_en_dict.get(nationality_en, nationality_en)

        for key in data_key_list:
            key_data = tds[statistics_td_column_index[key]].contents
            if len(key_data) == 0:
                data[key] = '-'
            elif key == 'minutes':
                data[key] = key_data[0].replace(',', '')
            else:
                data[key] = key_data[0]

        # data['position'] = tds[1].contents[0]
        # data['age'] = tds[2].contents[0]
        # data['games'] = tds[3].contents[0]
        # data['games_starts'] = tds[4].contents[0]
        # data['minutes'] = tds[5].contents[0].replace(',', '')
        # data['minutes_90s'] = tds[6].contents[0]
        # data['goals'] = tds[7].contents[0]
        # data['assists'] = tds[8].contents[0]
        # data['pens_made'] = tds[9].contents[0]
        # data['pens_att'] = tds[10].contents[0]
        # data['cards_yellow'] = tds[11].contents[0]
        # data['cards_red'] = tds[12].contents[0]
        # data['goals_per90'] = tds[13].contents[0]
        # data['assists_per90'] = tds[14].contents[0]
        # data['goals_assists_per90'] = tds[15].contents[0]   # goals + assists
        # data['pens_per90'] = tds[16].contents[0]  # goals - penality
        # data['goals_assists_pens_per90'] = tds[17].contents[0]  # goals + assists - penalty
        # data['xg'] = tds[18].contents[0]      # expected goals
        # data['npxg'] = tds[19].contents[0]  # non penalty expected goals
        # data['xa'] = tds[20].contents[0]      # expected assists
        # data['xg_per90'] = tds[21].contents[0]
        # data['xa_per90'] = tds[22].contents[0]
        # data['xg_xa_per90'] = tds[23].contents[0]  # xg + xa per 90 mins
        # data['npxg_per90'] = tds[24].contents[0]
        # data['npxg_xa_per90'] = tds[25].contents[0]
        player_data.append(data)

    return player_data

def get_all_competition_statistics():
    url =  'https://fbref.com/en/squads/b8fd03ef/2020-2021/all_comps/Manchester-City-Stats-All-Competitions'
    selector = '#stats_standard_ks_combined > tbody'
    strhtml = requests.get(url).text
    tree = BeautifulSoup(strhtml, 'lxml')
    
    return {
        'team': {}, 'player': get_player_statistics(tree, selector, all_statistics_td_column_index)} 

def get_epl_statistics():
    url =  'https://fbref.com/en/squads/b8fd03ef/2020-2021/s10728/Manchester-City-Stats-Premier-League'
    team_selector = '#stats_standard_10728 > tfoot'
    player_selector = '#stats_standard_10728 > tbody'
    strhtml = requests.get(url).text
    tree = BeautifulSoup(strhtml, 'lxml')
    return {
        'team': get_team_league_statistics(tree, team_selector, epl_statistics_td_column_index), 
        'player': get_player_statistics(tree, player_selector, epl_statistics_td_column_index)}

def get_ucl_statistics():
    url = 'https://fbref.com/en/squads/b8fd03ef/2020-2021/s10096/Manchester-City-Stats-Champions-League'
    player_selector = '#stats_standard_10096 > tbody'
    team_selector = '#stats_standard_10096 > tfoot'
    strhtml = requests.get(url).text
    tree = BeautifulSoup(strhtml, 'lxml')
    return {
        'team': get_team_league_statistics(tree, team_selector, ucl_statistics_td_column_index), 
        'player': get_player_statistics(tree, player_selector, ucl_statistics_td_column_index)}

def get_fa_statistics():
    url = 'https://fbref.com/en/squads/b8fd03ef/2020-2021/s10888/Manchester-City-Stats-FA-Cup'
    player_selector = '#stats_standard_10888 > tbody'
    team_selector = '#stats_standard_10888 > tfoot'
    strhtml = requests.get(url).text
    tree = BeautifulSoup(strhtml, 'lxml')
    return {
        'team': get_team_league_statistics(tree, team_selector, fa_statistics_td_column_index), 
        'player': get_player_statistics(tree, player_selector, fa_statistics_td_column_index)}

def get_efl_statistics():
    url = 'https://fbref.com/en/squads/b8fd03ef/2020-2021/s10906/Manchester-City-Stats-EFL-Cup'
    player_selector = '#stats_standard_10906 > tbody'
    team_selector = '#stats_standard_10906 > tfoot'
    strhtml = requests.get(url).text
    tree = BeautifulSoup(strhtml, 'lxml')
    return {
        'team': get_team_league_statistics(tree, team_selector, efl_statistics_td_column_index), 
        'player': get_player_statistics(tree, player_selector, efl_statistics_td_column_index)}

# if __name__ == "__main__":
#     all_data = get_all_competition_statistics()
#     epl_data = get_epl_statistics()
#     ucl_data = get_ucl_statistics()
#     fa_data = get_fa_statistics()
#     efl_data = get_efl_statistics()

#     pdb.set_trace()