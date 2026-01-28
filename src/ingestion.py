import os
import pdfplumber
import docx
from typing import Optional

class ResumeIngestor:
    """
    Handles ingestion of resumes from various formats.
    """

    def extract_text(self, file_path: str) -> str:
        """
        Extracts text from a file based on extension.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif ext == '.docx':
            return self._extract_from_docx(file_path)
        elif ext == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _extract_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # extract_text(x_tolerance=1, y_tolerance=1) helps with layout
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error parsing PDF {file_path}: {e}")
            # Fallback could be added here
        return text

    def _extract_from_docx(self, file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Error parsing DOCX {file_path}: {e}")
            return ""

    def _extract_from_txt(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error parsing TXT {file_path}: {e}")
            return ""
