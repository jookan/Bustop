import cv2
import numpy as np
import serial
import time

# 설정값: 임계값 및 최소/최대 컨투어 면적
THRESHOLD = 30
MIN_AREA = 1000  # 최소 컨투어 면적
MAX_AREA = 5000  # 최대 컨투어 면적

# Arduino와의 시리얼 통신 설정
ser = serial.Serial('COM6', 9600)  # COM 포트는 아두이노 연결 포트로 변경
time.sleep(2)  # 초기 연결 대기 시간

# 배경 제거 알고리즘 초기화
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)

def preprocess_frame(frame):
    """프레임을 그레이스케일로 변환하고 히스토그램 정규화."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 전처리
        preprocessed_frame = preprocess_frame(frame)

        # 배경 제거 및 차이 계산
        fg_mask = bg_subtractor.apply(preprocessed_frame)
        _, fg_mask = cv2.threshold(fg_mask, THRESHOLD, 255, cv2.THRESH_BINARY)

        # 노이즈 제거
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # 컨투어 탐지
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        draw_frame = frame.copy()

        object_detected = False
        for contour in contours:
            area = cv2.contourArea(contour)
            if MIN_AREA < area < MAX_AREA:  # 면적 조건 필터링
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(draw_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                object_detected = True

        if object_detected:
            print("움직임 감지됨, '1' 전송")
            ser.write(b'1')
            time.sleep(0.1)
        else:
            print("움직임 감지되지 않음, '0' 전송")
            ser.write(b'0')
            time.sleep(0.1)

        # 결과 시각화
        stacked = np.hstack((draw_frame, cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR)))
        cv2.imshow('Motion Detection', stacked)

        # ESC 키로 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    ser.close()  # 시리얼 포트 닫기
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
