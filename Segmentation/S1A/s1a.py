import cv2 
import numpy as np


img=cv2.imread('src/wheel.png',cv2.IMREAD_GRAYSCALE)


# Creating kernel 
kernel = np.ones((3, 3), np.uint8) 
  
# Using cv2.erode() method  
img_erode= cv2.erode(img, kernel)  

img_out=img-img_erode

cv2.imwrite('output/test_image.png',img_out)

