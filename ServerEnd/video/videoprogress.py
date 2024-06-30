import cv2
import numpy as np


def get_gauss_sharpen_gray(frame: np.ndarray) -> np.ndarray:
    gaussian = cv2.GaussianBlur(frame, (5, 5), 0)
    sharpen_kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])

    sharpen = cv2.filter2D(gaussian, -1, sharpen_kernel)

    return cv2.cvtColor(sharpen, cv2.COLOR_BGR2GRAY)


def progress_yolo_img(img: np.ndarray, idx: int) -> np.ndarray:
    result = img
    if idx == 0:
        gray = cv2.addWeighted(img[:, :, 1], 0.5, img[:, :, 2], 0.5, 0)
        hist = cv2.equalizeHist(gray)
        ret, result = cv2.threshold(hist, 180, 255, cv2.THRESH_TOZERO)
    elif idx == 1:
        gray = cv2.addWeighted(img[:, :, 0], 0.5, img[:, :, 2], 0.5, 0)
        hist = cv2.equalizeHist(gray)
        ret, trunc_img = cv2.threshold(hist, 150, 255, cv2.THRESH_TRUNC)
        result = cv2.medianBlur(trunc_img,3)

    return result

