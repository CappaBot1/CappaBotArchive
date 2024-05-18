from flask import Flask, request

app = Flask('Flask_Server')

@app.route('/')
def home():
	return "I'm alive"

@app.route('/secrets')
def secrets():
	return "I am secret, shhhh"

class Server:
	def __init__(self):
		self.running = True
	
	def stop(self):
		self.running = False

	def run():
		app.run(host='0.0.0.0', port=8000)