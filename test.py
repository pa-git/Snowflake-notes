import cv2
import numpy as np
import pytesseract
from pytesseract import Output

# Set Tesseract OCR Path (only needed for Windows users)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Step 1: Denoising
    image = cv2.fastNlMeansDenoising(image, h=30)

    # Step 2: Contrast Enhancement (Histogram Equalization)
    image = cv2.equalizeHist(image)

    # Step 3: Adaptive Thresholding (Binarization)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)

    # Step 4: Deskewing (Skew Correction)
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    image = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return image

def extract_text(image):
    # Configure Tesseract for better accuracy on tabular data
    custom_config = r'--oem 3 --psm 6'  # psm 6 treats the image as a block of text
    text = pytesseract.image_to_string(image, config=custom_config)
    
    return text

def main(image_path):
    preprocessed_image = preprocess_image(image_path)
    
    # Save the processed image (for debugging)
    cv2.imwrite("processed_image.png", preprocessed_image)

    extracted_text = extract_text(preprocessed_image)

    print("Extracted Text:")
    print(extracted_text)

if __name__ == "__main__":
    image_path = "table_image.jpg"  # Change this to your actual image path
    main(image_path)
