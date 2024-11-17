import cv2
import numpy as np
#import serial
import time

# 설정값: 임계값과 최대 차이 픽셀 수 설정
THRESHOLD = 50
MAX_DIFF = 5

# Arduino와의 시리얼 통신 설정
#ser = serial.Serial('COM6', 9600)  # COM 포트는 아두이노 연결 포트로 변경
time.sleep(2)  # 아두이노와의 초기 연결 대기 시간


def preprocess_frame(frame):
    """프레임을 그레이스케일로 변환합니다."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def compute_difference(frame1, frame2):
    """두 프레임의 차이를 이진화하여 반환합니다."""
    diff = cv2.absdiff(frame1, frame2)
    _, diff_thresh = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)
    return diff_thresh


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    ret, frame_a = cap.read()
    ret, frame_b = cap.read()

    while ret:
        ret, frame_c = cap.read()
        if not ret:
            break

        # 각 프레임을 그레이스케일로 변환
        gray_a, gray_b, gray_c = map(preprocess_frame, [frame_a, frame_b, frame_c])

        # 두 차이 이미지를 이진화한 후 AND 연산으로 변화 영역 추출
        diff = cv2.bitwise_and(compute_difference(gray_a, gray_b), compute_difference(gray_b, gray_c))

        # 노이즈 제거
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)

        # 변화가 있는 경우 그 영역을 사각형으로 표시
        diff_cnt = cv2.countNonZero(diff)
        draw_frame = frame_c.copy()

        # 변화 감지 및 컨투어 찾기
        if diff_cnt > MAX_DIFF:
            contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) < 100:  # 너무 작은 움직임은 무시
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(draw_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("움직임 감지됨, '1' 전송")
            #ser.write(b'1')  # Arduino에 '1' 전송
        else:
            print("움직임 감지되지 않음, '0' 전송")
            #ser.write(b'0')

        # 원본 이미지와 변화 영역을 함께 출력
        stacked = np.hstack((draw_frame, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        cv2.imshow('motion', stacked)

        # 프레임 이동
        frame_a, frame_b = frame_b, frame_c

        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키로 종료
            break

    cap.release()
    #ser.close()  # 시리얼 포트 닫기
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
