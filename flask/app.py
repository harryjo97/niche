from flask import *
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager

import numpy as np
import pandas as pd
import json

app = Flask(__name__)

def get_three(code='072520', date='20200918'):
    code = code
    date = date
    url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={date}161000'
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    stock_df = pd.DataFrame()
    for page in range(1, 41):
        pg_url = f'{url}&page={page}'
        pg_html = requests.get(pg_url, headers=headers)
        soup = BeautifulSoup(pg_html.content, 'html.parser')
        table_str = soup.find_all('table')[0]
        pg_table = pd.read_html(str(table_str))
        stock_df = stock_df.append(pg_table[0])

    stock_df = stock_df[::-1].dropna().reset_index(drop=True)
    stock_json = {}
    data_num = stock_df.shape[0]
    for i in range(data_num):
        stock_json[stock_df.iloc[i, 0]] = {
            "close": stock_df.iloc[i, 1],
            "sell": stock_df.iloc[i, 3],
            "buy": stock_df.iloc[i, 4]
        }

    return stock_json

@app.route('/three_json')
def get_three_json():
    return get_three()

@app.route('/three')
def plot_three():
    return render_template('plot_chart_three.html', stock_json=get_three())

def get_days(code='072520', date_list=['20200918','20200921','20200922','20200923']):
    code = code
    date_list = date_list
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    stock_json = {}

    for date in date_list:
        stock_df = pd.DataFrame()
        url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={date}161000'
        for page in range(1, 41):
            pg_url = f'{url}&page={page}'
            pg_html = requests.get(pg_url, headers=headers)
            soup = BeautifulSoup(pg_html.content, 'html.parser')
            table_str = soup.find_all('table')[0]
            pg_table = pd.read_html(str(table_str))
            stock_df = stock_df.append(pg_table[0])

        stock_df = stock_df[::-1].dropna().reset_index(drop=True)

        for i in range( stock_df.shape[0] ):
            stock_json[date + '/' + stock_df.iloc[i, 0]] = {
                "close": stock_df.iloc[i, 1],
                "sell": stock_df.iloc[i, 3],
                "buy": stock_df.iloc[i, 4]
            }

    return stock_json

@app.route('/days')
def plot_days():
    return render_template('plot_chart_days.html', stock_json=get_days(code='035720', date_list=['20200921','20200922','20200923','20200924']))

@app.route('/days_tooltip')
def plot_days_tooltip():
    return render_template('plot_chart_days_tooltip.html', stock_json=get_days(code='035720', date_list=['20200921','20200922']))

@app.route('/days_json')
def get_days_json():
    return get_days()

def get_codes(code='072520'):
    code = code
    date_list = ['20200918', '20200921', '20200922', '20200923']
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    stock_json = {}

    for date in date_list:
        stock_df = pd.DataFrame()
        url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={date}161000'
        for page in range(1, 41):
            pg_url = f'{url}&page={page}'
            pg_html = requests.get(pg_url, headers=headers)
            soup = BeautifulSoup(pg_html.content, 'html.parser')
            table_str = soup.find_all('table')[0]
            pg_table = pd.read_html(str(table_str))
            stock_df = stock_df.append(pg_table[0])

        stock_df = stock_df[::-1].dropna().reset_index(drop=True)

        for i in range( stock_df.shape[0] ):
            stock_json[date + '/' + stock_df.iloc[i, 0]] = {
                "close": stock_df.iloc[i, 1],
                "sell": stock_df.iloc[i, 3],
                "buy": stock_df.iloc[i, 4]
            }

    return stock_json

@app.route('/codes')
def plot_codes():
    code_list = ['072520']
    pool = Pool(processes=12)
    pool.map(get_codes, code_list)
    # store in global variable list
    return render_template('plot_chart_codes.html')

@app.route('/')
def get_data_json():
    return '<h1>GenNBio<h1>'

if __name__ == '__main__':
    app.run()
