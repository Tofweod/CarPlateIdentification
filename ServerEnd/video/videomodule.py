import base64
import time
import numpy as np
from flask import Blueprint, Response, jsonify
import cv2
from video.videoprobe import VideoStableProbe
import video.videoprogress as vpg
import config as cfg
from yolo.utils import detect, draw_boxes, result_filter
from ocr.ocrmodule import set_ocr_results, clear_ocr_results
from video.timerutil import MultiTimer

multi_timer = MultiTimer()

video_module = Blueprint('video_module', __name__)

videoFinished: bool = False

yolo_is_timeout: bool = False

current_frame: np.ndarray
yolo_frame: np.ndarray
pre_frame: np.ndarray

probe: VideoStableProbe | None = None


@video_module.route('/probeResult')
def probe_result() -> Response:
    global probe
    if probe is None:
        return Response("No data stream", content_type='text/plain')

    def result_stream():
        while not probe.stable:
            time.sleep(0.5)
            yield f"data: {probe.fea_period}\n\n"

    return Response(result_stream(), content_type='text/event-stream')


def __frame2bytes(frame: np.ndarray, _format: str) -> bytes:
    _, buffer = cv2.imencode(_format, frame)
    return buffer.tobytes()


def yolo_timeout():
    global yolo_is_timeout
    yolo_is_timeout = True


def __generate_video_stream(url: str | int = None) -> bytes:
    if url:
        cap = cv2.VideoCapture(url)
    else:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 60)
    global current_frame
    global yolo_frame
    global pre_frame
    global probe
    probe = VideoStableProbe(cap, cfg.video_during_time, cfg.threshold)

    multi_timer.start_timer("yolo_timer", cfg.yolo_timeout, yolo_timeout)
    stable = False
    while cap.isOpened():
        ret, current_frame = cap.read()
        if not ret:
            continue
        # pre-progress for stable test
        vpg_frame = vpg.get_gauss_sharpen_gray(current_frame)
        # test stable
        if vpg_frame is not None:
            stable = probe(vpg_frame)
        global yolo_is_timeout
        if stable or yolo_is_timeout:
            multi_timer.reset_timer("yolo_timer", cfg.yolo_timeout)
            yolo_is_timeout = False
            boxes, confidences, class_ids, idxs = detect(current_frame, current_frame.shape[1], current_frame.shape[0])
            # result_filter 通过Ioc和面积过滤yolo结果，选择面积最大的plate
            max_idx, box, confidence = result_filter(cfg.yolo_confidence, cfg.yolo_size, boxes, confidences, idxs)
            if max_idx != -1:
                x, y, w, h = box
                if x <= 0 or y <= 0 or w <= 0 or h <= 0:
                    continue
                yolo_frame = current_frame[y:y + h, x:x + w]
                pre_frame = vpg.progress_yolo_img(yolo_frame, class_ids[max_idx])
                current_frame = draw_boxes(current_frame, boxes, confidences, class_ids, idxs)
                set_ocr_results(pre_frame, class_ids[max_idx])
                finish()
            else:
                probe.clear()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + __frame2bytes(current_frame, ".jpg") + b'\r\n')
    multi_timer.stop_timer("yolo_timer")
    cap.release()


def __generate_picture_stream(cv_img: np.ndarray) -> bytes:
    ret_val, buffer = cv2.imencode('.jpg', cv_img)
    if ret_val:
        frame = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@video_module.route('/testVideo')
def test_video() -> Response:
    return Response(__generate_video_stream("test/yolo_test.mp4"),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@video_module.route('/rawVideo')
def raw_video() -> Response:
    return Response(__generate_video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


@video_module.route('/preResult')
def pre_result() -> Response:
    response = Response(__generate_picture_stream(pre_frame), mimetype="multipart/x-mixed-replace; boundary=frame")
    return response


@video_module.route('/yoloResult')
def yolo_result() -> Response:
    # TODO: yolo result
    response = Response(__generate_picture_stream(yolo_frame), mimetype="multipart/x-mixed-replace; boundary=frame")
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
    global yolo_frame
    global pre_frame
    yolo_frame = pre_frame = None
    clear_ocr_results()
    return " ", 200
