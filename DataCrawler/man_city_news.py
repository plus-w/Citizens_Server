import requests
import pdb
import datetime
import json
import re
from bs4 import BeautifulSoup


url = 'https://news.zhibo8.cc/zuqiu/more.htm'

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

def get_mobile_news_url(date_str, index):
    pattern = 'https://m.zhibo8.cc/news/web/zuqiu/{}/{}.htm'.format(date_str, index)
    return pattern

def get_news_list_url_by_date(date):
    year, month, day = date['year'], date['month'], date['day']
    pattern = 'https://news.zhibo8.cc/zuqiu/json/{}-{}-{}.htm'.format(year, month, day)
    return pattern

def get_news_list_json(url):
    tree = BeautifulSoup(get_url_content(url), 'lxml')
    data = re.sub(r'("[\s\w]*)"([\s\w]*")',r"\1\'\2", tree.get_text())
    news_list_data = json.loads(data)
    return news_list_data

def get_news_list_by_date(date):
    news_list_url = get_news_list_url_by_date(date)
    news_list_data = get_news_list_json(news_list_url)

    news_list = []
    date_str = news_list_data['date']
    for news in news_list_data['video_arr']:
        labels = news['lable']
        if '曼城' not in labels:
            continue
        title = news['title']
        url = 'https://news.zhibo8.cc' + news['url']
        cover_img_url = news['thumbnail'].replace('_thumb', '')
        mobile_url = get_mobile_news_url(date_str, news['filename'])
        news_list.append({'id':news['filename'], 'date': date_str, 'title': title, 'url': url, 'mobile_url': mobile_url, 'cover_img_url': cover_img_url})
    return news_list   

# get_news_list_by_date({'year': '2021', 'month': '01', 'day': '27'})
