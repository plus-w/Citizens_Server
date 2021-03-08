
import requests
import re 
from bs4 import BeautifulSoup
import json

team_info_url = "https://db.qiumibao.com/f/index/team?id=139"
transfer_url = "https://dc.qiumibao.com/shuju/public/index.php?_url=/football/transfer_team&team=%E6%9B%BC%E5%9F%8E"
player_info_url_pattern = 'https://db.qiumibao.com/f/index/player?pid='

def get_url_content(url):
    strhtml = requests.get(url)        #Get方式获取网页数据
    # print(strhtml.encoding)
    strhtml = strhtml.text.encode('iso-8859-1').decode('unicode_escape')
    # print(strhtml.apparent_encoding)
    # print(requests.utils.get_encodings_from_content(strhtml.text))
    # pdb.set_trace()
    return strhtml

def get_players_list():
    tree = BeautifulSoup(get_url_content(team_info_url), 'lxml')
    data = re.sub(r'("[\s\w]*)"([\s\w]*)"([\s\w]*")',r"\1\"\2\"\3", tree.get_text()) 
    team_information_json = json.loads(data)

    players = team_information_json['players']
    return players

def get_player_detail(pid):
    tree = BeautifulSoup(get_url_content(player_info_url_pattern + pid), 'lxml')
    data = re.sub(r'("[\s\w]*)"([\s\w]*)"([\s\w]*")',r"\1\"\2\"\3", tree.get_text()) 
    player_detail = json.loads(data)
    return player_detail

