import cv2 as cv
import numpy as np

img = np.ones((500,500, 3), np.uint8)*255
#cv.rectangle(img, (10,10), (200,100), (234,56,100), 2)
#cv.rectangle(img, (10,10), (200,100), (234,56,100), -1)
#cv.rectangle(img, (20,20), (210,110), (234,56,100), 2)#Suma = traslacion, multiplicación = escalado

#cv.circle(img, (255,255), 30, (23, 43, 144), -1 )
#cv.circle(img, (255,255), 12, (234, 43, 11), -1 )

#cv.line(img, (255, 255), (300, 100), (0, 255, 0), 4)

i = 1
for i in range (600):
    if 0<i<500:
        i=i*(-1)
    cv.circle(img, (i, i), 20, (255, 0, 0), -1)
    #cv.rectangle(img, (10+i, 10), (200, 100), (34, 56, 100), -1)
    cv.imshow("img", img)
    img = np.ones((500, 500, 3), np.uint8)*150
    cv.waitKey(10)

cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()