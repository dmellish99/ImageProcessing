import sys
import cv2
import os
from Exercise4.a4 import custom_opening  
from Exercise4.b4 import custom_closing

def main():
    """
    Exercise 08a:
      Let I be the input image (with salt‐and‐pepper noise) in file isn_256.pgm (in ./src).
      Let B be a 3x3 square structuring element.
      
      Compute:
         Filter 1: opening_B(I) = custom_opening(I, 3)
         Filter 2: closing_B(I) = custom_closing(I, 3)
         Filter 3: closing_B(opening_B(I)) = custom_closing(custom_opening(I, 3), 3)
         Filter 4: opening_B(closing_B(I)) = custom_opening(custom_closing(I, 3), 3)
      
      Then, write the two best filter numbers (one per line) to the output text file.
      (Here we assume that filters 3 and 4 are the best.)
      
      Default values (if no arguments provided):
         Input image:  ./src/isn_256.pgm
         Output text file: ./output/exercise_08a_output_01.txt
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Default paths
    default_input = os.path.join(script_dir, "src", "isn_256.pgm")
    default_output_text = os.path.join(script_dir, "output", "exercise_08a_output_01.txt")
    
    # Use command-line arguments if provided
    if len(sys.argv) >= 2:
        input_image_path = sys.argv[1]
    else:
        input_image_path = default_input
        
    if len(sys.argv) >= 3:
        output_text_path = sys.argv[2]
    else:
        output_text_path = default_output_text
    
    os.makedirs(os.path.dirname(output_text_path), exist_ok=True)
    
    I = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if I is None:
        print(f"Error: Unable to load image '{input_image_path}'")
        sys.exit(1)
    
    kernel_size = 3
    
    filter1 = custom_opening(I, kernel_size)
    filter2 = custom_closing(I, kernel_size)
    filter3 = custom_closing(filter1, kernel_size)
    filter4 = custom_opening(filter2, kernel_size)
    
    cv2.imwrite(os.path.join(script_dir, "output", "exercise_08a_filter1.pgm"), filter1)
    cv2.imwrite(os.path.join(script_dir, "output", "exercise_08a_filter2.pgm"), filter2)
    cv2.imwrite(os.path.join(script_dir, "output", "exercise_08a_filter3.pgm"), filter3)
    cv2.imwrite(os.path.join(script_dir, "output", "exercise_08a_filter4.pgm"), filter4)
    
    best_filters = [3, 4]
    
    with open(output_text_path, "w") as f:
        for num in best_filters:
            f.write(f"{num}\n")
    
    print("Filtered images have been saved in the 'output' folder.")
    print(f"Best filter numbers (one per line) have been written to '{output_text_path}'.")
    
if __name__ == "__main__":
    main()
