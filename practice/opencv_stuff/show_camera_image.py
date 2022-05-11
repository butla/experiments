"""
Show camera output and save a photo when quitting.
"""

import cv2

cap = cv2.VideoCapture(0)

while(True):
    _, frame = cap.read()

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('fota.jpg', frame)
        break

cap.release()
cv2.destroyAllWindows()

