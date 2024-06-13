from flask import Flask, render_template, request, redirect, Response
import config as cfg
from video.videomodule import video_module
from video.videoprobe import ProbeMethod
from ocr.ocrmodule import ocr_module


app = Flask(__name__, template_folder=cfg.templates)

app.register_blueprint(video_module)
app.register_blueprint(ocr_module)


@app.route("/")
def index() -> str:
    return render_template('index.html',
                           spring_boot_url=cfg.spring_boot_url,
                           spring_boot_port=cfg.spring_boot_port,
                           video_during_time=cfg.video_during_time,
                           threshold=cfg.threshold,
                           method=ProbeMethod.enum_str(cfg.method))


@app.route("/update", methods=["POST", "GET"])
def update() -> Response | str:
    if request.method == "POST":
        cfg.spring_boot_url = request.form["spring_boot_url"]
        cfg.spring_boot_port = int(request.form["spring_boot_port"])
        cfg.video_during_time = float(request.form["video_during_time"])
        cfg.threshold = float(request.form["threshold"])
        cfg.method = int(request.form["method"])
        return redirect("/")

    return render_template('update.html',
                           spring_boot_url=cfg.spring_boot_url,
                           spring_boot_port=cfg.spring_boot_port,
                           video_during_time=cfg.video_during_time,
                           threshold=cfg.threshold,
                           method=cfg.method,
                           methods=ProbeMethod)


@app.route("/getStartVal", methods=["POST"])
def get_start_val() -> tuple | None:
    data = request.get_json()
    cfg.startVideo = data.get("start")
    return '', 200


if __name__ == '__main__':
    app.run(host=cfg.host, port=cfg.port, debug=False)
