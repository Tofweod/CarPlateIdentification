import base64
import numpy as np
from init import *
from flask import Response, jsonify
import cv2
from videoprobe import VideoStableProbe

videoFinished: bool = False

current_frame: np.array = None


def __generate_video_stream(url:str | int =None) -> bytes:
    if url :
        cap = cv2.VideoCapture(url)
    else:
        cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FPS,60)
    print("fps:",cap.get(cv2.CAP_PROP_FPS))
    probe = VideoStableProbe(cap)
    global current_frame
    while cap.isOpened():
        current_frame,stable = probe()
        if stable:
            finish()
            break
        _, buffer = cv2.imencode('.jpg', current_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()


def __generate_picture_stream(cv_img: np.ndarray) -> bytes:
    ret_val, buffer = cv2.imencode('.jpg', cv_img)
    if ret_val:
        frame = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/testVideo')
def test_video() -> Response:
    return Response(__generate_video_stream('test/test.mp4'), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/rawVideo')
def raw_video() -> Response:
    return Response(__generate_video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/preResult')
def pre_result() -> Response:
    # TODO:here we just send picture for test, pre-progress need to be done and generate numpy of pre-handled picture
    response = Response(__generate_picture_stream(current_frame), mimetype="multipart/x-mixed-replace; boundary=frame")
    return response


@app.route('/yoloResult')
def yolo_result() -> Response:
    response = Response(__generate_picture_stream(current_frame), mimetype="multipart/x-mixed-replace; boundary=frame")
    return response


@app.route('/sendFinished')
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
@app.route('/finish')
def finish() -> tuple | None:
    global videoFinished
    videoFinished = True
    return " ", 200


@app.route('/reset')
def reset() -> tuple | None:
    print("flask has been reset")
    global videoFinished
    videoFinished = False
    return " ",200

