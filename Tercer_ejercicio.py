import cv2 as cv
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    cv.imshow("Video", img)
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()