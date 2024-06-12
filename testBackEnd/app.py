from videomodule import *
from ocrmodule import *
from flask import render_template,request
import config as cfg


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/getStartVal",methods=["POST"])
def get_start_val():
    data = request.get_json()
    cfg.startVideo = data.get("start")
    return '', 200


if __name__ == '__main__':
    app.run(host=host, port=port)
