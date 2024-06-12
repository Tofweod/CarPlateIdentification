import cv2
import numpy as np
import config as cfg
from typing import Tuple
from collections import deque
import math


class VideoStableProbe:

    def __init__(self, cap: cv2.VideoCapture, during: float = cfg.video_during_time, threshold: float = cfg.threshold,
                 method=None):
        self.cap = cap
        self.during = during
        self.threshold = threshold
        self.method = method
        self.__deque = deque()
        self.__maxSize = math.ceil(self.during * cap.get(cv2.CAP_PROP_FPS))
        self.__prev_frame = None
        self.__cur_frame = None

    def cap_available(self):
        return self.cap.isOpened()

    @staticmethod
    def __get_gray(frame: np.ndarray):
        gaussian = cv2.GaussianBlur(frame, (5, 5), 0)
        sharpen_kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])

        sharpen = cv2.filter2D(gaussian, -1, sharpen_kernel)

        return cv2.cvtColor(sharpen, cv2.COLOR_BGR2GRAY)

    def __probe_video_stable(self) -> bool:
        if len(self.__deque) == 0:
            ret = False
            while not ret:
                ret ,frame = self.cap.read()
                self.__prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        while True:
            ret, self.__cur_frame = self.cap.read()
            if not ret:
                continue

            gray = self.__get_gray(self.__cur_frame)
            p0 = cv2.goodFeaturesToTrack(self.__prev_frame, maxCorners=100,
                                         qualityLevel=0.3,
                                         minDistance=7,
                                         blockSize=7)

            if p0 is None:
                self.__prev_frame = gray.copy()
                continue

            p1, st, err = cv2.calcOpticalFlowPyrLK(self.__prev_frame, gray, p0, None,
                                                   winSize=(15, 15),
                                                   maxLevel=2,
                                                   criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

            self.__prev_frame = gray.copy()

            if p1 is None:
                continue

            motion = p1 - p0

            abs_sum = 0
            for i in range(motion.shape[0]):
                abs_sum = abs_sum + abs(motion[i, 0, 0]) + abs(motion[i, 0, 1])
            fea_val = abs_sum / motion.shape[0]

            if len(self.__deque) > self.__maxSize:
                self.__deque.popleft()
                self.__deque.append(fea_val)
            else:
                self.__deque.append(fea_val)
                return False

            fea_period = sum(self.__deque) /len(self.__deque)
            print(fea_period,end= ' ')

            return fea_period <= self.threshold

    def __call__(self) -> Tuple[np.array, bool]:
        is_stable = self.__probe_video_stable()
        return self.__cur_frame,is_stable
