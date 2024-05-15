from flask import Flask, request
from threading import Thread

app = Flask('Flask_Server')

@app.route('/')
def home():
  return "I'm alive"

def run():
  app.run(host='0.0.0.0', port=8000)

def keep_alive():
  t = Thread(target=run)
  t.start()