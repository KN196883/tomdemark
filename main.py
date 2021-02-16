from mailer import sendGmailAttach
from confidential import username, password, to_address
import tomdemark


sub = 'Tom Demark Indicator'
body = ''

df = tomdemark.get_ohlc_as_pd('JPY=X', days=365)
t, o, h, l, c, shortVal, longVal, sellVal, buyVal = tomdemark.get_tdsequential(df)
tomdemark.plot_tdseq(t, o, h, l, c, shortVal, longVal, sellVal, buyVal, 
                     ylabel='USDJPY', figshow=False, savefigname='USDJPY.png')

attach_files = [{'name': 'USDJPY.png', 'path': './USDJPY.png'}]
sendGmailAttach(username, password, to_address, sub, body, attach_files)
