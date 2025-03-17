import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# List of image and marker files
image_files = ['src/coffee_grains.jpg']
marker_files = ['src/coffee_markers.png']  # Marker images
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


# Create a figure for subplots
fig, axes = plt.subplots(len(image_files), 3, figsize=(10, 5 * len(image_files)))

for i, (img_file, marker_file) in enumerate(zip(image_files, marker_files)):
    img = cv.imread(img_file)
    marker_img = cv.imread(marker_file, cv.IMREAD_GRAYSCALE)  # Load marker as grayscale
    
    assert img is not None, f"Image {img_file} not found."
    assert marker_img is not None, f"Marker image {marker_file} not found."

    # Ensure marker image matches input image size
    marker_img = cv.resize(marker_img, (img.shape[1], img.shape[0]), interpolation=cv.INTER_NEAREST)
    
    # marker_img=cv.cvtColor(marker_img, cv.COLOR_BGR2GRAY)

    marker_img_inv=255-marker_img


    ## Apply dilation 
    kernel = np.ones((3, 3), np.uint8)

    opening = cv.dilate(marker_img_inv, kernel, iterations=6)

   
    # # Apply Otsu's thresholding
    # ret, thresh = cv.threshold(marker_img_inv, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)


    # Remove noise using morphological opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(opening, cv.MORPH_OPEN, kernel, iterations=2)

    # Identify sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=3)

    # # Identify sure foreground area using distance transform
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)


    # Identify unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)


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
    cv.imwrite('output/coffee_grains_w_outline.png',img)



#     # Plot images in subplots
#     axes[i, 0].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))  # Convert BGR to RGB
#     axes[i, 0].set_title("Original Image")
#     axes[i, 0].axis("off")

#     axes[i, 1].imshow(marker_img, cmap="gray")  # Show the loaded marker image
#     axes[i, 1].set_title("Loaded Marker Image")
#     axes[i, 1].axis("off")

#     axes[i, 2].imshow(cv.cvtColor(overlay, cv.COLOR_BGR2RGB))  # Show outlined coffee grains
#     axes[i, 2].set_title("Outlined Coffee Grains")
#     axes[i, 2].axis("off")

# plt.tight_layout()
# plt.show()
