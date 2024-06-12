import base64

from init import *
from flask import Response, jsonify
import cv2

videoFinished = False

current_frame = None


# TODO:
def __probe_video_stable(frame_queue, threshold, method):
    return True


def __generate_video_stream():
    cap = cv2.VideoCapture('test/test.mp4')
    global current_frame
    while cap.isOpened():
        success, current_frame = cap.read()
        # TODO: implement __probe_video_stable
        # if __probe_video_stable():
        #     break;
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', current_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()


def __generate_picture_stream(cv_img):
    ret_val, buffer = cv2.imencode('.jpg', cv_img)
    if ret_val:
        frame = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/testVideo')
def test_video():
    return Response(__generate_video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/preResult')
def pre_result():
    # TODO:here we just send picture for test, pre-progress need to be done and generate numpy of pre-handled picture
    img = cv2.imread('test/test.jpg')
    response = Response(__generate_picture_stream(img), mimetype="multipart/x-mixed-replace; boundary=frame")
    del img
    return response


@app.route('/yoloResult')
def yolo_result():
    img = cv2.imread('test/test.jpg')
    response = Response(__generate_picture_stream(img), mimetype="multipart/x-mixed-replace; boundary=frame")
    del img
    return response


@app.route('/sendFinished')
def send_finished():
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
def finish():
    global videoFinished
    videoFinished = True
    return " ", 200

