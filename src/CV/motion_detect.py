import cv2
import numpy as np

# 설정값: 임계값과 최대 차이 픽셀 수 설정
THRESHOLD = 40
MAX_DIFF = 5

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
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)

        # 변화가 있는 경우 그 영역을 사각형으로 표시
        diff_cnt = cv2.countNonZero(diff)
        draw_frame = frame_c.copy()
        if diff_cnt > MAX_DIFF:
            nzero = np.nonzero(diff)
            cv2.rectangle(draw_frame, (min(nzero[1]), min(nzero[0]), max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)
            print(1)

        # 원본 이미지와 변화 영역을 함께 출력
        stacked = np.hstack((draw_frame, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        cv2.imshow('motion', stacked)

        # 프레임 이동
        frame_a, frame_b = frame_b, frame_c

        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키로 종료
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
