import cv2
import sys
import os

def inf_images(image_path1, image_path2):
    """
    Reads two grayscale PGM images and computes their pixel-wise infimum (minimum).
    
    Args:
        image_path1 (str): Path to the first input PGM image.
        image_path2 (str): Path to the second input PGM image.
        
    Returns:
        inf_img: The resulting image obtained by taking the pixel-wise minimum.
    """
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    if img1 is None:
        raise ValueError(f"Unable to read image from '{image_path1}'. Check the path and format.")
    
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
    if img2 is None:
        raise ValueError(f"Unable to read image from '{image_path2}'. Check the path and format.")
    
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Compute pixel-wise minimum (infimum)
    inf_img = cv2.min(img1, img2)
    return inf_img

def run():
    """
    Main function to compute the infimum of two PGM images.
    
    Usage:
      - Without arguments, the following default values are used:
          Input image 1: ./src/exercise_02c_input_01.pgm
          Input image 2: ./src/exercise_02c_input_02.pgm
          Output image:  ./output/exercise_02c_inf_output_01.pgm
      - With arguments:
          python exercise_02c_inf.py <input_image1.pgm> <input_image2.pgm> <output_image.pgm>
    
    The computed inf image is saved to the specified output path.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) == 1:
        input_file1 = os.path.join(script_dir, "src", "image1.pgm")
        input_file2 = os.path.join(script_dir, "src", "image2.pgm")
        output_file = os.path.join(script_dir, "output", "exercise_02c_inf_output_01.pgm")
        print("No arguments provided. Using default values:")
        print("  Input image 1:", input_file1)
        print("  Input image 2:", input_file2)
        print("  Output image:", output_file)
    elif len(sys.argv) == 4:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]
        output_file = sys.argv[3]
    else:
        print("Usage: python exercise_02c_inf.py <input_image1.pgm> <input_image2.pgm> <output_image.pgm>")
        sys.exit(1)
    
    inf_img = inf_images(input_file1, input_file2)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    cv2.imwrite(output_file, inf_img)
    print("Inf image computed and saved to:", output_file)
    return inf_img

if __name__ == "__main__":
    run()
