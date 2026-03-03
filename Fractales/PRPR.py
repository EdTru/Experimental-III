import cv2
import numpy as np
AREA_BASE = 54*38 #mm²

img = cv2.imread('PapelAluminio.jpeg')
#cv2.imshow('Original', img)

#ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

#img = thresh1


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

canny = cv2.Canny(gray, 70, 500)

contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print("Number of Contours = " ,len(contours))
#cv2.imshow('Canny Edges', canny)

for i, cnt in enumerate(contours):
	M = cv2.moments(cnt)
	if M['m00'] != 0.0:
		x1 = int(M['m10']/M['m00'])
		y1 = int(M['m01']/M['m00'])
	area = cv2.contourArea(cnt)
	perimeter = cv2.arcLength(cnt, True)
	perimeter = round(perimeter, 4)
	print(f'Area of contour :', area)
	#print(f'Perimeter of contour {i+1}:', perimeter)
	img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
	cv2.putText(img, f'Area :{area}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)



cv2.imshow('Contours', img)
cv2.waitKey(0)