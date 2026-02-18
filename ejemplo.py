import cv2 as cv

img = cv.imread("C:\\Users\\Yagoc\\OneDrive\\Imágenes\\lenovo.png")
cv.imshow("imagen", img)
cv.waitKey()
cv.destroyAllWindows()