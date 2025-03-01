import os

image_path = "your_image.jpg"
if not os.path.exists(image_path):
    print(f"Error: File '{image_path}' not found!")
else:
    print(f"File '{image_path}' found.")
