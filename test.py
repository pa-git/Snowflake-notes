import cv2
import numpy as np
import pytesseract

def preprocess_image(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Step 1: Denoising
    image = cv2.fastNlMeansDenoising(image, h=30)

    # Step 2: Detect potential white text on light background
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary_inv = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)  # Detect light areas

    # Step 3: Invert regions with low contrast (i.e., potential headers)
    mask = binary_inv  # Areas where text might be white
    inverted = cv2.bitwise_not(image)  # Invert the whole image
    image[mask == 255] = inverted[mask == 255]  # Apply inversion only where needed

    # Step 4: Contrast Enhancement
    image = cv2.equalizeHist(image)

    # Step 5: Adaptive Thresholding (Binarization)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)

    return image

def extract_text(image):
    # Configure Tesseract for better table recognition
    custom_config = r'--oem 3 --psm 6'  # psm 6 treats the image as a block of text
    text = pytesseract.image_to_string(image, config=custom_config)
    
    return text

def main(image_path):
    preprocessed_image = preprocess_image(image_path)
    
    # Save the processed image for debugging
    cv2.imwrite("processed_image.png", preprocessed_image)

    extracted_text = extract_text(preprocessed_image)

    print("Extracted Text:")
    print(extracted_text)

if __name__ == "__main__":
    image_path = "table_image.jpg"  # Change this to your actual image path
    main(image_path)
