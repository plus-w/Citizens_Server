

from datetime import datetime
from typing import List


def network_format(data: dict):
    format_data = {}
    format_data['error_code'] = 0
    format_data['error_message'] = ''
    format_data['data'] = [data]
    return format_data

def network_format(data: List[dict]):
    format_data = {'error_code': 0, 'error_message': '', 'data': data}
    return format_data

def date_yesterday(date):
    y, m, d = date.strip().split('-')
    y, m, d = int(y), int(m), int(d)
    if d > 1 :
        d -= 1
    else:
        if m == 3:
            m -= 1
            d = 29 if y % 4 == 0 else 28
        elif m == 1:
            y -= 1
            m = 12
            d = 31
        else:
            m -= 1
            d = 31 if m in [1,3,5,7,8,10,12] else 30
    return str(datetime.date(y, m, d))

def date_compare(date_a, date_b):
    y_a, m_a, d_a = date_a.strip().split()
    y_b, m_b, d_b = date_b.strip().split()

    if y_a < y_b: return '<'
    elif y_a > y_b: return '>'
    else:
        if m_a < m_b: return '<'
        elif m_a > m_b: return '>'
        else:
            if d_a < d_b: return '<'
            elif d_a > d_b: return '>'
            else: return '='

def check_date(date):
    if len(date.strip().split('-')) != 3:
        return {'error_code': 1, 'error_message': 'Invalid date format, should be like 2021-01-01'}
    else:
        y, m, d = date.strip().split('-')
        if not y.isdigit() or not m.isdigit() or not d.isdigit():
            return {'error_code': 1, 'error_message': 'Invalid date format, should be like 2021-01-01'}
        else:
            y, m, d = int(y), int(m), int(d)
            date_error = False
            if y < 2021 or m < 1 or m > 12 or d < 1 or d > 31:
                date_error = True
            else:
                if y % 4 == 0 and m == 2 and d > 29 or y % 4 != 0 and m == 2 and d > 28:
                    date_error = True
                if m not in [1,3,5,7,8,10,12] and d > 30:
                    date_error = True
            if date_error:
                return {'error_code': 1, 'error_message': 'Invalid date range'}
            else:
                return {'error_code': 0, 'error_message': ''}
