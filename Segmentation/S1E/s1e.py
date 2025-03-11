import numpy as np
import cv2
from matplotlib import pyplot as plt


## Found from 

img = cv2.imread('src/water_coins.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


out=np.zeros((img.shape[0],img.shape[1]))

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)


img[markers == -1] = [255,0,0]

for a_row in range(0,img.shape[0]):
    for a_col in range(0,img.shape[1]):
        # print(img[a_row,a_col])
        if img[a_row,a_col][0]==255:
            out[a_row,a_col]=255


markers=out


print(markers)




## Apply new markers file to Lenna.png and plat.jpg


img=cv2.imread('src/Lenna.png')

print(img)

# Get dimensions
h1, w1 = markers.shape[:2]
h2, w2 = img.shape[:2]


# Determine the larger image
target_width = max(w1, w2)
target_height = max(h1, h2)

assert img is not None, "Error: Image 'Lenna.png' could not be read. Check the file path."
assert markers is not None, "Error: Image 'Lenna.png' could not be read. Check the file path."

print(f"Markers shape: {markers.shape}")
print(f"Image shape: {img.shape}")

print(f"Unique values in markers: {np.unique(markers)}")



markers=np.float32(markers)
img = np.uint8(img)


# Resize both images to the larger dimensions
resized_img1 = cv2.resize(markers, (target_width, target_height), interpolation = cv2.INTER_LINEAR)

resized_img1=np.int32(resized_img1)

resized_img2 = cv2.resize(img, (target_width, target_height), interpolation = cv2.INTER_LINEAR)


watershed=cv2.watershed(resized_img2,resized_img1)
cv2.imwrite('output/watershed_test_1.png',watershed)


img=cv2.imread('src/plat.jpg')


# Get dimensions
h1, w1 = markers.shape[:2]
h2, w2 = img.shape[:2]

# Determine the larger image
target_width = max(w1, w2)
target_height = max(h1, h2)


markers=np.float32(markers)
img = np.uint8(img)

# Resize both images to the larger dimensions
resized_img1 = cv2.resize(markers, (target_width, target_height))

resized_img1=np.int32(resized_img1)


resized_img2 = cv2.resize(img, (target_width, target_height))

watershed=cv2.watershed(resized_img2,resized_img1)

cv2.imwrite('output/watershed_test_2.png',watershed)


