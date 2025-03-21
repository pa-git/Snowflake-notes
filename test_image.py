import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Preprocesses an image to enhance text visibility for OCR.
    Ensures that all text is black on a white background.
    
    :param image_path: Path to the input image.
    :return: Processed image ready for OCR.
    """
    # Load image in grayscale
    im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply median blur to remove uneven background illumination
    bg = cv2.medianBlur(im, 51)
    out = 255 - cv2.absdiff(bg, im)

    # Apply CLAHE to enhance local contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    out = clahe.apply(out)

    # Binarize the image using adaptive thresholding
    thresh = cv2.adaptiveThreshold(out, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)

    # Detect and invert only white-on-black text regions
    inverted_regions = thresh < 128  # Identify dark regions
    thresh[inverted_regions] = 255 - thresh[inverted_regions]  # Invert only those regions

    return thresh
