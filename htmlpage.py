from flask import Flask
from specify_what_to_make import tickers, names

app = Flask(__name__, static_folder='graphs')

@app.route('/tomdemark')
def draw_demark():
	htmltext = '''
		<html>
		<head></head>
		<body>
	'''
	for name in names:
		htmltext += f'''
			<h2>{name}</h2>
			<img src="graphs/{name}.png", width=100%>
		'''
	htmltext += '''
		</body>
		</html>
	'''

	return htmltext

if __name__ == '__main__':
	app.run(debug=False, port=14355, host='0.0.0.0')
