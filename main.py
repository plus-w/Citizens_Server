from utils import check_date, date_compare, date_yesterday, network_format
from flask import Flask, request
from flask_restful import Api, Resource
import datetime
import sqlite3 as sql
from DataCrawler.man_city_news import get_news_list_by_date

app = Flask(__name__)
api = Api(app)

db = 'citizens.db'

class NewsList(Resource):
    def get(self, date_str):
        # procedures:
        # 1. if date == today or date > today, go to zhibo8.cc to find latest news and store to db
        # 2. if date < today, go to db to get news of 3 days before that day
        
        # validation 
        msg = check_date(date_str)
        if msg['error_code'] != 0: return msg
        
        compare = date_compare(date_str, str(datetime.date.today()))
        news_list = []
        date = {'year': date_str[:4], 'month': date_str[5:7], 'day': date_str[8:10]}
        if compare == '=' or compare == '>':
            news_list = network_format(get_news_list_by_date(date))
        else:
            for i in range(3):
                yesterday = date_yesterday(date_str)
                date = {'year': yesterday[:4], 'month': yesterday[5:7], 'day': yesterday[8:10]}
                news_list.append(get_news_list_by_date(date))
                date_str = yesterday
            news_list = network_format(news_list)
        return news_list
    
    # def put(self, todo_id):
    #     todos[todo_id] = request.form['data']
    #     return {todo_id: todos[todo_id]}

api.add_resource(NewsList, '/news/<string:date_str>')

def initialize():
    # db_connection = sql.connect('flask_learn.db')
    return True



if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000

    # initialize
    # find news from 2021.01.01 and store to db

    app.run(debug=False, host=host, port=port)