
import sys
import cv2
import numpy as np
import math


def identify_flatzone(img,row,col,neighbor_connectivity):
 

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


    unique_pixels=np.unique(img).tolist()

    # print(unique_pixels)
    # print(maxrow)
    # print(maxcol)
 

    selected_pixel_intensity=img[row,col]
    # print(selected_pixel_intensity)

    label_intensity_value=selected_pixel_intensity

    processed_status[row,col]=1
    
    waiting_queue=[(row,col)]

    ## idea is to store a list of lists that stores according to each pixel 

    ## example {0:[[(0,1),(0,2)], [(12,13),(13,12)]],1:[[(100,110),(100,111)], [(18,18),(19,19)]] }
    total_regions={}
    while len(waiting_queue)>0:
        

        cur_row=waiting_queue[0][0]
        cur_col=waiting_queue[0][1]
        


        cur_pixel_val=img[cur_row,cur_col]
        
       
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
               
                ## Add the neighbor pixel to the waiting queue

                waiting_queue.append((row_idx,col_idx))

                ## Set processed status=1 to ensure pixel won't be re-added to the queue
                processed_status[row_idx,col_idx]=1
            
        ## Finally, expunge the first value from the queue as it is has been processed.
        del waiting_queue[0]
    return processed_status


def identifyTotalFlatZones(img_path,input_txt_path):
    ## Read image path
    img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
    
    ## Read arguments
    with open(input_txt_path) as file:
        content=file.readlines()
        neighbor_connectivity=int(content[0])

        file.close()
    
    ## Establish dimensinos of image
    nrows=img.shape[0]
    ncols=img.shape[1]

    
    ## Mapped Regions
    out=np.zeros((nrows, ncols))



    minrow=0
    maxrow=nrows
    mincol=0
    maxcol=ncols

    region_counter=1
    for row in range(minrow,maxrow):

        for col in range(mincol,maxcol):
            ## Check if pixel has been processed already
            if out[row,col]==0:
                ## If not, run the flatzone algo
                identified_flatzone=identify_flatzone(img,row,col,neighbor_connectivity)
                
                ## only select the region which is connected
                identified_flatzone=np.where(identified_flatzone==1)

                identified_flatzone_coords=list(zip(*identified_flatzone))

                for coord_pair in identified_flatzone_coords:
                    row_to_mark=coord_pair[0]
                    col_to_mark=coord_pair[1]

                    out[row_to_mark,col_to_mark]=region_counter
                ## Move on to next region and consider it a different section
                region_counter+=1
    ## Subtract one since there is a general "unbounded area"
    return (region_counter-1)



## Test function on input image 1


test_img_path='src/immed_gray_inv_20051218_thresh127.pgm'

input_txt_path='exercise_12a_input_01.txt'

img_test_n_regions=identifyTotalFlatZones(test_img_path,input_txt_path)

print(img_test_n_regions)


## Test function on input image 2 

test_img_path='src/immed_gray_inv.pgm'

input_txt_path='exercise_12a_input_02.txt'

img_test_n_regions=identifyTotalFlatZones(test_img_path,input_txt_path)

print(img_test_n_regions)



    
        
