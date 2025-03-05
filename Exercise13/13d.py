
import sys
import cv2
import numpy as np
import os



def main():

    """
    Checks for all flatzones of an image which are local maxima.
    
    Usage:
      python exercise_13d.py <input_image_path> <output_image_path>
      
      where:
       - <input_image_path> is the path to the input PGM image
       - <output_image_path> is the path to the output PGM image
       
    If no arguments are provided, default values are used:
      - input_image_path: src/immed_gray_inv_20051218_frgr4.pgm
      - output_image_path: output/exercise_13c_output.pgm


    The output image will be provided in output/exercise_13c_output.pgm

    """

    script_dir = os.path.dirname(os.path.abspath(__file__))


    if len(sys.argv) == 1:
        input_image_path = os.path.join(script_dir, "src", "immed_gray_inv_20051218_frgr4.pgm")
        output_image_path="output/exercise_13c_output.pgm"
        print("No arguments provided. Using default values:")
        print("  Input image:", input_image_path)
        print("  Input image:", output_image_path)

    elif len(sys.argv) < 3:
        print("Usage: python exercise_13c.py <i> <input_image_path> <output_image_path>")
        sys.exit(1)
    else:
        input_image_path = sys.argv[1]
        output_image_path=sys.argv[2]

    ## Read image path
    img=cv2.imread(input_image_path,cv2.IMREAD_GRAYSCALE)


    
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
    

    for a_row in range(minrow,maxrow):

        for a_col in range(mincol,maxcol):

          
            if processed_status[a_row,a_col]==0:

                ## Initialize Region Coordinates
                region_coords=[]

                neighbor_distinct_vals=[]


                ## Establish a waiting queue
                waiting_queue=[(a_row,a_col)]

                
                while len(waiting_queue)>0:

                    selected_pixel=waiting_queue.pop(0)



                    row=selected_pixel[0]
                    col=selected_pixel[1]


                    selected_pixel_intensity=img[row,col]



                    if processed_status[row, col]==1:
                        continue


                    processed_status[row, col]=1



                    ## Add the value to the list of region coords
                    region_coords.append((row, col))

                    
                    

                    ## Initialize various lists
                    valid_neighbors=[]
                    coords_to_check=[]


                    ## Add four neighbors (will check later if they are valid pixels)
                    ## Add pixel above
                    coords_to_check.append((row-1,col))
                    
                    ## Add pixel below
                    coords_to_check.append((row+1,col))
                    
                    ## Add pixel to the right
                    coords_to_check.append((row,col+1))
                    
                    ## Add pixel to the left
                    coords_to_check.append((row,col-1))

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
                        
                            ## Add the neighbor pixel to the waiting queue

                            waiting_queue.append((row_idx,col_idx))

                        elif img[row_idx,col_idx]!=selected_pixel_intensity:

                            ## Add pixel intensity to neighbors list
                            neighbor_distinct_vals.append(img[row_idx,col_idx])

    
            ## Set output to 255 if local minimum is detected
            if len(neighbor_distinct_vals)>0 and selected_pixel_intensity>max(neighbor_distinct_vals):
                for row_idx, col_idx in region_coords:
                    out[row_idx, col_idx] = 255  # Mark local maxima flat zones in white

    ## Output image to file 
    
    cv2.imwrite(output_image_path,out)
    return out



if __name__ == "__main__":
    main()
        