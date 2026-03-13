import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    raise SystemExit

current_mode = 'original'
gaussian_kernel = 9
median_kernel = 9
bilateral_d = 9
box_kernel = 9
threshold_value = 127
sharpen_strength = 1.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output = frame.copy()

    if current_mode == 'laplacian':
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        output = cv2.cvtColor(np.uint8(np.absolute(lap)), cv2.COLOR_GRAY2BGR)

    elif current_mode == 'sobel':
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.magnitude(sx, sy)
        output = cv2.cvtColor(np.uint8(np.absolute(sobel)), cv2.COLOR_GRAY2BGR)

    elif current_mode == 'canny':
        edges = cv2.Canny(gray, 80, 160)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif current_mode == 'gaussian':
        if gaussian_kernel % 2 == 0:
            gaussian_kernel += 1
        output = cv2.GaussianBlur(frame, (gaussian_kernel, gaussian_kernel), 2)

    elif current_mode == 'median':
        if median_kernel % 2 == 0:
            median_kernel += 1
        output = cv2.medianBlur(frame, median_kernel)

    elif current_mode == 'bilateral':
        output = cv2.bilateralFilter(frame, bilateral_d, 75, 75)

    elif current_mode == 'boxblur':
        if box_kernel % 2 == 0:
            box_kernel += 1
        output = cv2.blur(frame, (box_kernel, box_kernel))

    elif current_mode == 'threshold':
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        output = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    elif current_mode == 'adaptive':
        adaptive = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        output = cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)

    elif current_mode == 'sharpen':
        kernel = np.array([
            [0, -1, 0],
            [-1, 5 + sharpen_strength, -1],
            [0, -1, 0]
        ], dtype=np.float32)
        output = cv2.filter2D(frame, -1, kernel)

    cv2.putText(output, f"Mode: {current_mode}", (10, 35),
                cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 255), 2)

    cv2.putText(output, "o original", (10, 70),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "l laplacian", (10, 95),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "s sobel", (10, 120),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "c canny", (10, 145),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "g gaussian", (10, 170),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "m median", (10, 195),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "b bilateral", (10, 220),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "x boxblur", (10, 245),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "t threshold", (10, 270),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "a adaptive", (10, 295),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "h sharpen", (10, 320),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (255, 255, 255), 1)
    cv2.putText(output, "q quit", (10, 345),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 200, 255), 1)

    if current_mode == 'gaussian':
        cv2.putText(output, f"+ / - kernel: {gaussian_kernel}", (10, 375),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 255, 0), 1)

    elif current_mode == 'median':
        cv2.putText(output, f"] / [ kernel: {median_kernel}", (10, 375),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 255, 0), 1)

    elif current_mode == 'bilateral':
        cv2.putText(output, f"= / - diameter: {bilateral_d}", (10, 375),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 255, 0), 1)

    elif current_mode == 'boxblur':
        cv2.putText(output, f"p / i kernel: {box_kernel}", (10, 375),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 255, 0), 1)

    elif current_mode == 'threshold':
        cv2.putText(output, f"8 / 2 threshold: {threshold_value}", (10, 375),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 255, 0), 1)

    elif current_mode == 'sharpen':
        cv2.putText(output, f"6 / 4 sharpen: {sharpen_strength:.1f}", (10, 375),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 255, 0), 1)

    cv2.imshow("Advance Edge Detection System", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('o'):
        current_mode = 'original'

    elif key == ord('l'):
        current_mode = 'laplacian'

    elif key == ord('s'):
        current_mode = 'sobel'

    elif key == ord('c'):
        current_mode = 'canny'

    elif key == ord('g'):
        current_mode = 'gaussian'

    elif key == ord('m'):
        current_mode = 'median'

    elif key == ord('b'):
        current_mode = 'bilateral'

    elif key == ord('x'):
        current_mode = 'boxblur'

    elif key == ord('t'):
        current_mode = 'threshold'

    elif key == ord('a'):
        current_mode = 'adaptive'

    elif key == ord('h'):
        current_mode = 'sharpen'

    elif key == ord('+') and current_mode == 'gaussian':
        gaussian_kernel = min(51, gaussian_kernel + 2)

    elif key == ord('-') and current_mode == 'gaussian':
        gaussian_kernel = max(3, gaussian_kernel - 2)

    elif key == ord(']') and current_mode == 'median':
        median_kernel = min(51, median_kernel + 2)

    elif key == ord('[') and current_mode == 'median':
        median_kernel = max(3, median_kernel - 2)

    elif key == ord('=') and current_mode == 'bilateral':
        bilateral_d = min(25, bilateral_d + 2)

    elif key == ord('-') and current_mode == 'bilateral':
        bilateral_d = max(3, bilateral_d - 2)

    elif key == ord('p') and current_mode == 'boxblur':
        box_kernel = min(51, box_kernel + 2)

    elif key == ord('i') and current_mode == 'boxblur':
        box_kernel = max(3, box_kernel - 2)

    elif key == ord('8') and current_mode == 'threshold':
        threshold_value = min(255, threshold_value + 5)

    elif key == ord('2') and current_mode == 'threshold':
        threshold_value = max(0, threshold_value - 5)

    elif key == ord('6') and current_mode == 'sharpen':
        sharpen_strength = min(5.0, sharpen_strength + 0.2)

    elif key == ord('4') and current_mode == 'sharpen':
        sharpen_strength = max(0.0, sharpen_strength - 0.2)

cap.release()
cv2.destroyAllWindows()
