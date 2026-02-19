import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)

recording = False
mirror = False
out = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if mirror:
        frame = cv2.flip(frame, 1)

    display = frame.copy()

    cv2.putText(display, "SPACE=Photo  R=Record  M=Mirror  ESC=Exit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    if recording:
        out.write(frame)
        cv2.putText(display, "REC...", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow("AuraCam+", display)

    key = cv2.waitKey(1) & 0xFF

    if key == 32:  # Photo
        name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        cv2.imwrite(name, frame)
        print("Saved:", name)

    elif key == ord('r'):  # Record toggle
        recording = not recording
        if recording:
            name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".avi"
            out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'XVID'), 20, (frame.shape[1], frame.shape[0]))
            print("Recording started")
        else:
            out.release()
            print("Recording stopped")

    elif key == ord('m'):  # Mirror toggle
        mirror = not mirror

    elif key == 27:
        break

cap.release()
if out:
    out.release()
cv2.destroyAllWindows()