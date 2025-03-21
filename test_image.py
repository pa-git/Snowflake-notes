import cv2
import numpy as np
import pytesseract

# Load image in grayscale
image_path = "your_image_path_here.png"
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

# Detect regions where text is white on black
# We assume those areas are darker than a threshold
inverted_regions = thresh < 128  # Identify dark regions
thresh[inverted_regions] = 255 - thresh[inverted_regions]  # Invert only those regions

# Optional: Dilate to make text thicker
kernel = np.ones((2, 2), np.uint8)
thresh = cv2.dilate(thresh, kernel, iterations=1)

# Perform OCR on the processed image
text = pytesseract.image_to_string(thresh, config="--psm 6")

# Show the processed image
cv2.imshow("Processed Image", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print OCR result
print(text)
