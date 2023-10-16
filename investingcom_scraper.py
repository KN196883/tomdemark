import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas
from random import randint
import random_user_agent
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import investpy

# 参考 https://github.com/alvarobartt/investpy/blob/master/investpy/stocks.py

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


def search_id_candidates(query):
    ''' Investing.comの商品一覧の中から、クエリで検索する。
    get_historical()関数で必要なid_を取得するために使うことを念頭にしている

    >>> search_id_candidates(query='US T-Note')

    '''
    result = investpy.search.search_quotes(
        text=query, products=None, countries=None, n_results=None
    )
    for a in result:
        print(f'{a.id_} +++ {a.symbol} +++ {a.name}')
    return result


def get_historical(id_,
                   from_date, to_date,
                   interval='Daily',
                   date_str_fmt=None,
                   force_exclude_weekend=False,
                   dateCol_be_str=False
):
    ''' ある商品の四本値をInvesting.comから取得する。
    ====
    Args:
        id_ (int): Investing.comで商品を指定するための数字
              不明であれば、search_id_candidates()関数で探して見当をつけよう
        from_date (datetime.datetime)
        to_date (datetime.datetime)
        interval (str)
        date_str_fmt (str)
        force_exclude_weekend (bool): 
            investing.comのデータになぜか休日のオープンしていないときのデータが
            入っていることがある。その場合、この引数をTrueに指定することによって
            強制的に土日を外すことができる。
            ※土日以外の祝日を強制排除することは現状できない  # FIXME
    '''
    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "st_date": from_date.strftime('%m/%d/%Y'),
        "end_date": to_date.strftime('%m/%d/%Y'),
        "interval_sec": interval.capitalize(),
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": user_agent_rotator.get_random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    # HTTPリクエスト
    url = "https://www.investing.com/instruments/HistoricalDataAjax"
    req = requests.post(url, headers=head, data=params)
    soup = BeautifulSoup(req.text, 'html.parser')
    dates = []
    o = []
    h = []
    l = []
    c = []
    for record in soup.select_one('table tbody').select('tr'):
        record_list = record.select('td')
        if date_str_fmt is None:
            appended = datetime.strptime(record_list[0].text, '%b %d, %Y')
        else:
            appended = datetime.strptime(record_list[0].text, '%b %d, %Y').strftime(date_str_fmt)
        dates.append(appended)
        c.append(float(record_list[1].text.replace(',', '')))
        o.append(float(record_list[2].text.replace(',', '')))
        h.append(float(record_list[3].text.replace(',', '')))
        l.append(float(record_list[4].text.replace(',', '')))
    df = pandas.DataFrame({
        'Date': dates,
        'Open': o,
        'High': h,
        'Low': l,
        'Close': c
    })

    if force_exclude_weekend:
        df = df[(df['Date'].dt.dayofweek != 5) & (df['Date'].dt.dayofweek != 6)]

    if dateCol_be_str:
        df['Date'] = df['Date'].astype('str')

    return df.iloc[::-1]

