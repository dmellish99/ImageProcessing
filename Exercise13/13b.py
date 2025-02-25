
import sys
import cv2
import numpy as np


def identify_flatzone_local_max(img_path,input_txt_path):
    ## Read image path
    img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)

    with open(input_txt_path) as file:
        content=file.readlines()
        col=int(content[0])
        row=int(content[1])
        neighbor_connectivity=int(content[2])
        # label_intensity_value=int(content[3])

        file.close()


    

    ## Establish dimensinos of image
    nrows=img.shape[0]
    ncols=img.shape[1]


    # Output image of the same size as the original (but will be modified later).
    out=np.zeros((nrows, ncols))

    ## Create a binary matrix that will flag pixels which have already been processed
    processed_status=np.zeros((nrows, ncols))

    minrow=0
    maxrow=nrows
    mincol=0
    maxcol=ncols

    # print(maxrow)
    # print(maxcol)

    selected_pixel_intensity=img[row,col]

    ## Set initial pixel equal to intensity of label intensity
    # out[row,col]=label_intensity_value

    processed_status[row,col]=1
    
    waiting_queue=[(row,col)]


    neighbors_to_check=[]

    while len(waiting_queue)>0:
        # print(waiting_queue[0])
        
        cur_row=waiting_queue[0][0]
        cur_col=waiting_queue[0][1]
        
        valid_neighbors=[]


        coords_to_check=[]
        if neighbor_connectivity==4:
            
            ## Add four neighbors (will check later if they are valid pixels)
            ## Add pixel above
            coords_to_check.append((cur_row-1,cur_col))
            
            ## Add pixel below
            coords_to_check.append((cur_row+1,cur_col))
            
            ## Add pixel to the right
            coords_to_check.append((cur_row,cur_col+1))
            
            ## Add pixel to the left
            coords_to_check.append((cur_row,cur_col-1))

        elif neighbor_connectivity==8:
            
            ## Add four neighbors (will check later if they are valid pixels)
            ## Add pixel above
            coords_to_check.append((cur_row-1,cur_col))
            
            ## Add pixel below
            coords_to_check.append((cur_row+1,cur_col))
            
            ## Add pixel to the right
            coords_to_check.append((cur_row,cur_col+1))
            
            ## Add pixel to the left
            coords_to_check.append((cur_row,cur_col-1))

            ## Add pixel diagonally upper left 
            coords_to_check.append((cur_row-1,cur_col-1))

            ## Add pixel diagonally upper right
            coords_to_check.append((cur_row-1,cur_col+1))

            ## Add pixel diagonally lower left
            coords_to_check.append((cur_row+1,cur_col-1))

            ## Add pixel diagonally lower right
            coords_to_check.append((cur_row+1,cur_col+1))

        ## Ensure that no pixel coordinates which exceed the image dimension are NOT added
        for coord in coords_to_check:

           row_idx=coord[0]
           col_idx=coord[1]
        
           if (row_idx>=minrow and row_idx<=maxrow-1) and (col_idx>=mincol and col_idx<=maxcol-1):
                valid_neighbors.append(coord)
        ## Iterate through each neighbor of the valid pixels to check
        for neighbor in valid_neighbors:

            row_idx=neighbor[0]
            col_idx=neighbor[1]


        ## Check if the neighbor matches the pixel intensity of a selected pixel and also ensure that it hasn't been processed.
            if img[row_idx,col_idx]==selected_pixel_intensity and processed_status[row_idx,col_idx]==0:
                ## Set the output image label
                # out[row_idx,col_idx]=label_intensity_value
                
                ## Add the neighbor pixel to the waiting queue
                waiting_queue.append((row_idx,col_idx))


                ## Set processed status=1 to ensure pixel won't be re-added to the queue
                processed_status[row_idx,col_idx]=1

            if img[row_idx,col_idx]!=selected_pixel_intensity and processed_status[row_idx,col_idx]==0:
                neighbors_to_check.append((row_idx,col_idx))
        ## Finally, expunge the first value from the queue as it is has been processed.
        del waiting_queue[0]

    print(neighbors_to_check)
    is_local_maximum=1
    ## Iterate through neighbor pixels which don't have the same similiarity
    for a_neighbor in neighbors_to_check:
        neighbor_row=a_neighbor[0]
        neighbor_col=a_neighbor[1]

        neighbor_pixel=img[neighbor_row,neighbor_col]
        # print(selected_pixel_intensity)
        print(neighbor_pixel)
        if neighbor_pixel>selected_pixel_intensity and is_local_maximum==1:
            is_local_maximum=0
    
    
    return is_local_maximum



## Test function on input image


test_img_path='src/immed_gray_inv_20051218_frgr4.pgm'

input_txt_path='exercise_13b_input_01.txt'

img_test=identify_flatzone_local_max(test_img_path,input_txt_path)


with open('output/exercise_13b_output_01.txt','w') as file:
    file.write(str(img_test))
    file.close()



test_img_path='src/immed_gray_inv_20051218_frgr4.pgm'

input_txt_path='exercise_13b_input_02.txt'

img_test=identify_flatzone_local_max(test_img_path,input_txt_path)


with open('output/exercise_13b_output_02.txt','w') as file:
    file.write(str(img_test))
    file.close()


        
            
   