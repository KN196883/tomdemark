import logging
import tomdemark
from specify_what_to_make import tickers, names
from datetime import datetime, timedelta
import logging
from time import sleep
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s : %(asctime)s : %(message)s',
                    )

while True:
	for ticker, name in zip(tickers, names):
		logging.info(f'start drawing of "{ticker}"...')
		try:
			df = tomdemark.get_ohlc_as_pd(ticker, days=365)
			t, o, h, l, c, shortVal, longVal, sellVal, buyVal = tomdemark.get_tdsequential(df)
			tomdemark.plot_tdseq(t, o, h, l, c, shortVal, longVal, sellVal, buyVal, 
			                     ylabel=name, figshow=False, savefigname=f'./graphs/{name}.png')
		except Exception:
			logging.error(f'Error occured in ticker "{ticker}". will pass and continue...')
			continue
		sleep(1)

	with open('last_originated_datetime.txt', 'w') as f:
		f.write((datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S"))

	# 3時間待機する
	logging.info('3時間待機します...')
	sleep(60*60*3)