
import sys
import cv2
import numpy as np
import os


import cv2 
import numpy as np


img=cv2.imread('src/wheel.png',cv2.IMREAD_GRAYSCALE)


# Creating kernel 
kernel = np.ones((3, 3), np.uint8) 
  
# Using cv2.erode() method  
img_erode= cv2.erode(img, kernel)  

img_out=img-img_erode


nrows=img.shape[0]
ncols=img.shape[1]

x_c, y_c = ncols//2, nrows//2
r = 200

color=0

for y in range(img_out.shape[0]):
    for x in range(img_out.shape[1]):
        if (x - x_c) ** 2 + (y - y_c) ** 2 <= r ** 2:
            img_out[y, x] = color  # Set pixel color inside the circle

cv2.imwrite('output/test_image.png',img_out)


# def main():

#     """
#     Checks if the flatzone of a given pixel for an image is a local minima.
    
#     Usage:
#       python exercise_s1b.py <input_image_path> <input_text_path> <connectivity> <similarity_threshold> <output_image_path>
      
#       where:
#        - <input_image_path> is the path to the input PGM image
#        - <input_text_path> locates the pixels specified
#        - <connectivity> should be an integer, either 4 or 8
#        - <similarity_threshold>  should be a positive non-zero integer, specifies the boundary of similarity
#        - <output_image_path> is the path to where the output image will be saved
       
#     If no arguments are provided, default values are used:
#       - input_image_path: src/cameraman.pgm
#       - input_text_path: exercise_s1b_input.txt
#       - connectivity - 8
#       - similarity_threshold - 30
#       - output_image_path: output/exercise_11a_output.pgm
    
    
#     """

#     script_dir = os.path.dirname(os.path.abspath(__file__))


#     if len(sys.argv) == 1:
#         input_image_path = os.path.join(script_dir, "src", "cameraman.png")
#         input_text_path='exercise_s1b_input.txt'
#         neighbor_connectivity=8
#         similarity_threshold=30
#         print("No arguments provided. Using default values:")
#         print("  Input image:", input_image_path)
#         output_image_path="output/exercise_1b_output.pgm"

#     elif len(sys.argv) < 6:
#         print("Usage: python exercise_1b.py <input_image_path> <input_text_path> <connectivity> <similarity_threshold> <output_image_path>")
#         sys.exit(1)
#     else:
#         input_image_path = sys.argv[1]
#         input_text_path=sys.argv[2]
#         neighbor_connectivity = int(sys.argv[3])
#         similarity_threshold=int(sys.argv[4])
#         output_image_path=sys.argv[5]





#     ## Read image path
#     img=cv2.imread(input_image_path,cv2.IMREAD_GRAYSCALE)

#     with open(input_text_path,'r') as file:
#         content=file.readlines()
#         a_col=int(content[0])
#         a_row=int(content[1])
#         # neighbor_connectivity=int(content[2])
#         # label_intensity_value=int(content[3])


   


    
#     ## Establish dimensinos of image
#     nrows=img.shape[0]
#     ncols=img.shape[1]

    
#     ## Set for output image
#     out=np.zeros((nrows, ncols))

#     minrow=0
#     maxrow=nrows
#     mincol=0
#     maxcol=ncols

    
#     ## Create a binary matrix that will flag pixels which have already been processed
#     processed_status=np.zeros((nrows, ncols))

#     # Always process the seed pixel
#     waiting_queue = [(a_row, a_col)]
#     processed_status[a_row, a_col] = 1  # Mark as visited
#     out[a_row, a_col] = 255  # Mark the flatzone region

#     selected_pixel_intensity=img[a_row,a_col]
#     print(selected_pixel_intensity)
    
#     while len(waiting_queue)>0:

        
        

#         selected_pixel=waiting_queue.pop(0)
        

#         row=selected_pixel[0]
#         col=selected_pixel[1]






#         processed_status[row, col]=1


        

#         ## Initialize various lists
#         valid_neighbors=[]
#         coords_to_check=[]

#         ## Add pixel above
#         coords_to_check.append((row-1,col))
#         ## Add pixel below
#         coords_to_check.append((row+1,col))
        
#         ## Add pixel to the right
#         coords_to_check.append((row,col+1))
        
#         ## Add pixel to the left
#         coords_to_check.append((row,col-1))

#         ## Case where neighbor connectivity is 8 
#         if neighbor_connectivity==8:
#             ## Add pixel diagonally upper left 
#             coords_to_check.append((row-1,col-1))

#             ## Add pixel diagonally upper right
#             coords_to_check.append((row-1,col+1))

#             ## Add pixel diagonally lower left
#             coords_to_check.append((row+1,col-1))

#             ## Add pixel diagonally lower right
#             coords_to_check.append((row+1,col+1))

#         ## Ensure that pixel coordinates which exceed the image dimension are NOT added
#         for coord in coords_to_check:

#             row_idx=coord[0]
#             col_idx=coord[1]
            
#             if (row_idx>=minrow and row_idx<=maxrow-1) and (col_idx>=mincol and col_idx<=maxcol-1):
#                 valid_neighbors.append((row_idx,col_idx))
    
#         ## Iterate through each neighbor of the valid pixels to check
#         for neighbor in valid_neighbors:

#             row_idx=neighbor[0]
#             col_idx=neighbor[1]

#             # neighbor_distinct_vals.append(img[row_idx,col_idx])



#         ## Check if the neighbor falls within the similarity threshold of a selected pixel and also ensure that it hasn't been processed.
#             if (img[row_idx,col_idx]>=(selected_pixel_intensity-similarity_threshold) and img[row_idx,col_idx]<=(selected_pixel_intensity+similarity_threshold)) and processed_status[row_idx,col_idx]==0:
#                 processed_status[row_idx,col_idx]=1
#                 ## Add the neighbor pixel to the waiting queue

#                 waiting_queue.append((row_idx,col_idx))

#                 out[row_idx,col_idx]=255



#     ## Output image to file
#     cv2.imwrite(output_image_path,out)


#     return out


# if __name__ == "__main__":
#     main()