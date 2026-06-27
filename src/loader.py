from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

import pytesseract
from pdf2image import convert_from_path


def load_pdf(pdf_path):

    # First try normal text extraction
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Check if text was extracted
    extracted_text = ""

    for doc in documents:
        extracted_text += doc.page_content.strip()

    # If text exists, return normal documents
    if extracted_text != "":
        print("Normal PDF detected.")
        return documents

    # If no text, use OCR
    print("Scanned PDF detected. Running OCR...")

    # Tesseract installation path
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    # Convert PDF pages to images using Poppler
    images = convert_from_path(
        pdf_path,
        poppler_path=r"C:\Users\shris\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    )

    ocr_documents = []

    for i, image in enumerate(images):

        text = pytesseract.image_to_string(image)

        ocr_documents.append(
            Document(
                page_content=text,
                metadata={"page": i}
            )
        )

    return ocr_documents