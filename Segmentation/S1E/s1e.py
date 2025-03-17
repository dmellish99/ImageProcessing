import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# List of image files
image_files = ['src/water_coins.jpg', 'src/Lenna.png','src/plat.jpg']

# Create a figure for subplots
fig, axes = plt.subplots(len(image_files), 3, figsize=(10, 5 * len(image_files)))

for i, img_file in enumerate(image_files):
    img = cv.imread(img_file)
    assert img is not None, f"Image {img_file} not found. Please check the file path."

    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding
    _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Remove noise using morphological opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)

    # Identify sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=3)

    # Identify sure foreground area using distance transform
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    _, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    # Identify unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)

    # Marker labeling
    _, markers = cv.connectedComponents(sure_fg)

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

    # Save images
    cv.imwrite(f'output/markers_watershed_gray_{i}.png', markers_vis)
    cv.imwrite(f'output/original_image_{i}.png', cv.cvtColor(img, cv.COLOR_BGR2RGB))
    
    # Plot images in subplots
    axes[i, 0].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))  # Convert BGR to RGB for proper display
    axes[i, 0].set_title("Original Image")
    axes[i, 0].axis("off")

    axes[i, 1].imshow(thresh, cmap="gray")
    axes[i, 1].set_title("Thresholded Image")
    axes[i, 1].axis("off")

    axes[i, 2].imshow(markers_vis, cmap="ocean")
    axes[i, 2].set_title("Color Markers")
    axes[i, 2].axis("off")

plt.tight_layout()
plt.show()
