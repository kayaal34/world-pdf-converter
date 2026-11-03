"""GUI Application for Word to PDF Converter"""
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from converter import WordToPDFConverter, unique_output_path
import os
import sys
import threading


class WordPDFConverterApp:
    """GUI Application for converting Word documents to PDF"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Word to PDF Dönüştürücü")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # Set window icon (if available)
        try:
            icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(icon_path)
        except tk.TclError:
            pass
        
        self.converter = WordToPDFConverter()
        self.selected_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="Word to PDF Dönüştürücü",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white',
            pady=15
        )
        title_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File selection section
        file_section = tk.LabelFrame(
            content_frame,
            text="Dosya Seçimi",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        file_section.pack(fill=tk.X, pady=(0, 15))
        
        # Selected file display
        self.file_label = tk.Label(
            file_section,
            text="Dosya seçilmedi",
            font=('Arial', 10),
            bg='#ecf0f1',
            fg='#7f8c8d',
            wraplength=400,
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        self.file_label.pack(fill=tk.X)
        
        # Browse button
        browse_btn = tk.Button(
            file_section,
            text="Word Dosyası Seç (.docx)",
            command=self.select_file,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=8,
            cursor='hand2'
        )
        browse_btn.pack(pady=10)
        
        # Conversion section
        convert_section = tk.LabelFrame(
            content_frame,
            text="Dönüştürme",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        convert_section.pack(fill=tk.X, pady=(0, 15))
        
        # Output location info
        output_info = tk.Label(
            convert_section,
            text="Microsoft Word veya LibreOffice gereklidir\nPDF, İndirilenler klasörüne kaydedilir",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        output_info.pack()
        
        # Convert button
        self.convert_btn = tk.Button(
            convert_section,
            text="PDF'ye Dönüştür",
            command=self.convert_to_pdf,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.convert_btn.pack(pady=15)
        
        # Status section
        status_section = tk.LabelFrame(
            content_frame,
            text="Durum",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        status_section.pack(fill=tk.BOTH, expand=True)
        
        # Status text
        self.status_text = tk.Text(
            status_section,
            font=('Arial', 9),
            bg='#ecf0f1',
            fg='#2c3e50',
            height=8,
            state=tk.DISABLED
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(status_section, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
    
    def select_file(self):
        """Open file dialog to select a Word document"""
        file_path = filedialog.askopenfilename(
            title="Word Dosyası Seçin",
            filetypes=[("Word Dosyaları", "*.docx"), ("Tüm Dosyalar", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            file_name = Path(file_path).name
            self.file_label.config(
                text=f"Seçilen Dosya: {file_name}",
                fg='#27ae60'
            )
            self.add_status(f"✓ Dosya seçildi: {file_name}")
    
    def convert_to_pdf(self):
        """Convert selected Word document to PDF"""
        if not self.selected_file:
            messagebox.showerror("Hata", "Lütfen önce bir Word dosyası seçin!")
            return
        
        # Get downloads folder
        downloads_folder = Path.home() / "Downloads"
        output_file = unique_output_path(downloads_folder, Path(self.selected_file).stem)

        self.add_status("⏳ Dönüştürme başlatılıyor...")
        self.convert_btn.config(state=tk.DISABLED)

        # Dönüştürme uzun sürebilir; arayüz donmasın diye ayrı thread'de çalışır
        threading.Thread(
            target=self._convert_worker,
            args=(self.selected_file, output_file),
            daemon=True
        ).start()

    def _convert_worker(self, input_file, output_file):
        """Run the conversion off the UI thread"""
        try:
            success = self.converter.convert(input_file, str(output_file))
            error = self.converter.last_error
        except Exception as e:
            success, error = False, str(e)
        # Tkinter'a sadece ana thread'den dokunulur
        self.root.after(0, self._conversion_finished, success, output_file, error)

    def _conversion_finished(self, success, output_file, error):
        """Show the result of a conversion"""
        self.convert_btn.config(state=tk.NORMAL)

        if success:
            self.add_status(f"✓ Dönüştürme başarılı!")
            self.add_status(f"✓ Dosya kaydedildi: {output_file}")

            # Ask to open file
            if messagebox.askyesno(
                "Başarı",
                f"PDF dosyası başarıyla oluşturuldu!\n\n{output_file}\n\nDosyayı açmak ister misiniz?"
            ):
                os.startfile(str(output_file))
                self.add_status("✓ Dosya açılıyor...")
        else:
            self.add_status("✗ Dönüştürme başarısız oldu!")
            if error:
                self.add_status(error)
            messagebox.showerror("Hata", f"Dönüştürme sırasında bir hata oluştu!\n\n{error or ''}")

    def add_status(self, message):
        """Add status message to status text"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = WordPDFConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
