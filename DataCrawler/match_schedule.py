import requests
import pdb
import datetime
import json
from bs4 import BeautifulSoup


base_url = 'https://db.qiumibao.com/f/index/teamschedules?id='

def get_url_content(url):
    strhtml = requests.get(url)        #Get方式获取网页数据
    # print(strhtml.encoding)
    strhtml = strhtml.text.encode('iso-8859-1').decode('unicode_escape')
    # print(strhtml.apparent_encoding)
    # print(requests.utils.get_encodings_from_content(strhtml.text))
    # pdb.set_trace()
    return strhtml
# tree = BeautifulSoup(strhtml, 'lxml')

# #boxlist > div.dataList > ul:nth-child(1) > li:nth-child(7) > span.articleTitle > a

# news_data = tree.select('#boxlist > div.dataList > ul:nth-child(5) > li > span.articleTitle > a')
# labels_data = tree.select('#boxlist > div.dataList > ul:nth-child(5) > li')

def get_match_schedule(team_id: str):
    url = base_url + team_id
    match_data_json = json.loads(BeautifulSoup(get_url_content(url), 'lxml').get_text())
    if match_data_json['status'] != 1:
        return {'error_code': 1, 'error_message': 'Query failed'}
    match_item_list = match_data_json['data']
    result = []
    for match in match_item_list:
        match_filtered = {}
        match_filtered['match_id'] = match['id']
        match_filtered['season'] = match['season_display']  # 2020/2021
        match_filtered['league'] = match['league']  # 欧冠，英超，联赛杯，足总杯
        match_filtered['type'] = match['type']  # 1/4决赛
        match_filtered['round'] = match['round']  # 20
        match_filtered['home_id'] = match['home_id']
        match_filtered['home_name'] = match['home']
        match_filtered['home_logo_url'] = match['home_logo']
        match_filtered['away_id'] = match['away_id']
        match_filtered['away_name'] = match['away']
        match_filtered['away_logo_url'] = match['away_logo']
        match_filtered['home_score'] = match['home_score']
        match_filtered['away_score'] = match['away_score']
        match_filtered['date'] = match['s_date']
        match_filtered['time'] = match['s_time']
        result.append(match_filtered)

    return result

# get_news_list_by_date({'year': '2021', 'month': '01', 'day': '27'})
