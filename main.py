from DataCrawler.statistics import get_all_competition_statistics, get_efl_statistics, get_epl_statistics, get_fa_statistics, get_statistics, get_ucl_statistics
from DataCrawler.match_schedule import get_match_schedule
from utils import check_date, date_compare, date_yesterday, network_format
from flask import Flask, request
from flask_restful import Api, Resource
import datetime
import sqlite3 as sql
from DataCrawler.man_city_news import get_news_list_by_date

app = Flask(__name__)
api = Api(app)

db = 'citizens.db'

class Statistics(Resource):
    def get(self):
        return network_format(get_statistics())

class NewsListByDate(Resource):
    def post(self, date_str):
        # procedures:
        # 1. if date == today or date > today, go to zhibo8.cc to find latest news and store to db
        # 2. if date < today, go to db to get news of 3 days before that day
        
        labels = request.form['labels'].split(',')

        # validation 
        msg = check_date(date_str)
        if msg['error_code'] != 0: return msg
        
        compare = date_compare(date_str, str(datetime.date.today()))
        news_list = []
        date = {'year': date_str[:4], 'month': date_str[5:7], 'day': date_str[8:10]}
        if compare == '=' or compare == '>':
            news_list = network_format(get_news_list_by_date(date, labels))
        else:
            for i in range(3):
                date = {'year': date_str[:4], 'month': date_str[5:7], 'day': date_str[8:10]}
                news_list += get_news_list_by_date(date, labels)
                date_str = date_yesterday(date_str)
            news_list = network_format(news_list)
        return news_list
    
    # def put(self, todo_id):
    #     todos[todo_id] = request.form['data']
    #     return {todo_id: todos[todo_id]}

# class NewsListByPage(Resource):
#     def get(self, page_num):
#         # procedures:
#         # 1. if page_num < 0, return error
#         # 2. if page_num 
        
#         # validation 
#         msg = check_date(date_str)
#         if msg['error_code'] != 0: return msg
        
#         compare = date_compare(date_str, str(datetime.date.today()))
#         news_list = []
#         date = {'year': date_str[:4], 'month': date_str[5:7], 'day': date_str[8:10]}
#         if compare == '=' or compare == '>':
#             news_list = network_format(get_news_list_by_date(date))
#         else:
#             for i in range(3):
#                 date = {'year': date_str[:4], 'month': date_str[5:7], 'day': date_str[8:10]}
#                 news_list += get_news_list_by_date(date)
#                 date_str = date_yesterday(date_str)
#             news_list = network_format(news_list)
#         return news_list

class MatchSchedule(Resource):
    def get(self, team_id):
        if not team_id.isdigit() or int(team_id) < 36 or int(team_id) > 478:
            return {'error_code': 1, 'error_message': "Invalid team id", 'data':[]}

        return network_format(get_match_schedule(team_id))

api.add_resource(MatchSchedule, '/match/<string:team_id>')
api.add_resource(NewsListByDate, '/news/<string:date_str>')
api.add_resource(Statistics, '/statistics')

def initialize():
    db_connection = sql.connect('citizens.db')
    return True



if __name__ == "__main__":
    host = '0.0.0.0'
    port = 4000

    # initialize
    # find news from 2021.01.01 and store to db

    app.run(debug=True, host=host, port=port)