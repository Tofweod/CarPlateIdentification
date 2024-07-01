from flask import Blueprint, jsonify, Response
import cv2
from paddleocr import PaddleOCR
import numpy as np
from ocr.ocrresult import OCRResult
from ocr.platecheck import check_plate

ocr_module = Blueprint('ocr_module', __name__)

ocr_model = PaddleOCR(use_angle_cls=True, lang='ch')

result: OCRResult | None = None


def __ocr_recognize(img: np.array) -> OCRResult:
    results = ocr_model.ocr(img, det=False)[0][0]
    text, confidence = results
    return OCRResult(text, confidence)


@ocr_module.route('/ocrTest')
def ocr_test() -> Response:
    ocr_objs = []
    for i in range(1, 7):
        image = "test/test" + str(i) + ".png"
        img = cv2.imread(image)
        ocr_objs.append(__ocr_recognize(img))
    return jsonify([obj.to_dict() for obj in ocr_objs])


@ocr_module.route("/ocrResult")
def ocr_result() -> Response:
    global result
    if result is None:
        return jsonify({"result": "no result", "status": 1})
    if not check_plate(result.text, result.plate_type) or result.confidence < 0.9:
        return jsonify({"result": "wrong plate", "status": 1})

    return jsonify({"result": f"result:{result.text}<br>confidence:{result.confidence}", "status": 0})


def set_ocr_results(img: np.ndarray, plate_type: int) -> None:
    global result
    result = __ocr_recognize(img)
    result.plate_type = plate_type


def clear_ocr_results() -> None:
    global result
    result = None

# if __name__ == '__main__':
#     im = cv2.imread('../test/test1.png')
#     result = ocr_model.ocr(im)
#     print(result)
