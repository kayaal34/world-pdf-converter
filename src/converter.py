"""Word to PDF Converter Module"""
from pathlib import Path
import os
from docx2pdf import convert


class WordToPDFConverter:
    """Convert Word documents to PDF format"""
    
    def __init__(self):
        pass
    
    def convert(self, word_file_path: str, pdf_file_path: str) -> bool:
        """
        Convert a Word document to PDF
        
        Args:
            word_file_path: Path to the input Word document
            pdf_file_path: Path to save the output PDF
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_dir = Path(pdf_file_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert using docx2pdf (uses LibreOffice backend)
            output_folder = str(output_dir)
            convert(word_file_path, pdf_file_path)
            
            # Verify file was created
            if os.path.exists(pdf_file_path):
                print(f"✓ Dönüştürme başarılı: {pdf_file_path}")
                return True
            else:
                print("Hata: PDF dosyası oluşturulamadı")
                return False
            
        except Exception as e:
            print(f"Error converting document: {str(e)}")
            return False
