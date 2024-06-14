from flask import Blueprint, jsonify, Response
import cv2
import hyperlpr3 as lpr3
import numpy as np

ocr_module = Blueprint('ocr_module', __name__)

cather = lpr3.LicensePlateCatcher()


class OCRResult:
    plate_name = {
        0: "蓝色普通车牌",
        1: "黄色普通车牌",
        2: "新能源车牌（绿色）",
        3: "白色警用车牌",
        4: "其他特殊车牌"
    }

    def __init__(self, text, confidence, plate_type, bounding_box) -> None:
        self.text = str(text)
        self.confidence = float(confidence)
        self.plate_type = int(plate_type)
        self.bounding_box = [
            {"lt": [int(bounding_box[0]), int(bounding_box[1])]},
            {"rb": [int(bounding_box[2]), int(bounding_box[3])]},
        ]

    def __repr__(self) -> str:
        return (f"OCRResult(bounding_box={self.bounding_box}, text='{self.text}',"
                f" confidence={self.confidence}, type={OCRResult.plate_name[self.plate_type]})")

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "type": OCRResult.plate_name[self.plate_type],
            "bounding_box": self.bounding_box,
        }


def __ocr_detect(img: np.array) -> list[OCRResult]:
    results = cather(img)
    ocr_results = [OCRResult(text, confidence, plate_type, bounding_box)
                   for text, confidence, plate_type, bounding_box in results]
    return ocr_results


@ocr_module.route('/ocrTest')
def ocr_test() -> Response:
    ocr_objs = []
    for i in range(1, 7):
        image = "test/test" + str(i) + ".png"
        img = cv2.imread(image)
        ocr_objs += __ocr_detect(img)
    return jsonify([obj.to_dict() for obj in ocr_objs])


@ocr_module.route("/ocrResult")
def ocr_result() -> Response:
    return jsonify({
        "result": "test context"
    })
