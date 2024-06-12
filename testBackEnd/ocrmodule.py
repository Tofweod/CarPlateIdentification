from init import *
from flask import jsonify
import cv2
import hyperlpr3 as lpr3


cather = lpr3.LicensePlateCatcher()


class OCRResult:
    plate_name = {
        0: "蓝色普通车牌",
        1: "黄色普通车牌",
        2: "新能源车牌（绿色）",
        3: "白色警用车牌",
        4: "其他特殊车牌"
    }

    def __init__(self, text, confidence, plate_type, bounding_box):
        self.text = str(text)
        self.confidence = float(confidence)
        self.plate_type = int(plate_type)
        self.bounding_box = [
            {"lt": [int(bounding_box[0]), int(bounding_box[1])]},
            {"rb": [int(bounding_box[2]), int(bounding_box[3])]},
        ]

    def __repr__(self):
        return (f"OCRResult(bounding_box={self.bounding_box}, text='{self.text}',"
                f" confidence={self.confidence}, type={OCRResult.plate_name[self.plate_type]})")

    def to_dict(self):
        return {
            "text": self.text,
            "confidence": self.confidence,
            "type": OCRResult.plate_name[self.plate_type],
            "bounding_box": self.bounding_box,
        }


def __ocr_detect(image):
    img = cv2.imread(image)
    results = cather(img)
    ocr_results = [OCRResult(text, confidence, plate_type, bounding_box)
                   for text, confidence, plate_type, bounding_box in results]
    return ocr_results


@app.route('/ocrTest')
def ocr_test():
    ocr_objs = []
    for i in range(1, 7):
        img = "test/test" + str(i) + ".png"
        ocr_objs += __ocr_detect(img)
    return jsonify([obj.to_dict() for obj in ocr_objs])


@app.route("/ocrResult")
def ocr_result():
    return jsonify({
        "result": "test context"
    })
