import cv2.dnn
import numpy as np

# 初始化颜色和类别名
colors = np.array([
    [255, 0, 0],
    [0, 255, 0]
])

classes = ['blue_plate', 'green_plate']

net = cv2.dnn.readNetFromONNX('yolo/best.onnx')

net_size = (640, 640)