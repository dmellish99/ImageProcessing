import cv2
import sys
import os

def threshold_image(image_path, threshold_value):
    """
    Reads a grayscale image and applies thresholding:
      - If the pixel value is greater or equal to threshold_value, assign 255.
      - Otherwise, assign 0.
      
    Args:
        image_path (str): Path to the input PGM image.
        threshold_value (int): Threshold value.
        
    Returns:
        new_img: The thresholded image.
    """
    # Read the image in grayscale mode.
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Unable to read image from '{image_path}'. Please check the path and format.")
    
    new_img = img.copy()
    
    nrows, ncols = img.shape
    
    for row in range(nrows):
        for col in range(ncols):
            pixel = img[row, col]
            if pixel >= threshold_value:
                new_img[row, col] = 255
            else:
                new_img[row, col] = 0
    
    return new_img

def run():
    """
    Main function to execute Exercise 2A.
    
    Usage:
      - Without arguments, it uses default values:
          Input image:  ./src/cam_74.pgm
          Threshold:    100
          Output image: ./output/cam_74_threshold100.pgm
      - Otherwise:
          python 2a.py <input_image.pgm> <threshold_value> <output_image.pgm>
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) == 1:
        # Default values
        input_file = os.path.join(script_dir, "src", "cam_74.pgm")
        threshold = 100
        output_file = os.path.join(script_dir, "output", "cam_74_threshold100.pgm")
        print("No arguments provided. Using default values:")
        print("  Input image:", input_file)
        print("  Threshold:", threshold)
        print("  Output image:", output_file)
    elif len(sys.argv) == 4:
        input_file = sys.argv[1]
        try:
            threshold = int(sys.argv[2])
        except ValueError:
            print("Threshold value must be an integer.")
            sys.exit(1)
        output_file = sys.argv[3]
    else:
        print("Usage: python 2a.py <input_image.pgm> <threshold_value> <output_image.pgm>")
        sys.exit(1)
    
    # Apply thresholding.
    result = threshold_image(input_file, threshold)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    cv2.imwrite(output_file, result)
    print("Image processed and saved to:", output_file)

if __name__ == "__main__":
    run()
