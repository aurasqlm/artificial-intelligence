import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    if not ret:
        break
    display_frame = frame.copy()
    cv2.putText(display_frame,"Press Space Button to Capture Your WebCam",(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
    cv2.putText(display_frame,"Press Escape Button to Exit",(20,80),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)

    cv2.imshow("Camera",display_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 32:
        filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpeg"
        cv2.imwrite(filename,frame)
        print(f"Saved {filename}")
    elif key == 27:
        break



cap.release()
cv2.destroyAllWindows()