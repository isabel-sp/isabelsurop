import numpy as np
import matplotlib.pyplot as plt
import cv2


img_raw = cv2.imread('3clicked.png')
img_raw = cv2.resize(img_raw, (1440, 1080))
cv2.imwrite('test_14401080.png', img_raw)