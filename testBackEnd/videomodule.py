from init import *
from flask import Response
import cv2


# TODO:
def __probe_video_stable(frame_queue, threshold, method):
    return True


def __generate_video_stream():
    cap = cv2.VideoCapture('test.mp4')
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()


@app.route('/testVideo')
def test_video():
    return Response(__generate_video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")
