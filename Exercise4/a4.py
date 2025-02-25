#!/usr/bin/env python3
import sys
import cv2
import os
from Exercise3.a3 import custom_erosion
from Exercise3.b3 import custom_dilation

def custom_opening(img, kernel_size):
    """
    Perform morphological opening on a grayscale image.
    Opening is defined as erosion followed by dilation.
    
    Args:
        img (numpy.ndarray): Grayscale image.
        kernel_size (int): Size of the square kernel.
    
    Returns:
        numpy.ndarray: Image after opening.
    """
    return custom_dilation(custom_erosion(img, kernel_size), kernel_size)

def run():
    """
    Main function for morphological opening (Exercise 04a).
    
    Usage:
      python exercise_04a.py <kernel_parameter> <input_image> <output_image>
    where:
      - <kernel_parameter> is an integer i, so that kernel size = 2*i + 1.
      - <input_image> is the path to the input PGM image.
      - <output_image> is the path where the result will be saved.
    
    Defaults (if no arguments provided):
      kernel_parameter: 1           (kernel size becomes 3)
      input_image:      ./src/immed_gray_inv.pgm
      output_image:     ./output/immed_gray_inv_ope.pgm
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Default values
    default_kernel_param = 1
    default_input = os.path.join(script_dir, "src", "immed_gray_inv.pgm")
    default_output = os.path.join(script_dir, "output", "immed_gray_inv_ope.pgm")
    
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
        print("Usage: python exercise_04a.py <kernel_parameter> <input_image> <output_image>")
        sys.exit(1)
    
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: could not read image '{input_image_path}'")
        sys.exit(1)
    
    kernel_size = 2 * kernel_param + 1
    opened_img = custom_opening(img, kernel_size)
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    cv2.imwrite(output_image_path, opened_img)
    print(f"Opening applied with a {kernel_size}x{kernel_size} kernel.")
    print("Output image saved to:", output_image_path)
    return opened_img

if __name__ == "__main__":
    run()
