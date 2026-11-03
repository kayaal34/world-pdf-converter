"""Word to PDF Converter Module"""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)

LIBREOFFICE_TIMEOUT = 120

# LibreOffice PATH'te değilse Windows'taki varsayılan kurulum yerlerine bakılır
LIBREOFFICE_PATHS = [
    Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "LibreOffice" / "program" / "soffice.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "LibreOffice" / "program" / "soffice.exe",
]


def unique_output_path(folder, stem: str) -> Path:
    """Return folder/stem.pdf, or stem_1.pdf, stem_2.pdf ... if it already exists"""
    output_file = Path(folder) / f"{stem}.pdf"
    counter = 1
    while output_file.exists():
        output_file = Path(folder) / f"{stem}_{counter}.pdf"
        counter += 1
    return output_file


def find_libreoffice():
    """Return the path of the LibreOffice executable, or None"""
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for path in LIBREOFFICE_PATHS:
        if path.exists():
            return str(path)
    return None


def convert_with_word(word_file_path: str, pdf_file_path: str):
    """Convert using Microsoft Word through docx2pdf"""
    from docx2pdf import convert
    convert(word_file_path, pdf_file_path)


def convert_with_libreoffice(word_file_path: str, pdf_file_path: str):
    """Convert using LibreOffice in headless mode"""
    soffice = find_libreoffice()
    if soffice is None:
        raise RuntimeError("LibreOffice bulunamadı")

    # LibreOffice çıktı adını kendisi seçer; geçici klasöre yazıp hedefe taşıyoruz
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", temp_dir, word_file_path],
            check=True,
            capture_output=True,
            timeout=LIBREOFFICE_TIMEOUT,
        )
        produced = Path(temp_dir) / f"{Path(word_file_path).stem}.pdf"
        if not produced.exists():
            raise RuntimeError("LibreOffice PDF oluşturmadı")
        shutil.move(str(produced), pdf_file_path)


class WordToPDFConverter:
    """Convert Word documents to PDF format"""

    # Önce Word denenir, olmazsa LibreOffice
    backends = (
        ("Microsoft Word", convert_with_word),
        ("LibreOffice", convert_with_libreoffice),
    )

    def __init__(self):
        self.last_error = None

    def convert(self, word_file_path: str, pdf_file_path: str) -> bool:
        """
        Convert a Word document to PDF

        Args:
            word_file_path: Path to the input Word document
            pdf_file_path: Path to save the output PDF

        Returns:
            bool: True if conversion successful, False otherwise
        """
        self.last_error = None
        if not os.path.isfile(word_file_path):
            self.last_error = f"Dosya bulunamadı: {word_file_path}"
            return False

        # Ensure output directory exists
        Path(pdf_file_path).parent.mkdir(parents=True, exist_ok=True)

        errors = []
        for name, backend in self.backends:
            try:
                backend(word_file_path, pdf_file_path)
            except Exception as e:
                errors.append(f"{name}: {e}")
                continue

            # Verify file was created
            if os.path.exists(pdf_file_path):
                logger.info("Dönüştürme başarılı (%s): %s", name, pdf_file_path)
                return True
            errors.append(f"{name}: PDF dosyası oluşturulamadı")

        self.last_error = "\n".join(errors)
        logger.error("Dönüştürme başarısız: %s", self.last_error)
        return False
