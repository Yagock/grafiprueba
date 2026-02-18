import cv2 as cv
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if(ret):
        cv.imshow("Video", img)
    else:
        print("No me pude conectar a la cámara")
        break
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()