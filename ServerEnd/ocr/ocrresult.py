class OCRResult:

    def __init__(self, text, confidence, plate_type=-1) -> None:
        self.text = str(text)
        self.confidence = float(confidence)
        self.plate_type = plate_type

    def __repr__(self) -> str:
        return (f"OCRResult(text='{self.text}',"
                f" confidence={self.confidence})")

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "confidence": self.confidence,
        }
