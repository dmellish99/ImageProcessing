#!/usr/bin/env python3
import sys

# Import the run() functions from each exercise.
# Adjust the import paths according to your project structure.
from Exercise2.a2.a2 import run as run_2a
from Exercise2.b2.b2 import run as run_2b
from Exercise2.c2.c2s import run as run_2cs
from Exercise2.c2.c2i import run as run_2ci
from Exercise3.a3 import run as run_3a
from Exercise3.b3 import run as run_3b
from Exercise4.a4 import run as run_4a
from Exercise4.b4 import run as run_4b
from Exercise5.a5 import main as run_5a
from Exercise5.b5 import main as run_5b
from Exercise6.a6 import main as run_6a
from Exercise6.b6 import main as run_6b
from Exercise7.a7 import main as run_7a
from Exercise7.b7 import main as run_7b
from Exercise8.a8 import main as run_8

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
        print("2a) Exercise 2a")
        print("2b) Exercise 2b")
        print("2cs) Exercise 2c (supremum)")
        print("2ci) Exercise 2c (infimum)")
        print("3a) Exercise 3a")
        print("3b) Exercise 3b")
        print("4a) Exercise 4a")
        print("4b) Exercise 4b")
        print("5a) Exercise 5a")
        print("5b) Exercise 5b")
        print("6a) Exercise 6a")
        print("6b) Exercise 6b")
        print("7a) Exercise 7a")
        print("7b) Exercise 7b")
        print("8) Exercise 8")
        print("9) Exercise 9")
        print("0) Exit")
        
        choice = input("Select an exercise: ").strip()
        
        if choice == "2a":
            run_2a()
        elif choice == "2b":
            run_2b()
        elif choice == "2cs":
            run_2cs()
        elif choice == "2ci":
            run_2ci()
        elif choice == "3a":
            run_3a()
        elif choice == "3b":
            run_3b()
        elif choice == "4a":
            run_4a()
        elif choice == "4b":
            run_4b()
        elif choice == "5a":
            run_5a()
        elif choice == "5b":
            run_5b()
        elif choice == "6a":
            run_6a()
        elif choice == "6b":
            run_6b()
        elif choice == "7a":
            run_7a()
        elif choice == "7b":
            run_7b()
        elif choice == "8":
            run_8()
        elif choice == "0":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
