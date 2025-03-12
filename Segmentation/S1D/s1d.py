import numpy as np
import cv2 as cv

import matplotlib.pyplot as plt

# Load the image
img = cv.imread('src/coffee_grains.jpg')
assert img is not None, "Image not found. Please check the file path."

# Convert to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Apply Otsu's thresholding
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)


# Remove noise using morphological opening
kernel = np.ones((3, 3), np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)

# Identify sure background area
sure_bg = cv.dilate(opening, kernel, iterations=3)



# Identify sure foreground area using distance transform
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

# Identify unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)

cv.imwrite('output/sure_fg.png',sure_fg)
cv.imwrite('output/sure_bg.png',sure_bg)

# Marker labeling
ret, markers = cv.connectedComponents(sure_fg)

# Add one to all labels so that background is not zero
markers = markers + 1

# Mark the unknown region with zero
markers[unknown == 255] = 0

# Apply watershed algorithm
markers = cv.watershed(img, markers)
img[markers == -1] = [0, 0, 255]  # Mark watershed boundaries in red

# Normalize markers to 8-bit grayscale for better visualization
markers_vis = cv.normalize(markers, None, 0, 255, cv.NORM_MINMAX)
markers_vis = np.uint8(markers_vis)


cv.imwrite('output/markers_watershed_coffee_grains.png',markers)
cv.imwrite('output/markers_watershed_coffee_grains_grayscale.png',markers_vis)

# # Display results
cv.imshow('Original Image', img)
cv.imshow('Thresholded Image', thresh)
cv.imshow('Grayscale Markers', markers_vis)
cv.waitKey(0)
cv.destroyAllWindows()
