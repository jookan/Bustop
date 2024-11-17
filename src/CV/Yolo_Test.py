import cv2
import numpy as np
import serial
import time
import sqlite3

from Bustop.src.sqlite3.manage_DB import update_score

# Yolo 모델 초기화
net = cv2.dnn.readNet("yolov2-tiny.weights", "yolov2-tiny.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getUnconnectedOutLayersNames()
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# 설정값: 임계값과 최대 차이 픽셀 수 설정
THRESHOLD = 50
MAX_DIFF = 10
NO_MOTION_DELAY = 1.5  # 움직임이 없을 때 초록불로 바뀌는 딜레이 (초 단위)

# Arduino와의 시리얼 통신 설정
ser = serial.Serial('COM6', 9600)
time.sleep(2)

# 전역 변수
last_motion_time = time.time()
motion_detected = False

def preprocess_frame(frame):
    """프레임을 그레이스케일로 변환합니다."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def compute_difference(frame1, frame2):
    """두 프레임의 차이를 이진화하여 반환합니다."""
    diff = cv2.absdiff(frame1, frame2)
    _, diff_thresh = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)
    return diff_thresh

def detect_objects(frame):
    """Yolo 모델을 사용하여 객체를 감지합니다."""
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    return class_ids, confidences, boxes, indexes

def main():
    global last_motion_time, motion_detected

    DB = "bus_database.db"
    con = sqlite3.connect(DB)
    cur = con.cursor()
    driver_name = "이주환"

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    ret, frame_a = cap.read()
    ret, frame_b = cap.read()

    count = 0

    while ret:
        ret, frame_c = cap.read()
        if not ret:
            break

        gray_a, gray_b, gray_c = map(preprocess_frame, [frame_a, frame_b, frame_c])

        # 두 차이 이미지를 이진화한 후 AND 연산으로 변화 영역 추출
        diff_ab = compute_difference(gray_a, gray_b)
        diff_bc = compute_difference(gray_b, gray_c)
        diff = cv2.bitwise_and(diff_ab, diff_bc)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)

        diff_cnt = cv2.countNonZero(diff)
        draw_frame = frame_c.copy()

        current_time = time.time()

        # Yolo 객체 감지 실행
        class_ids, confidences, boxes, indexes = detect_objects(draw_frame)

        # Yolo 결과를 프레임에 표시
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(draw_frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(draw_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 움직임 감지 여부에 따라 Arduino로 신호 전송 및 DB 점수 업데이트
        if diff_cnt > MAX_DIFF:
            last_motion_time = current_time
            motion_detected = True
            ser.write(b'1')
            if ser.in_waiting > 0 :
                get_data = ser.readline()
                if get_data :
                    count += 0.2
                    print("엑셀 밟음")
            time.sleep(0.05)

        else:
            if (current_time - last_motion_time) > NO_MOTION_DELAY and motion_detected:
                ser.write(b'0')
                motion_detected = False
                time.sleep(0.05)

        stacked = np.hstack((draw_frame, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        cv2.imshow('motion', stacked)

        frame_a, frame_b = frame_b, frame_c

        if cv2.waitKey(1) & 0xFF == 27:
            break

    update_score(con, cur, driver_name, count)
    con.close()
    cap.release()
    ser.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
