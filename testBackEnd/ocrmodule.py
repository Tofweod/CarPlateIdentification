from init import *
from flask import jsonify


# TODO:
def __ocr_detect(image):
    return ""


@app.route('/ocrResult')
def ocr_result():
    data = {
        "result": "test context"
    }
    return jsonify(data)

