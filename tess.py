from pdf2image import convert_from_path
import pytesseract

# Set the Tesseract OCR executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text

pdf_text = extract_text_from_pdf("sample.pdf")
print(pdf_text)
