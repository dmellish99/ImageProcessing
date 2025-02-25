# Image Processing Exercises – Morphological Operations

This repository contains a series of image processing exercises focused on morphological operations such as thresholding, dilation, erosion, opening, closing, and noise filtering. All exercises are implemented in Python using custom functions without relying on OpenCV's built-in morphology functions. These exercises were developed as part of the Image Processing course.

## Repository Structure Overview

Each exercise is organized into its own folder. Within every exercise folder, there is a **src** subfolder that contains the input files specific to that exercise, and an **output** subfolder where the resulting files (images or text files) are saved. In addition, a central main module (`main.py`) is provided to launch the exercises from a menu.

## 🚀 Running the Exercises
You can run the central `main.py` file to launch exercises from a menu:

```bash
python main.py
```

When you run main.py:
- Each exercise will run using its default parameters if no command-line arguments are provided.
- To supply custom parameters, run the corresponding exercise module directly 

## 🛠️ Custom Functions
This repository uses custom implementations for the following morphological operations instead of OpenCV's built-in functions, which was an objective of the course:
- Custom Erosion and Dilation (Exercise 3):
- Custom Opening (Exercise 4a):
- Custom Closing (Exercise 4b):

These custom functions are used in later exercises to evaluate idempotence and filter performance.