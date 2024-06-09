from init import *
from flask import jsonify
import cv2


class OCRResult:
    def __init__(self, bounding_box, text, confidence):
        self.bounding_box = [
            {"lt": [int(coord) for coord in bounding_box[0]]},
            {"lb": [int(coord) for coord in bounding_box[1]]},
            {"rt": [int(coord) for coord in bounding_box[2]]},
            {"rb": [int(coord) for coord in bounding_box[3]]}
        ]
        self.text = text
        self.confidence = confidence

    def __repr__(self):
        return f"OCRResult(bounding_box={self.bounding_box}, text='{self.text}', confidence={self.confidence})"

    def to_dict(self):
        return {
            "bounding_box": self.bounding_box,
            "text": self.text,
            "confidence": self.confidence
        }


# TODO:
def __ocr_detect(image):
    img = cv2.imread(image)
    result = reader.recognize(img)
    ocr_results = [OCRResult(bounding_box, text, confidence) for bounding_box, text, confidence in result]
    return ocr_results


@app.route('/ocrResult')
def ocr_result():
    ocr_objs = __ocr_detect("test1.png")
    return jsonify([obj.to_dict() for obj in ocr_objs])


if __name__ == '__main__':
    pass
