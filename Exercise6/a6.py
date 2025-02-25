#!/usr/bin/env python3
import sys
import cv2
import os
from Exercise4.b4 import custom_closing  
from Exercise4.a4 import custom_opening   
from Exercise2.b2.b2 import compare_images  

def combined_closing_opening(img, kernel_size):
    """
    Applies closing followed by opening.
    
    Args:
        img (numpy.ndarray): Input grayscale image.
        kernel_size (int): Kernel size for operations.
        
    Returns:
        numpy.ndarray: Processed image.
    """
    return custom_opening(custom_closing(img, kernel_size), kernel_size)

def main():
    """
    Checks the idempotence of the combined operation (closing then opening).
    
    Usage:
      python exercise_06a.py <i> <input_image> <output_text_file>
      
      where:
       - <i> is an integer such that kernel size = 2*i + 1.
       - <input_image> is the path to the input PGM image.
       - <output_text_file> is the path to the text file where the result will be written.
       
    If no arguments are provided, default values are used:
      - i: 1         (kernel size becomes 3)
      - input_image: ./src/immed_gray_inv_20051123_clo2ope2.pgm
      - output_text_file: ./output/exercise_06a_result.txt
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) == 1:
        i = 1
        input_image_path = os.path.join(script_dir, "src", "immed_gray_inv_20051123_clo2ope2.pgm")
        output_text_path = os.path.join(script_dir, "output", "exercise_06a_result.txt")
        print("No arguments provided. Using default values:")
        print("  i:", i, "-> kernel size =", 2 * i + 1)
        print("  Input image:", input_image_path)
        print("  Output text file:", output_text_path)
    elif len(sys.argv) < 4:
        print("Usage: python exercise_06a.py <i> <input_image> <output_text_file>")
        sys.exit(1)
    else:
        i = int(sys.argv[1])
        input_image_path = sys.argv[2]
        output_text_path = sys.argv[3]
    
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: could not load image {input_image_path}")
        sys.exit(1)
    
    kernel_size = 2 * i + 1

    result_once = combined_closing_opening(img, kernel_size)
    result_twice = combined_closing_opening(result_once, kernel_size)

    output_img1 = os.path.join(script_dir, "output", "exercise_06a_output_01.pgm")
    output_img2 = os.path.join(script_dir, "output", "exercise_06a_output_02.pgm")
    os.makedirs(os.path.dirname(output_img1), exist_ok=True)
    cv2.imwrite(output_img1, result_once)
    cv2.imwrite(output_img2, result_twice)

    # Compare the two results.
    identical = compare_images(output_img1, output_img2)

    with open(output_text_path, "w") as f:
        f.write(f"Combined operation (closing then opening) is idempotent: {identical}\n")

    print(f"Comparison result saved in {output_text_path}")
    print("Combined operation (closing then opening) is idempotent:", identical)
    return identical

if __name__ == "__main__":
    main()
