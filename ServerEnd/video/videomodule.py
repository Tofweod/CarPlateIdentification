import base64
import time
import numpy as np
from flask import Blueprint, Response, jsonify
import cv2
from video.videoprobe import VideoStableProbe
import config as cfg

video_module = Blueprint('video_module', __name__)

videoFinished: bool = False

current_frame: np.ndarray

probe: VideoStableProbe | None = None


@video_module.route('/probeResult')
def probe_result() -> Response:
    global probe
    if probe is None:
        return Response("No data stream", content_type='text/plain')

    def result_stream():
        while probe.available():
            time.sleep(0.5)
            yield f"data: {probe.fea_period}\n\n"

    return Response(result_stream(), content_type='text/event-stream')


def __generate_video_stream(url: str | int = None) -> bytes:
    if url:
        cap = cv2.VideoCapture(url)
    else:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 60)
    print("fps:", cap.get(cv2.CAP_PROP_FPS))
    print("threshold:", cfg.threshold)
    global current_frame
    global probe
    probe = VideoStableProbe(cap, cfg.video_during_time, cfg.threshold)
    while probe.available():
        current_frame, stable = probe()
        # if stable:
        #     finish()
        #     break

        # TODO: add yolo bound into current_frame
        _, buffer = cv2.imencode('.jpg', current_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finish()
    cap.release()


def __generate_picture_stream(cv_img: np.ndarray) -> bytes:
    ret_val, buffer = cv2.imencode('.jpg', cv_img)
    if ret_val:
        frame = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@video_module.route('/testVideo')
def test_video() -> Response:
    return Response(__generate_video_stream("test/test.mp4"),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@video_module.route('/rawVideo')
def raw_video() -> Response:
    return Response(__generate_video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


@video_module.route('/preResult')
def pre_result() -> Response:
    # TODO:here we just send picture for test, pre-progress need to be done and generate numpy of pre-handled picture
    response = Response(__generate_picture_stream(current_frame), mimetype="multipart/x-mixed-replace; boundary=frame")
    return response


@video_module.route('/yoloResult')
def yolo_result() -> Response:
    response = Response(__generate_picture_stream(current_frame), mimetype="multipart/x-mixed-replace; boundary=frame")
    return response


@video_module.route('/sendFinished')
def send_finished() -> Response:
    global videoFinished
    global current_frame
    if not videoFinished:
        return jsonify({'finish': videoFinished,
                        'baseImg': ''
                        })
    if current_frame is None:
        return jsonify({'status': 'false'})
    _, buffer = cv2.imencode('.jpg', current_frame)
    base64_data = base64.b64encode(buffer.tobytes()).decode('utf-8')
    return jsonify({
        'finish': videoFinished,
        "baseImg": base64_data,
    })


# add route for test
@video_module.route('/finish')
def finish() -> tuple | None:
    global videoFinished
    videoFinished = True
    return " ", 200


@video_module.route('/reset')
def reset() -> tuple | None:
    print("flask has been reset")
    global videoFinished
    videoFinished = False
    global probe
    probe = None
    return " ", 200
