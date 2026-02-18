import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
ret, img = cap.read()
x, y, z = img.shape
fondo = np.zeros((x, y), np.uint8)

while True:
    ret, img = cap.read()
    if(ret):
        r,g,b=cv.split(img)
        cv.imshow("Videor", r)
        cv.imshow("Videog", g)
        cv.imshow("Videob", b)
        cv.imshow("Video", img)
    else:
        print("No me pude conectar a la cámara")
        break
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()