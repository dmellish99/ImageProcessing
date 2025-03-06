import numpy as np
import cv2 as cv

# Load images
img = cv.imread('src/coffee_grains.jpg')  # Ensure it loads correctly
markers = cv.imread('src/coffee_markers.png', cv.IMREAD_GRAYSCALE)  # Grayscale for markers

# Debugging: Check if images are loaded
if img is None:
    raise ValueError("Error: Could not load src/coffee_grains.png")
if markers is None:
    raise ValueError("Error: Could not load src/coffee_markers.png")

# Convert grayscale to BGR (if necessary)
if len(img.shape) == 2:  # If it's grayscale
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

# Convert markers to int32
markers = np.int32(markers)

# Ensure shapes match
if markers.shape != img.shape[:2]:
    raise ValueError(f"Error: Shape mismatch! img shape: {img.shape[:2]}, markers shape: {markers.shape}")

# Apply watershed
cv.watershed(img, markers)

# Convert markers back to uint8 for visualization
output = np.uint8(markers)

# Save result
cv.imwrite('output/test_image.png', output)

print("Watershed applied successfully!")
