import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


## Found from 

img = cv.imread('src/water_coins.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)


out=np.zeros((img.shape[0],img.shape[1]))

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv.watershed(img,markers)
img[markers == -1] = [255,0,0]

for a_row in range(0,img.shape[0]):
    for a_col in range(0,img.shape[1]):
        print(img[a_row,a_col])
        if img[a_row,a_col][0]==255:
            out[a_row,a_col]=255


markers=out
markers= np.int32(markers)




## Apply new markers file to Lenna.png and plat.jpg


img=cv.imread('src/Lenna.png')


# Get dimensions
h1, w1 = markers.shape[:2]
h2, w2 = img.shape[:2]

# Determine the larger image
target_width = max(w1, w2)
target_height = max(h1, h2)

# Resize both images to the larger dimensions
resized_img1 = cv.resize(markers, (target_width, target_height))
resized_img2 = cv.resize(img, (target_width, target_height))

watershed=cv.watershed(resized_img2,resized_img1)
cv.imwrite('output/watershed_test_1.png',watershed)


img=cv.imread('src/plat.jpg')


# Get dimensions
h1, w1 = markers.shape[:2]
h2, w2 = img.shape[:2]

# Determine the larger image
target_width = max(w1, w2)
target_height = max(h1, h2)

# Resize both images to the larger dimensions
resized_img1 = cv.resize(markers, (target_width, target_height))
resized_img2 = cv.resize(img, (target_width, target_height))

watershed=cv.watershed(resized_img2,resized_img1)

cv.imwrite('output/watershed_test_2.png',watershed)


