import cv2
import numpy as np
from yolo.settings import colors, classes, net, net_size


def draw_boxes(image, boxes, confidences, class_ids, idxs):
    for i in idxs:
        x, y, w, h = boxes[i]
        color = [int(c) for c in colors[class_ids[i]]]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        text = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image


def detect(img, width, height):
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, net_size, swapRB=True, crop=False)
    net.setInput(blob)
    # 进行前向传播，获取输出
    outputs = net.forward()

    # YOLOv5参数
    conf_threshold = 0.5
    nms_threshold = 0.4

    # 解析输出
    boxes = []
    confidences = []
    class_ids = []

    # 将需要的box提取出来
    for detection in outputs[0]:
        box_iou = detection[4]
        class_iou = detection[5:]
        for i in range(len(class_iou)):
            confidence = box_iou * class_iou[i]
            if confidence > conf_threshold:
                box = detection[0:4] * np.array(
                    [width / net_size[0], height / net_size[1], width / net_size[0], height / net_size[1]])
                (centerX, centerY, w, h) = box.astype("int")
                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(i)

    # 应用非极大值抑制
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # 绘制检测结果
    if len(idxs) > 0:
        idxs = idxs.flatten()
    return boxes, confidences, class_ids, idxs


def result_filter(confidence, size, boxes, confidences, idxs):
    if len(boxes) == 0 or len(confidences) == 0 or len(idxs) == 0:
        return -1, [], []
    max_square = 0
    max_idx = idxs[0]

    for idx in idxs:
        square = boxes[idx][2] * boxes[idx][3]

        if square > max_square:
            max_square = square
            max_idx = idx
    if confidences[max_idx] > confidence and boxes[max_idx][2] * boxes[max_idx][3] > size:
        return max_idx, boxes[max_idx], confidences[max_idx]
    return -1, [], []
