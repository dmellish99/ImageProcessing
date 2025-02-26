import cv2
import sys
import os

def sup_images(image_path1, image_path2):
    """
    Reads two grayscale PGM images and computes their pixel-wise supremum (maximum).
    
    Args:
        image_path1 (str): Path to the first input PGM image.
        image_path2 (str): Path to the second input PGM image.
        
    Returns:
        new_img: The resulting image obtained by taking the pixel-wise maximum.
    """

    ## Read image file paths
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2=cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
    
    ## Set a copy of the first image for output later
    new_img=img1
    
    ## Check n_pixels
    if img1.size!=img2.size:
        raise ValueError("Images Sizes are not Equal")
    
    ## Continue with code if image sizes are equal
    else:
        ## Set dimensions of images
        nrows=img1.shape[0]
        ncols=img1.shape[1]
        
        ## Iterate through each row and column (each pixel)
        for row in range(0,nrows):
            for col in range(0,ncols):
                ## Set a value for the current pixel of each image
                cur_pixel_img1=img1[row,col]
                cur_pixel_img2=img2[row,col]
                ## Use the Max of the two pixels if Inf
                new_img[row,col]=max(cur_pixel_img1,cur_pixel_img2)
    
    return new_img

def run():
    """
    Main function to compute the supremum of two PGM images.
    
    Usage:
      - Without arguments, the following default values are used:
          Input image 1: ./src/exercise_02c_input_01.pgm
          Input image 2: ./src/exercise_02c_input_02.pgm
          Output image:  ./output/exercise_02c_sup_output_01.pgm
      - With arguments:
          python exercise_02c_sup.py <input_image1.pgm> <input_image2.pgm> <output_image.pgm>
    
    The computed sup image is saved to the specified output path.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) == 1:
        input_file1 = os.path.join(script_dir, "src", "image1.pgm")
        input_file2 = os.path.join(script_dir, "src", "image2.pgm")
        output_file = os.path.join(script_dir, "output", "exercise_02c_sup_output_01.pgm")
        print("No arguments provided. Using default values:")
        print("  Input image 1:", input_file1)
        print("  Input image 2:", input_file2)
        print("  Output image:", output_file)
    elif len(sys.argv) == 4:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]
        output_file = sys.argv[3]
    else:
        print("Usage: python exercise_02c_sup.py <input_image1.pgm> <input_image2.pgm> <output_image.pgm>")
        sys.exit(1)
    
    sup_img = sup_images(input_file1, input_file2)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    cv2.imwrite(output_file, sup_img)
    print("Sup image computed and saved to:", output_file)
    return sup_img

if __name__ == "__main__":
    run()
