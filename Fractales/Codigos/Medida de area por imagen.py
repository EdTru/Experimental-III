import cv2
import numpy as np

img1 = cv2.imread("P5.jpeg")
img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(img,80,400,0)
contours,hierarchy = cv2.findContours(thresh, 2, 2)
print("Number of contours in image:",len(contours))

for i, cnt in enumerate(contours):
   M = cv2.moments(cnt)
   if M['m00'] != 0.0:
      x1 = int(M['m10']/M['m00'])
      y1 = int(M['m01']/M['m00'])
   area = cv2.contourArea(cnt)
   perimeter = cv2.arcLength(cnt, True)
   perimeter = round(perimeter, 4)
   print(f'Area of contour {i+1}:', area)
   print(f'Perimeter of contour {i+1}:', perimeter)
   img1 = cv2.drawContours(img1, [cnt], -1, (0,255,255), 3)
   cv2.putText(img1, f'Area :{area}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
   cv2.putText(img1, f'Perimeter :{perimeter}', (x1, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

cv2.imshow("Image", img1)
cv2.waitKey(0)
cv2.destroyAllWindows()