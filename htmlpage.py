from flask import Flask
from specify_what_to_make import wanted_investingcom_ids

app = Flask(__name__, static_folder='graphs')

@app.route('/tomdemark')
def draw_demark():
	with open('last_originated_datetime.txt', 'r') as f:
		last_originated_datetime = f.read()
	htmltext = f'''
		<html>
		<head></head>
		<body>
		最終更新: {last_originated_datetime}<br>
		<small>自分向け注意: ローカルで実行している場合、-9時間</small>
	'''
	for name, invcom_id in wanted_investingcom_ids.items():
		htmltext += f'''
			<h2>{name}</h2>
			<img src="/graphs/{name}.png", width=100%>
		'''
	htmltext += '''
		</body>
		</html>
	'''

	return htmltext

if __name__ == '__main__':
	app.run(debug=False, port=14355, host='0.0.0.0')
