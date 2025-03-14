
import sys
import cv2
import numpy as np
import os



def run():

    """
    Checks if the flatzone of a given pixel for an image is a local minima.
    
    Usage:
      python exercise_12a.py <input_image_path> <input_text_file> <output_text_path>
      
      where:
       - <input_image_path> is the path to the input PGM image
       - <input_text_file> is the path to the text file where the parameters are specified
       - <output_text_path> is the path to the output txt file
       
    If no arguments are provided, default values are used:
      - input_image: src/immed_gray_inv.pgm
      - input_text_file: exercise_12a_input_01.txt
      - output_text_path will be provided in output/exercise_12a_output.txt
    
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))


    if len(sys.argv) == 1:
        input_image_path = os.path.join(script_dir, "src", "immed_gray_inv.pgm")
        input_text_file="Exercise12/exercise_12a_input_01.txt"
        output_text_path='Exercise12/output/exercise_12a_output.txt'

        print("No arguments provided. Using default values:")
        print("  Input image:", input_image_path)
        print("  Output text:", output_text_path)

        print()
    elif len(sys.argv) < 4:
        print("Usage: python exercise_12a.py <input_image_path> <input_text_file> <output_text_path>")
        sys.exit(1)
    else:
        input_image_path=sys.argv[1]
        input_text_file = sys.argv[2]
        output_text_path=sys.argv[3]

    print(input_image_path)




    ## Read image path
    img=cv2.imread(input_image_path,cv2.IMREAD_GRAYSCALE)

    with open(input_text_file) as file:
        content=file.readlines()

        neighbor_connectivity=int(content[0])
        # label_intensity_value=int(content[3])

        file.close()

   


    
    ## Establish dimensinos of image
    nrows=img.shape[0]
    ncols=img.shape[1]



    minrow=0
    maxrow=nrows
    mincol=0
    maxcol=ncols

    ## Create a binary matrix that will flag pixels which have already been processed
    processed_status=np.zeros((nrows, ncols))
    



    region_counter=0

    for a_row in range(0,maxrow):
        

        for a_col in range(0,maxcol):
            
            region_coords=[]
     
            
            if processed_status[a_row,a_col]==0:
                ## Add to counter
                region_counter+=1
                

                ## Establish a waiting queue
                waiting_queue=[(a_row,a_col)]

                
                while len(waiting_queue)>0:

                    selected_pixel=waiting_queue.pop(0)



                    row=selected_pixel[0]
                    col=selected_pixel[1]


                    selected_pixel_intensity=img[row,col]



                    # if processed_status[row, col]!=0:
                    #     continue


                    processed_status[row, col]=region_counter



                    ## Add the value to the list of region coords
                    region_coords.append((row, col))

                    
                    

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
                           
                        
                            ## Add the neighbor pixel to the waiting queue

                            waiting_queue.append((row_idx,col_idx))
                            
                            ## Add processed status
                            processed_status[row_idx,col_idx]=region_counter


    ## Get the last region
    max_region=np.max(processed_status)

    with open(output_text_path,'w') as file:
        file.write(str(max_region))
        file.close()

    return max_region
        
if __name__ == "__main__":
    run()