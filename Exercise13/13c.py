
import sys
import cv2
import numpy as np
import math


def identify_flatzone_local_minima(img,row,col):
 

    ## Establish dimensinos of image
    nrows=img.shape[0]
    ncols=img.shape[1]



    # for label_intensity_value in range(0,256):

        # Output image of the same size as the original (but will be modified later).
   

    minrow=0
    maxrow=nrows
    mincol=0
    maxcol=ncols

    ## Create a binary matrix that will flag pixels which have already been processed
    processed_status=np.zeros((nrows, ncols))

    ## Create a binary matrix that will flag pixels which are local Minima
    local_min=np.zeros((nrows, ncols))

    ## Create a binary matrix that will flag pixels belonging to the region
    flatzone=np.zeros((nrows,ncols))

    unique_pixels=np.unique(img).tolist()

    # print(unique_pixels)
    # print(maxrow)
    # print(maxcol)
 

    selected_pixel_intensity=img[row,col]
    # print(selected_pixel_intensity)

    label_intensity_value=selected_pixel_intensity

    processed_status[row,col]=1
    
    waiting_queue=[(row,col)]


    region_coords=[]

    while len(waiting_queue)>0:
        

        cur_row=waiting_queue[0][0]
        cur_col=waiting_queue[0][1]
        

        
        cur_pixel_val=img[cur_row,cur_col]
        

        ## Initialize various lists
        valid_neighbors=[]
        coords_to_check=[]
        neighbors_to_check=[]


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
               
                ## Add the neighbor pixel to the waiting queue

                waiting_queue.append((row_idx,col_idx))

                flatzone[row_idx,col_idx]=1

                ## Set processed status=label intensity_value to ensure pixel won't be re-added to the queue
                processed_status[row_idx,col_idx]=1

                ## Add proper coordinates to region coords list for later
                region_coords.append((row_idx,col_idx))

            
            elif img[row_idx,col_idx]!=selected_pixel_intensity and processed_status[row_idx,col_idx]==0 :
                ## Set processed status=label intensity_value to ensure pixel won't be re-added to the queue
                processed_status[row_idx,col_idx]=1

                ## Add the coordinates to a list of neighbors_to_check
                neighbors_to_check.append((row_idx,col_idx))


            
        ## Finally, expunge the first value from the queue as it is has been processed.
        del waiting_queue[0]

    

    # print(len(neighbors_to_check))
    is_local_minimum=0
    n_pixels_greater_than_region=0
    ## Iterate through neighbor pixels which don't have the same similiarity
    for a_neighbor in neighbors_to_check:
        neighbor_row=a_neighbor[0]
        neighbor_col=a_neighbor[1]

        neighbor_pixel=img[neighbor_row,neighbor_col]
        # print(selected_pixel_intensity)
        # print(neighbor_pixel)
        if neighbor_pixel<selected_pixel_intensity:
            n_pixels_greater_than_region+=1
    if n_pixels_greater_than_region==0:
        is_local_minimum=1
    
    

    if is_local_minimum==1:

        for coord_pair in region_coords:
            local_min_row=coord_pair[0]
            local_min_col=coord_pair[1]

            local_min[local_min_row,local_min_col]=1
        # print(np.where(local_min==1))

            
    ## Return flat image and indicator if it is a local max
    return [flatzone,local_min]


def identifylocalMinima(img_path):

    ## Read image path
    img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
    

    
    ## Establish dimensinos of image
    nrows=img.shape[0]
    ncols=img.shape[1]

    
    ## Set for output image
    out=np.zeros((nrows, ncols))

    ## Set a process status
    processed=np.zeros((nrows,ncols))

    minrow=0
    maxrow=nrows
    mincol=0
    maxcol=ncols


    for row in range(minrow,maxrow):

        for col in range(mincol,maxcol):
            ## Check if pixel has been processed already
            if processed[row,col]==0:
                ## If not, run the flatzone algo
                identified_flatzone=identify_flatzone_local_minima(img,row,col)
                
                flatzone=identified_flatzone[0]
                

                local_min=identified_flatzone[1]
                
                
                ## only select the region which is connected
                local_min=np.where(local_min==1)
                # print(local_min)

                

                local_min_coords=list(zip(*local_min))

                flatzone=np.where(flatzone==1)

                flatzone_coords=list(zip(*flatzone))

                for coord_pair in flatzone_coords:
                    row_to_mark=coord_pair[0]
                    col_to_mark=coord_pair[1]

                    processed[row_to_mark,col_to_mark]=1
                
                if len(local_min_coords)>0:
                    for coord_pair in local_min_coords:
                        row_to_mark=coord_pair[0]
                        col_to_mark=coord_pair[1]

                        out[row_to_mark,col_to_mark]=255
                


    return out

## Test function on input image 1



test_img_path='src/immed_gray_inv_20051218_frgr4.pgm'


img_test_local_minima=identifylocalMinima(test_img_path)

cv2.imwrite('output/exercise_13c_output_01.pgm',img_test_local_minima)


    
        
