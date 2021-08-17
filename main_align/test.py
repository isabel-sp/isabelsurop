import cv2
import numpy as np

def convert_bw_green(img):
    coefficients = [0,1,0]
    # for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
    m = np.array(coefficients).reshape((1,3))
    return cv2.transform(img, m)

def convert_more_green(img):
    coefficients = [-0.2,1.4,-0.2]
    # for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
    m = np.array(coefficients).reshape((1,3))
    return cv2.transform(img, m)

def convert_bw(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def convert_img(img, b, g, r):
    coefficients = [b,g,r]
    # for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
    m = np.array(coefficients).reshape((1,3))
    return cv2.transform(img, m)


im = cv2.imread('08_17_15_07_32.png')

cv2.imshow('image', im)
cv2.imshow('0.114, 0.587, 0.299', convert_img(im, 0.114, 0.587, 0.299))
cv2.imshow('0, 1, 0', convert_img(im, 0, 1, 0))
cv2.imshow('-2, 4, -2', convert_img(im, -2, 4, -2))
cv2.imshow('-1, 4, -3', convert_img(im, -1, 4, -3))
cv2.imshow('-0.2, 1.4, -0.2', convert_img(im, -0.2, 1.4, -0.2))


cv2.waitKey(0)
cv2.destroyAllWindows()