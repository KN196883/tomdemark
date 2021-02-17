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
				   interval='Daily'
):
	''' ある商品の四本値をInvesting.comから取得する。
	id_は、Investing.comで商品を指定するための数字。
	不明であれば、search_id_candidates()関数で探して見当をつけよう。
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
	    dates.append(
	        datetime.strptime(record_list[0].text, '%b %d, %Y')
	    )
	    c.append(float(record_list[1].text))
	    o.append(float(record_list[2].text))
	    h.append(float(record_list[3].text))
	    l.append(float(record_list[4].text))
	df = pandas.DataFrame({
	    'Date': dates,
	    'Open': o,
	    'High': h,
	    'Low': l,
	    'Close': c
	})

	return df.iloc[::-1]

