import cv2
import numpy as np

pic1 = cv2.imread('C:/Users/27165/Desktop/wh0001.png')
pic2 = cv2.imread('C:/Users/27165/Desktop/wh0019.png')
pic2 = 150 * np.ones([256, 256, 3], dtype=np.uint8)
cv2.circle(pic2, (0, 0), 10, (0, 0, 1.1), 100)
# img_add = cv2.addWeighted(pic1, 1, pic2, 0.9, 0)
img_add = cv2.multiply(pic1, pic2)
cv2.imshow('pic2', pic2)
cv2.imshow('sss', img_add)
cv2.waitKey(0)