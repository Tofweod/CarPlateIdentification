import cv2
import numpy as np
import config as cfg
from typing import Tuple
from collections import deque
import math
from enum import IntEnum


class ProbeMethod(IntEnum):
    OPTIONFLOWPYRLK = 0
    FRAMEDIFF = 1

    @staticmethod
    def enum_str(val: int | str) -> str:
        try:
            int_val = int(val)
            return ProbeMethod(int_val).name
        except ValueError:
            raise ValueError(f"no enum member with value {val}")
        except TypeError:
            raise TypeError(f"no valid enum member with value {val}")


class VideoStableProbe:
    probeMethods = {
        ProbeMethod.OPTIONFLOWPYRLK: "__option_flow_pyrLK",
        ProbeMethod.FRAMEDIFF: "__frame_diff",
    }

    @staticmethod
    def calc_frame_diff(method: ProbeMethod, prev_frame: np.ndarray, curr_frame: np.ndarray) -> float | None:
        method_name = VideoStableProbe.probeMethods.get(method)
        if method_name:
            method_name = "_VideoStableProbe" + method_name
            method = getattr(VideoStableProbe, method_name, None)
            if method:
                return method(prev_frame, curr_frame)
            else:
                print("Method not found")
        else:
            print("Invalid method")

    def __init__(self, cap: cv2.VideoCapture, during: float = cfg.video_during_time, threshold: float = cfg.threshold,
                 method: ProbeMethod = ProbeMethod.FRAMEDIFF) -> None:
        self.cap = cap
        self.during = during
        self.threshold = threshold
        self.method = method
        self.stable = False
        self.__deque = deque()
        self.__maxSize = math.ceil(self.during * cap.get(cv2.CAP_PROP_FPS))
        self.__prev_frame = None
        self.__cur_frame = None
        self.__fea_listeners = []
        self.__fea_period = 0

    def __notify_fea_listeners(self) -> None:
        for listener, args, kwargs in self.__fea_listeners:
            listener(*args, **kwargs)

    def add_fea_listener(self, listener, *args, **kwargs) -> None:
        self.__fea_listeners.append((listener, args, kwargs))

    def fea_listener_size(self) -> int:
        return len(self.__fea_listeners)

    @property
    def fea_period(self) -> float:
        return self.__fea_period

    @fea_period.setter
    def fea_period(self, value) -> None:
        if value != self.fea_period:
            self.__fea_period = value
            self.__notify_fea_listeners()

    def available(self) -> bool:
        if not self.stable:
            return self.cap.isOpened()
        return False

    @staticmethod
    def _get_gauss_sharpen_gray(frame: np.ndarray) -> np.ndarray:
        gaussian = cv2.GaussianBlur(frame, (5, 5), 0)
        sharpen_kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])

        sharpen = cv2.filter2D(gaussian, -1, sharpen_kernel)

        return cv2.cvtColor(sharpen, cv2.COLOR_BGR2GRAY)

    def __probe_video_stable(self, threshold: float, method: ProbeMethod) -> bool:
        if len(self.__deque) == 0:
            ret = False
            while not ret:
                ret, frame = self.cap.read()
                self.__prev_frame = self._get_gauss_sharpen_gray(frame)

        while True:
            ret, self.__cur_frame = self.cap.read()
            if not ret:
                continue

            success, fea_val, self.__prev_frame = VideoStableProbe.calc_frame_diff(method,
                                                                                   self.__prev_frame, self.__cur_frame)

            if not success:
                continue

            if len(self.__deque) > self.__maxSize:
                self.__deque.popleft()
            self.__deque.append(fea_val)

            self.fea_period = sum(self.__deque) / len(self.__deque)
            # print(f"val:{self.fea_period},maxsize:{self.__maxSize},cursize:{len(self.__deque)}")

            return self.fea_period <= threshold and len(self.__deque) >= self.__maxSize

    @staticmethod
    def __option_flow_pyrLK(prev_frame: np.ndarray, cur_frame: np.ndarray) -> Tuple[bool, float, np.ndarray]:
        gray = VideoStableProbe._get_gauss_sharpen_gray(cur_frame)
        p0 = cv2.goodFeaturesToTrack(prev_frame, maxCorners=100,
                                     qualityLevel=0.3,
                                     minDistance=7,
                                     blockSize=7)

        if p0 is None:
            prev_frame = gray.copy()
            return False, 0, prev_frame

        next_pts = np.zeros_like(p0)
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, gray, p0, next_pts,
                                               winSize=(15, 15),
                                               maxLevel=2,
                                               criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        prev_frame = gray.copy()

        if p1 is None:
            return False, 0, prev_frame

        motion = p1 - p0

        abs_sum = 0
        for i in range(motion.shape[0]):
            abs_sum = abs_sum + abs(motion[i, 0, 0]) + abs(motion[i, 0, 1])
        fea_val = abs_sum / motion.shape[0]

        return True, fea_val, prev_frame

    @staticmethod
    def __frame_diff(prev_frame: np.ndarray, cur_frame: np.ndarray) -> Tuple[bool, float, np.ndarray]:
        gray = VideoStableProbe._get_gauss_sharpen_gray(cur_frame)
        frame_diff = np.average(cv2.absdiff(prev_frame, gray))
        prev_frame = gray.copy()
        return True, frame_diff, prev_frame

    def __call__(self) -> Tuple[np.array, bool]:
        self.stable = self.__probe_video_stable(threshold=self.threshold, method=self.method)
        return self.__cur_frame, self.stable
