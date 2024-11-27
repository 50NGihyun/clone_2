# -*- coding: utf-8 -*-
"""
Interactive Image Segmentation Tool with Exit Fix
"""

import os
import cv2
import numpy as np

# Parameters for drawing
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates of the region
annotations = []  # List to store segmentation points


# Mouse callback function to draw contours
def draw_contour(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        annotations.append([(x, y)])  # Start a new contour

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            annotations[-1].append((x, y))  # Add points to the current contour

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        annotations[-1].append((x, y))  # Close the contour


# Function to display and annotate an image
def segment_image(image_path):
    global annotations
    annotations = []  # Clear annotations for each new image

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return False

    # Create a clone of the image for annotation display
    annotated_image = image.copy()
    cv2.namedWindow("Image Segmentation")
    cv2.setMouseCallback("Image Segmentation", draw_contour)

    print(f"Annotating image: {image_path}")
    while True:
        temp_image = annotated_image.copy()
        for contour in annotations:
            points = np.array(contour, dtype=np.int32)
            cv2.polylines(temp_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        cv2.imshow("Image Segmentation", temp_image)

        # Key press handling
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):  # Save annotations
            save_annotations(image_path, annotations)
            print("Annotations saved.")
        elif key == ord("c"):  # Clear annotations
            annotations.clear()
            annotated_image = image.copy()
            print("Annotations cleared.")
        elif key == ord("q") or key == 27:  # Quit annotation ('q' or ESC)
            print("Exiting annotation for current image.")
            break

    cv2.destroyWindow("Image Segmentation")  # Close the OpenCV window for this image
    return True


# Function to save annotations to a text file
def save_annotations(image_path, annotations):
    with open("annotations.txt", "a") as f:
        f.write(f"Image: {os.path.basename(image_path)}\n")
        for contour in annotations:
            f.write(str(contour) + "\n")
        f.write("\n")  # Separate entries by an empty line


# Function to process images in a directory
def process_images_in_directory(directory_path):
    # Get list of image files
    image_files = [
        os.path.join(directory_path, f)
        for f in os.listdir(directory_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not image_files:
        print("No images found in the specified directory.")
        return

    current_index = 0
    while True:
        image_path = image_files[current_index]
        success = segment_image(image_path)

        if not success:
            break

        print("Press 'n' for next image, 'p' for previous image, or 'ESC' to exit.")
        key = cv2.waitKey(0) & 0xFF
        if key == ord("n"):  # Next image
            current_index = (current_index + 1) % len(image_files)
        elif key == ord("p"):  # Previous image
            current_index = (current_index - 1) % len(image_files)
        elif key == 27:  # ESC key
            print("Exiting program.")
            break

    cv2.destroyAllWindows()  # Ensure all windows are closed


# Main entry point
if __name__ == "__main__":
    directory_path = r"C:\Users\cic\Documents\clone_2\Image_dataset"
    process_images_in_directory(directory_path)
