#!/usr/bin/env python3
import sys

# Import the run() functions from each exercise.
# Adjust the import paths according to your project structure.
from Exercise11.a11 import run as run_11a
from Exercise12.a12 import run as run_12a
from Exercise13.a13 import run as run_13a
from Exercise13.b13 import run as run_13b
from Exercise13.c13 import run as run_13c
from Exercise13.d13 import run as run_13d
from ExerciseMinimaImposition.minimaimposition import run as run_minima_imposition



def main():
    print("=== MAIN MENU ===")
    print("This central main module calls the run functions of each exercise.")
    print("Each exercise uses default parameters if none are provided.")
    print("To supply custom parameters, run the corresponding exercise module directly with your desired parameters.")
    print("For example, if an exercise expects an input image and an output file, run it as:")
    print("    python <exercise_module>.py <input_image> <output_file>")
    print("where <input_image> and <output_file> are your custom parameters.\n")
    
    while True:
        print("\n=== EXERCISE MENU ===")
        print("1) Exercise 11a")
        print("2) Minima Imposition")
        print("3) Exercise 12a")
        print("4) Exercise 13a")
        print("5) Exercise 13b")
        print("6) Exercise 13c")
        print("7) Exercise 13d")
        print("0) Exit")
        
        choice = input("Select an exercise: ").strip()
        
        if choice == "1":
            run_11a()
        elif choice == "2":
            run_minima_imposition()
        elif choice == "3":
            run_12a()
        elif choice == "4":
            run_13a()
        elif choice == "5":
            run_13b()
        elif choice == "6":
            run_13c()
        elif choice == "7":
            run_13d()
        elif choice == "0":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
