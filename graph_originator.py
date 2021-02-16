import logging
import tomdemark
from specify_what_to_make import tickers, names

for ticker, name in zip(tickers, names):
	try:
		df = tomdemark.get_ohlc_as_pd(ticker, days=365)
		t, o, h, l, c, shortVal, longVal, sellVal, buyVal = tomdemark.get_tdsequential(df)
		tomdemark.plot_tdseq(t, o, h, l, c, shortVal, longVal, sellVal, buyVal, 
		                     ylabel=name, figshow=False, savefigname=f'./graphs/{name}.png')
	except Exception:
		logging.error(f'Error occured in ticker "{ticker}". will pass and continue...')
		continue
