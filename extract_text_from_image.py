import cv2
import os
import pytesseract
import numpy as np

# Function to preprocess and extract text from image (for images with '_orange' suffix)
def extract_text_from_image_proc(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    alpha = 2.5  # Fine-tuned contrast
    beta = -100  # Fine-tuned brightness
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

    # Apply denoising
    denoised = cv2.fastNlMeansDenoising(adjusted, None, 30, 7, 21)

    # Apply a threshold to create a binary image
    _, binary = cv2.threshold(denoised, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the image (black text on white background)
    inverted = cv2.bitwise_not(binary)

    # Apply morphological operations to reduce noise
    kernel = np.ones((1, 1), np.uint8)  # Smaller kernel size
    morph = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel)

    # Invert again to get black text on white background
    final_image = cv2.bitwise_not(morph)

    # Use pytesseract to extract text from the preprocessed image
    extracted_text = pytesseract.image_to_string(final_image, lang='fra', config='--oem 3 --psm 1')

    return extracted_text

# Function to extract text from image (for images without '_orange' suffix)
def extract_text_from_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Extract text using pytesseract
    extracted_text = pytesseract.image_to_string(image, config='--oem 3 --psm 1')

    return extracted_text

# Function to process all images in a folder and save the extracted text to corresponding files
def process_images_in_folder(input_folder, text_output_folder):
    if not os.path.exists(text_output_folder):
        os.makedirs(text_output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image file extensions
            image_path = os.path.join(input_folder, filename)
            
            # Check if the image filename ends with '_orange' before the extension
            if filename.rsplit('.', 1)[0].endswith('_orange'):
                extracted_text = extract_text_from_image_proc(image_path)
            else:
                extracted_text = extract_text_from_image(image_path)

            # Save the extracted text to a corresponding text file
            text_filename = os.path.splitext(filename)[0] + '.txt'
            text_file_path = os.path.join(text_output_folder, text_filename)
            
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(extracted_text)

# Specify the input and output folders
input_folder = 'invoices'
text_output_folder = 'text_invoices'

# Process the images
process_images_in_folder(input_folder, text_output_folder)
