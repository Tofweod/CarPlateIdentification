from flask import Flask
import easyocr

app = Flask(__name__)

reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)

host = '0.0.0.0'

port = 5001
