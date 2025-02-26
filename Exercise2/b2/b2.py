import cv2
import sys
import os
import numpy as np

def compare_images(image_path1, image_path2):
    """
    Reads two grayscale PGM images and compares them.
    Two images are equal if:
      - They have the same dimensions.
      - Every corresponding pixel has the same intensity.
      
    Args:
        image_path1 (str): Path to the first input PGM image.
        image_path2 (str): Path to the second input PGM image.
        
    Returns:
        bool: True if the images are equal, False otherwise.
    """
    
    ## Ingest Images from file paths
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2=cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)


    ## Check n_pixels
    if img1.size!=img2.size:
        return False
    
    are_equal=True

    ## Set dimensions
    nrows=img1.shape[0]
    ncols=img1.shape[1]
        
    ## Iterate through each row and column (each pixel)
    for row in range(0,nrows):
        for col in range(0,ncols):
            ## Set a value for the current pixel of each image
            cur_pixel_img1=img1[row,col]
            cur_pixel_img2=img2[row,col]
            ## Check for equality, and set to false if values are not equal
            if cur_pixel_img1!=cur_pixel_img2:
                are_equal=False

    return are_equal
    

def run():
    """
    Main function to compare two PGM images.
    
    Usage:
      - Without arguments, defaults are used:
          Input images:  ./src/cam_74.pgm and ./src/cam_74.pgm
          Output file:   ./output/exercise_02b_output_01.txt
      - With arguments:
          python compare_images.py <input_image1.pgm> <input_image2.pgm>
    
    The program writes 'True' to the output file if the images are equal, and 'False' otherwise,
    and returns the Boolean result.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "output", "exercise_02b_output_01.txt")
    
    if len(sys.argv) == 1:
        input_file1 = os.path.join(script_dir, "src", "cam_74.pgm")
        input_file2 = os.path.join(script_dir, "src", "cam_74.pgm")
        print("No arguments provided. Using default values:")
        print("  Input image 1:", input_file1)
        print("  Input image 2:", input_file2)
        print("  Output file:", output_file)
    elif len(sys.argv) == 3:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]
    else:
        print("Usage: python compare_images.py <input_image1.pgm> <input_image2.pgm>")
        sys.exit(1)
    
    # Compare the images.
    are_equal = compare_images(input_file1, input_file2)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w") as f:
        f.write(str(are_equal))
    
    print("Comparison complete. Result written to:", output_file)
    return are_equal

if __name__ == "__main__":
    run()
