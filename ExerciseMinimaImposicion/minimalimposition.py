import cv2
import sys
import os
import numpy as np
import math

def inf_images(img1, img2):
    """
    Reads two grayscale PGM images and computes their pixel-wise infimum (minimum).
    
    Args:
        image_1 (cv2.image): input PGM Image.
        image_2 (cv2.image): input PGM Image.
        
    Returns:
        inf_img: The resulting image obtained by taking the pixel-wise minimum.
    """
    if img1 is None:
        raise ValueError(f"Unable to read image.")
    
    if img2 is None:
        raise ValueError(f"Unable to read image.")
    
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Compute pixel-wise minimum (infimum)
    inf_img = cv2.min(img1, img2)
    return inf_img


def sup_images(img1, img2):
    """
    Reads two grayscale PGM images and computes their pixel-wise supremum (maximum).
    
    Args:
        image_1 (cv2.image): input PGM Image.
        image_2 (cv2.image): input PGM Image.
        
    Returns:
        sup_img: The resulting image obtained by taking the pixel-wise minimum.
    """
    if img1 is None:
        raise ValueError(f"Unable to read image.")
    
    if img2 is None:
        raise ValueError(f"Unable to read image.")
    
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Compute pixel-wise minimum (infimum)
    sup_img = cv2.max(img1, img2)
    return sup_img



def compare_images(img1, img2):
    """
    Reads two grayscale PGM images and checks 
    
    Args:
        image_1 (cv2.image): input PGM Image.
        image_2 (cv2.image): input PGM Image.
        
    Returns:
        bool: True if the images are equal, False otherwise.
    """
    if img1 is None:
        raise ValueError(f"Unable to read image.")
    
    if img2 is None:
        raise ValueError(f"Unable to read image.")
    if img1.shape != img2.shape:
        return False
    
    return np.array_equal(img1, img2)



import numpy as np

import numpy as np

def custom_erosion(img, kernel_size, connectivity):
    """
    Perform morphological erosion on a grayscale image.

    Args:
        img (numpy.ndarray): Grayscale image.
        kernel_size (int): Size of the square kernel (should be odd).
        connectivity (int): Neighbor connectivity (4 or 8).

    Returns:
        numpy.ndarray: The eroded image.
    """
    h, w = img.shape
    pad = kernel_size // 2
    out = np.copy(img)  # Copy input image

    # Define 4-connectivity neighbors
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # If 8-connectivity is chosen, add diagonal neighbors
    if connectivity == 8:
        neighbor_offsets += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Iterate over every pixel
    for y in range(h):
        for x in range(w):
            # List to store neighbor pixel values
            neighbor_values = [img[y, x]]  # Include center pixel

            # Check neighbors based on connectivity
            for dy, dx in neighbor_offsets:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:  # Ensure inside bounds
                    neighbor_values.append(img[ny, nx])

            # Assign the minimum value from valid neighbors
            out[y, x] = min(neighbor_values)

    return out



def main ():

    """
    Reads a grayscale image PGM along with a marker image and imposes the Minima.

    
    Usage:
      python exercise_12a.py <input_image_path> <input_text_file> <output_text_path>
      
      where:
       - <input_image_path> is the path to the input PGM image
       - <input_image_markers_path> is the path to the input image marker PGM_image
       - <connectivity> is the amount of connectivity
       - <output_image_path> is the path to the output txt file
       
    If no arguments are provided, default values are used:
      - input_image: src/micro24_20060309_grad.pgm.pgm
      - connectivity: 8 
      - input_image_markers_path: src/micro24_20060309_markersinsideandfond.pgm
      - output_text_path will be provided in output/exercise_11_minima_imposition_output.pgm'
    
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) == 1:
        input_image_path = os.path.join(script_dir, "src", "micro24_20060309_grad.pgm")
        connectivity=8
        output_image_path='output/exercise_11_minima_imposition.pgm'
        input_image_markers_path='src/micro24_20060309_markersinsideandfond.pgm'
        print("No arguments provided. Using default values:")
        print("  Input image:", input_image_path)
    elif len(sys.argv) < 5:
        print("Usage: python exercise_11minimalimposition.py <input_image_path> <input_image_markers_path> <input_text_file> <output_text_path>")
        sys.exit(1)
    else:
        input_image_path=sys.argv[1]
        connectivity=int(sys.argv[2])
        input_image_markers_path=sys.argv[3]
        output_text_path=sys.argv[4]
        

    print(input_image_path)


    
    img=cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    img_markers=cv2.imread(input_image_markers_path, cv2.IMREAD_GRAYSCALE)

    ## Invert the image
    img_markers_inv=img_markers

    ## Iterate through each pixel of img_markers to invert the image
    for row in range(0,img_markers.shape[0]):
        for col in range(0,img_markers.shape[1]):
            if img_markers[row,col]==0:
                img_markers_inv[row,col]=255
            elif img_markers[row,col]==255:
                img_markers_inv[row,col]=0


    img_prime=inf_images(img,img_markers_inv)

    
    
    cur_image=img_markers_inv
    
    last_image=np.zeros((img.shape[0],img.shape[1]))


    while (compare_images(cur_image,last_image)==0):
        last_image=cur_image

        erosion=custom_erosion(cur_image,3,connectivity)

        cur_image=sup_images(erosion,img_prime)


    ## Write to filepath
    cv2.imwrite(output_image_path,cur_image)
    return cur_image


    

# test_image=imMinimaImpose('src/micro24.pgm','src/micro24_20060309_markersinsideandfond.pgm',8,'output/ gradient micro24_mod.pgm')


if __name__ == "__main__":
    main()



# def run():
#     """
#     Main function to compute the infimum of two PGM images.
    
#     Usage:
#       - Without arguments, the following default values are used:
#           Input image 1: ./src/exercise_02c_input_01.pgm
#           Input image 2: ./src/exercise_02c_input_02.pgm
#           Output image:  ./output/exercise_02c_inf_output_01.pgm
#       - With arguments:
#           python exercise_02c_inf.py <input_image1.pgm> <input_image2.pgm> <output_image.pgm>
    
#     The computed inf image is saved to the specified output path.
#     """
#     script_dir = os.path.dirname(os.path.abspath(__file__))
    
#     if len(sys.argv) == 1:
#         input_file1 = os.path.join(script_dir, "src", "image1.pgm")
#         input_file2 = os.path.join(script_dir, "src", "image2.pgm")
#         output_file = os.path.join(script_dir, "output", "exercise_02c_inf_output_01.pgm")
#         print("No arguments provided. Using default values:")
#         print("  Input image 1:", input_file1)
#         print("  Input image 2:", input_file2)
#         print("  Output image:", output_file)
#     elif len(sys.argv) == 4:
#         input_file1 = sys.argv[1]
#         input_file2 = sys.argv[2]
#         output_file = sys.argv[3]
#     else:
#         print("Usage: python exercise_02c_inf.py <input_image1.pgm> <input_image2.pgm> <output_image.pgm>")
#         sys.exit(1)
    
#     inf_img = inf_images(input_file1, input_file2)
    
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
#     cv2.imwrite(output_file, inf_img)
#     print("Inf image computed and saved to:", output_file)
#     return inf_img

# if __name__ == "__main__":
#     run()
