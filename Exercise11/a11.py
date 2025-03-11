
import sys
import cv2
import numpy as np
import os



def main():

    """
    Checks if the flatzone of a given pixel for an image is a local minima.
    
    Usage:
      python exercise_11a.py <input_image_path> <input_text_file>
      
      where:
       - <input_image_path> is the path to the input PGM image
       - <input_text_file> is the path to the text file where the parameters are specified
       - <output_image_path> is the path to where the output image will be saved
       
    If no arguments are provided, default values are used:
      - input_image_path: src/gran01_64.pgm
      - input_text_file: exercise_11a_input_01.txt
      - output_image_path: output/exercise_11a_output.pgm
    
    The output will be provided in output/exercise_11a_output.pgm
    
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))


    if len(sys.argv) == 1:
        input_image_path = os.path.join(script_dir, "src", "gran01_64.pgm")
        input_text_file = "exercise_11a_input_01.txt"
        print("No arguments provided. Using default values:")
        print("  Input image:", input_image_path)
        output_image_path="output/exercise_11a_output.pgm"

    elif len(sys.argv) < 4:
        print("Usage: python exercise_11a.py <input_image_path> <input_text_file> <output_image_path>")
        sys.exit(1)
    else:
        input_image_path = sys.argv[1]
        input_text_file = sys.argv[2]
        output_image_path=sys.argv[3]





    ## Read image path
    img=cv2.imread(input_image_path,cv2.IMREAD_GRAYSCALE)

    with open(input_text_file) as file:
        content=file.readlines()
        a_col=int(content[0])
        a_row=int(content[1])
        neighbor_connectivity=int(content[2])
        label_intensity_value=int(content[3])

        file.close()

   


    
    ## Establish dimensinos of image
    nrows=img.shape[0]
    ncols=img.shape[1]

    
    ## Set for output image
    out=np.zeros((nrows, ncols))

    minrow=0
    maxrow=nrows
    mincol=0
    maxcol=ncols

    
    ## Create a binary matrix that will flag pixels which have already been processed
    processed_status=np.zeros((nrows, ncols))

    # Always process the seed pixel
    waiting_queue = [(a_row, a_col)]
    processed_status[a_row, a_col] = 1  # Mark as visited
    out[a_row, a_col] = label_intensity_value  # Mark the flatzone region


    
    while len(waiting_queue)>0:
        

        selected_pixel=waiting_queue.pop(0)
        

        row=selected_pixel[0]
        col=selected_pixel[1]

        selected_pixel_intensity=img[row,col]





        processed_status[row, col]=1


        

        ## Initialize various lists
        valid_neighbors=[]
        coords_to_check=[]

        ## Add pixel above
        coords_to_check.append((row-1,col))
        ## Add pixel below
        coords_to_check.append((row+1,col))
        
        ## Add pixel to the right
        coords_to_check.append((row,col+1))
        
        ## Add pixel to the left
        coords_to_check.append((row,col-1))

        ## Case where neighbor connectivity is 8 
        if neighbor_connectivity==8:
            ## Add pixel diagonally upper left 
            coords_to_check.append((row-1,col-1))

            ## Add pixel diagonally upper right
            coords_to_check.append((row-1,col+1))

            ## Add pixel diagonally lower left
            coords_to_check.append((row+1,col-1))

            ## Add pixel diagonally lower right
            coords_to_check.append((row+1,col+1))

        ## Ensure that pixel coordinates which exceed the image dimension are NOT added
        for coord in coords_to_check:

            row_idx=coord[0]
            col_idx=coord[1]
            
            if (row_idx>=minrow and row_idx<=maxrow-1) and (col_idx>=mincol and col_idx<=maxcol-1):
                valid_neighbors.append((row_idx,col_idx))
    
        ## Iterate through each neighbor of the valid pixels to check
        for neighbor in valid_neighbors:

            row_idx=neighbor[0]
            col_idx=neighbor[1]

            # neighbor_distinct_vals.append(img[row_idx,col_idx])



        ## Check if the neighbor matches the pixel intensity of a selected pixel and also ensure that it hasn't been processed.
            if img[row_idx,col_idx]==selected_pixel_intensity and processed_status[row_idx,col_idx]==0:
                processed_status[row_idx,col_idx]=1
                ## Add the neighbor pixel to the waiting queue

                waiting_queue.append((row_idx,col_idx))

                out[row_idx,col_idx]=label_intensity_value



    ## Output image to file
    cv2.imwrite(output_image_path,out)


    return out


## Test function on input image


# test_input_image_path='src/immed_gray_inv_20051218_frgr4.pgm'

# input_text_file='exercise_13a_input_01.txt'

# img_test=identify_flatzone_local_min(test_input_image_path,input_text_file)


# with open('output/exercise_13a_output_01.txt','w') as file:
#     file.write(str(img_test))
#     file.close()



# test_input_image_path='src/immed_gray_inv_20051218_frgr4.pgm'

# input_text_file='exercise_13a_input_02.txt'

# img_test=identify_flatzone_local_min(test_input_image_path,input_text_file)


# with open('output/exercise_13a_output_02.txt','w') as file:
#     file.write(str(img_test))
#     file.close()


if __name__ == "__main__":
    main()