import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Change colorspace to HSV to make thresholding easier
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold for red (the color of my red composition book)
    mask = cv2.inRange(hsv, np.array([0, 100, 0]), np.array([15, 200, 255]))

    # Display the resulting thresholded image
    cv2.imshow('frame', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
