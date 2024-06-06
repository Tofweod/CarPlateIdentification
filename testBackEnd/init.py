from flask import Flask
import easyocr

app = Flask(__name__)

reader = None

host = '0.0.0.0'

port = 5001


def init_back_end():
    global reader
    reader = easyocr.Reader(['en', 'ch_sim'])

