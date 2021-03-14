from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources = {r'/*':{'origins': '*'}})


import time

@app.route('/')
def hello():

	return 'ok1'

@app.route('/bc')
def hello2():

	print('mc1')
	time.sleep(50)
	print('mc2')
	return 'ok2'

@app.route('/bkl')
def hello3():

	time.sleep(10)
	return 'ok3'