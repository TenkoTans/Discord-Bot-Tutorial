from flask import Flask
from threading import Thread
import random

app = Flask('')

def home():
    return "Bot has started"

def run():
    app.run(
    	host='0.0.0.0',
        port=random.randint(2000, 9000)
    )

def host():
    t = Thread(target=run)
    t.start()
