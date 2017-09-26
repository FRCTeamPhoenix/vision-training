import cv2
import numpy as np

# Load target sample image
frame = cv2.imread('target_sample.png')

# Change colorspace to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Threshold for the green of the target
mask = cv2.inRange(hsv, np.array([50, 100, 75]), np.array([80, 255, 255]))

# Retrieve a list of contours out of the image
# Each contour is a list of points, and each list of points forms a complete polygon
contours, _ = cv2.findContours(mask, 1, 2)

# Sort the contours by area (so the largest area shapes are first)
def greater(a, b):
    area1 = cv2.contourArea(a)
    area2 = cv2.contourArea(b)
    if area1 > area2:
        return -1
    return 1
contours.sort(greater)

# The target should be the two largest contours in the image, lets concatenate them together
target = np.concatenate((contours[0], contours[1]))

# We'll then find the smallest convex shape that fits around these contours. This should be a rectangle
target = cv2.convexHull(target)


# Approximate a polygon around the shape we just found. This isn't an exact operation, so it should reduce the number of
# sides on our shape to 4 in order to make the desired rectangle.
# e is the maximum distance between the original curve and the estimation, basically the accuracy of the polygon fit
# Increasing the constant from 0.1 will make it less accurate (less sides), a decreasing will make it more accurate (more sides)
e = 0.1 * cv2.arcLength(target, True)
target = cv2.approxPolyDP(target, e, True)

# Draw the rectangle on the original image
cv2.drawContours(frame, [target], -1, (0, 255, 0), 3)

# Display the resulting thresholded image
cv2.imshow('frame', frame)

# Wait for user input before closing window
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
