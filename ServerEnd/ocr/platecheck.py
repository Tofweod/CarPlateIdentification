province_list = [
    "皖", "沪", "津", "渝", "冀",
    "晋", "蒙", "辽", "吉", "黑",
    "苏", "浙", "京", "闽", "赣",
    "鲁", "豫", "鄂", "湘", "粤",
    "桂", "琼", "川", "贵", "云",
    "西", "陕", "甘", "青", "宁",
    "新"]

letter_list = [
    "A", "B", "C", "D", "E",
    "F", "G", "H", "J", "K",
    "L", "M", "N", "P", "Q",
    "R", "S", "T", "U", "V",
    "W", "X", "Y", "Z"]

number_list = [
    "0", "1", "2", "3", "4",
    "5", "6", "7", "8", "9"
]


def check_plate(plate_num, label):
    # wrong label
    if label == -1:
        return False
    # 确认长度
    # 蓝牌
    if label == 0:
        if len(plate_num) != 8:
            return False

    # 绿牌
    if label == 1:
        if len(plate_num) != 9:
            return False

    # 确认车牌字符是否在对应字符集里
    if plate_num[0] not in province_list:
        return False
    if plate_num[1] not in letter_list:
        return False
    # 不检查
    # if plate_num[2] != '·':
    #     return False
    car_num = plate_num[3:]
    for char_in_plate in car_num:
        if char_in_plate not in letter_list and char_in_plate not in number_list:
            return False

    return True