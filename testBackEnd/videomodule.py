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
        # TODO: implement __probe_video_stable
        # if __probe_video_stable():
        #     break;
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
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
    img = cv2.imread('test.jpg')
    response = Response(__generate_picture_stream(img), mimetype="multipart/x-mixed-replace; boundary=frame")
    del img
    return response


@app.route('/yoloResult')
def yolo_result():
    img = cv2.imread('test.jpg')
    response = Response(__generate_picture_stream(img), mimetype="multipart/x-mixed-replace; boundary=frame")
    del img
    return response


