from PIL import Image, ImageTk
import cv2
import numpy as np
import argparse
import os

# Load the HED model files
PROTO_PATH = "deploy.prototxt"
MODEL_PATH = "hed_pretrained_bsds.caffemodel"

if not os.path.exists(PROTO_PATH) or not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("HED model files not found! Ensure 'deploy.prototxt' and 'hed_pretrained_bsds.caffemodel' are in the project folder.")

# Load the HED model
net = cv2.dnn.readNetFromCaffe(PROTO_PATH, MODEL_PATH)

def detect_edges(input_path, output_path="edges.png"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image '{input_path}' not found!")

    # Load the input image
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError(f"Failed to read image '{input_path}'. Check if the file is accessible.")

    (H, W) = image.shape[:2]

    # Convert to blob and forward pass through the network
    blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(W, H),
                                 mean=(104.00698793, 116.66876762, 122.67891434),
                                 swapRB=False, crop=False)

    net.setInput(blob)
    edges = net.forward()

    # Normalize and convert to 8-bit image
    edges = (255 * edges[0, 0]).astype("uint8")

    # Save the result
    cv2.imwrite(output_path, edges)
    print(f"Edge-detected image saved as '{output_path}'")

if __name__ == "__main__":
    # Default input image
    input_image = "your_image.jpg"  # Ensure this exists in the project folder

    # Run edge detection
    detect_edges(input_image)
