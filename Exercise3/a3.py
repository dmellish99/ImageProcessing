#!/usr/bin/env python3
import sys
import cv2
import numpy as np
import os

def custom_erosion(img, kernel_size):
    """
    Perform morphological erosion on a grayscale image.

    Args:
        img (numpy.ndarray): Grayscale image.
        kernel_size (int): Size of the square kernel (should be odd).

    Returns:
        numpy.ndarray: Eroded image.
    """
    h, w = img.shape
    pad = kernel_size // 2
    out = np.zeros_like(img)

    for y in range(h):
        for x in range(w):
            # Define the neighborhood bounds considering image limits.
            y_start = max(0, y - pad)
            y_end = min(h, y + pad + 1)
            x_start = max(0, x - pad)
            x_end = min(w, x + pad + 1)

            # Extract the valid neighborhood region.
            roi = img[y_start:y_end, x_start:x_end]

            # Assign the minimum value found in the region.
            out[y, x] = np.min(roi)

    return out



def run():
    """
    Main function for Exercise 03a (Erosion).

    Usage:
      python exercise_03a.py <kernel_parameter> <input_image> <output_image>
    where:
      - <kernel_parameter> is an integer 'i' such that kernel size = 2*i + 1.
      - <input_image> is the path to the input PGM image.
      - <output_image> is the path where the output will be saved.

    If no arguments are provided, default values are used:
      kernel_parameter: 1         (kernel size becomes 3)
      input_image:      ./src/immed_gray_inv.pgm
      output_image:     ./output/immed_gray_inv_ero.pgm
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Default values.
    default_kernel_param = 1
    default_input = os.path.join(script_dir, "src", "immed_gray_inv.pgm")
    default_output = os.path.join(script_dir, "output", "immed_gray_inv_ero.pgm")

    if len(sys.argv) == 1:
        kernel_param = default_kernel_param
        input_image_path = default_input
        output_image_path = default_output
        print("No arguments provided. Using default values:")
        print("  Kernel parameter (i):", kernel_param, "-> kernel size =", 2 * kernel_param + 1)
        print("  Input image:", input_image_path)
        print("  Output image:", output_image_path)
    elif len(sys.argv) == 4:
        try:
            kernel_param = int(sys.argv[1])
        except ValueError:
            print("Kernel parameter must be an integer.")
            sys.exit(1)
        input_image_path = sys.argv[2]
        output_image_path = sys.argv[3]
    else:
        print("Usage: python exercise_03a.py <kernel_parameter> <input_image> <output_image>")
        sys.exit(1)

    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: could not read image '{input_image_path}'")
        sys.exit(1)

    kernel_size = 2 * kernel_param + 1

    # Perform erosion.
    eroded_img = custom_erosion(img, kernel_size)
    print(f"Erosion applied with a {kernel_size}x{kernel_size} kernel.")

    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

    cv2.imwrite(output_image_path, eroded_img)
    print("Output image saved to:", output_image_path)
    return eroded_img

if __name__ == "__main__":
    run()
