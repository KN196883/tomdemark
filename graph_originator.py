import logging
import tomdemark
from specify_what_to_make import wanted_investingcom_ids
from investingcom_scraper import get_historical
from datetime import datetime, timedelta
import logging
from time import sleep
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s : %(asctime)s : %(message)s',
                    )

while True:
	# for ticker, name in zip(tickers, names):
	for name, invcom_id in wanted_investingcom_ids.items():
		logging.info(f'start drawing of "{name}"...')
		try:
			df = get_historical(
					invcom_id,
					to_date=datetime.now()+timedelta(days=1),
					from_date=datetime.now()-timedelta(days=365),
					date_str_fmt='%Y-%m-%d'
				 )
			t, o, h, l, c, shortVal, longVal, sellVal, buyVal = tomdemark.get_tdsequential(df)
			tomdemark.plot_tdseq(t, o, h, l, c, shortVal, longVal, sellVal, buyVal, 
			                     ylabel=name, figshow=False, savefigname=f'./graphs/{name}.png')
		except Exception as e:
			logging.error(f'Error occured in "{name}". will pass and continue...')
			logging.error(e)
			continue
		sleep(1)

	with open('last_originated_datetime.txt', 'w') as f:
		f.write((datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S"))

	# 3時間待機する
	logging.info('3時間待機します...')
	sleep(60*60*3)