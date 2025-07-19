import argparse
import os
import pypandoc
from ebooklib import epub
from fpdf import FPDF, HTMLMixin
from pathlib import Path
import webbrowser
import tempfile
import urllib.request
from fpdf.enums import XPos, YPos
import re
from PIL import Image

# === CONFIGURATION ===
BOOK_DIR = Path("book")
COVER_IMAGE = BOOK_DIR / "cover.png"

# Book metadata
BOOK_TITLE = "Mastering ETL Pipelines for Data Science Workflows"
AUTHOR = "Pankaj Nagar"
LANGUAGE = "en"
IDENTIFIER = "urn:isbn:9780000000001"
PUBLISHER = "Independent Publishing"

# Ensure pandoc is available
try:
    pypandoc.get_pandoc_version()
except OSError:
    print("Pandoc not found. Downloading pandoc...")
    pypandoc.download_pandoc()

def get_chapter_files():
    """Get all markdown files from book directory, sorted by name"""
    md_files = list(BOOK_DIR.glob("*.md"))
    # Sort by filename to maintain chapter order
    md_files.sort(key=lambda x: x.name)
    return md_files

def convert_markdown_to_epub(output_file):
    """Convert markdown files to EPUB with cover image"""
    book = epub.EpubBook()
    book.set_identifier(IDENTIFIER)
    book.set_title(BOOK_TITLE)
    book.set_language(LANGUAGE)
    book.add_author(AUTHOR)
    book.add_metadata('DC', 'publisher', PUBLISHER)

    # Add cover image if exists
    if COVER_IMAGE.exists():
        with open(COVER_IMAGE, 'rb') as img_file:
            book.set_cover("cover.png", img_file.read())
        print(f"Cover image added from {COVER_IMAGE}")
    else:
        print("No cover image found in /book")

    chapters = get_chapter_files()
    epub_items = []
    nav_points = []

    for idx, md_file in enumerate(chapters, 1):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert markdown to HTML with better formatting
        html_content = pypandoc.convert_text(content, 'html', format='md')
        
        # Create chapter title from filename
        chapter_title = md_file.stem.replace('_', ' ').title()
        
        chapter = epub.EpubHtml(
            title=f"Chapter {idx}: {chapter_title}",
            file_name=f'chapter_{idx:02d}.xhtml',
            lang=LANGUAGE,
        )
        chapter.content = f"<h1>Chapter {idx}: {chapter_title}</h1><hr/>{html_content}"
        book.add_item(chapter)
        epub_items.append(chapter)
        nav_points.append(chapter)

    # TOC and Navigation
    book.toc = tuple(nav_points)
    book.spine = ['nav'] + epub_items
    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())

    epub.write_epub(output_file, book)
    print(f"EPUB created: {output_file}")

def convert_markdown_to_html(output_file):
    """Convert markdown files to a single HTML file"""
    chapters = get_chapter_files()
    html_content = f"""
<!DOCTYPE html>
<html lang="{LANGUAGE}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{BOOK_TITLE}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
        h2 {{ color: #34495e; }}
        h3 {{ color: #7f8c8d; }}
        code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>{BOOK_TITLE}</h1>
    <p><em>By {AUTHOR}</em></p>
    <hr>
"""
    
    for idx, md_file in enumerate(chapters, 1):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html_chapter = pypandoc.convert_text(content, 'html', format='md')
        chapter_title = md_file.stem.replace('_', ' ').title()
        
        html_content += f"""
    <h2>Chapter {idx}: {chapter_title}</h2>
    {html_chapter}
    <hr>
"""
    
    html_content += """
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML created: {output_file}")
    
    # Open in browser
    try:
        webbrowser.open(f'file://{os.path.abspath(output_file)}')
        print("Opened in browser")
    except:
        print("HTML file created - open manually in browser")

def ensure_font_exists(font_path, url=None):
    os.makedirs(os.path.dirname(font_path), exist_ok=True)
    if not os.path.exists(font_path):
        if url:
            print(f"Font not found at {font_path}. Downloading...")
            try:
                urllib.request.urlretrieve(url, font_path)
                print("Font downloaded successfully.")
            except Exception as e:
                print(f"Failed to download font: {e}")
                raise
        else:
            raise FileNotFoundError(f"Font not found and no download URL provided: {font_path}")

def sanitize_text(text):
    """Replace smart quotes and other problematic characters, and remove encoding artifacts like 'Â'."""
    replacements = {
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2013': '-',
        '\u2014': '--',
        '\u2705': '', # Checkmark emoji
        '\u274c': '', # Cross mark emoji
        '\u26a0': '', # Warning emoji
        '\U0001f4d6': '', # Open book emoji
        '\U0001f310': '', # Globe with meridians emoji
        '\U0001f4c4': '', # Page facing up emoji
        '\U0001f44b': '', # Waving hand emoji
        '\xc2': '', # Remove stray encoding artifact (Â)
        'Â': '', # Remove visible artifact
    }
    for smart, basic in replacements.items():
        text = text.replace(smart, basic)
    return text

def clean_html_for_pdf(html):
    # Remove <style>...</style> and <hr> tags
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<hr\s*/?>', '', html, flags=re.IGNORECASE)
    return html

class MyFPDF(FPDF, HTMLMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html_font = 'DejaVu'
        self._in_pre = False
        self._in_inline_code = False
        self._in_list = False
        self._list_type = None
        self._list_count = 0
        self._list_indent = 0

    def _font_family_for_tag(self, tag):
        if tag in ['code', 'pre']:
            return 'DejaVu'
        return super()._font_family_for_tag(tag)

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.ln(3)
            self.set_font('DejaVu', '', 11)
            self.set_fill_color(245, 245, 245)
            self.set_draw_color(200, 200, 200)
            self.set_text_color(40, 40, 40)
            self.set_x(self.l_margin + self._list_indent)
            self.cell(0, 2, '', ln=1)
            self.set_x(self.l_margin + self._list_indent + 2)
            self.multi_cell(0, 6, '', border='TLR', fill=True)
            self.set_x(self.l_margin + self._list_indent + 4)
            self._in_pre = True
        elif tag == 'code' and not self._in_pre:
            self.set_font('DejaVu', '', 11)
            self.set_fill_color(235, 235, 235)
            self.set_draw_color(200, 200, 200)
            self.set_text_color(60, 60, 60)
            self.set_x(self.get_x() + 1)
            self._in_inline_code = True
        elif tag == 'p':
            self.ln(2)
        elif tag in ['ul', 'ol']:
            self._in_list = True
            self._list_type = tag
            self._list_count = 0
            self._list_indent += 6
            self.ln(2)
        elif tag == 'li':
            self._list_count += 1
            self.ln(1)
            self.set_x(self.l_margin + self._list_indent)
            # Only print marker, no extra characters
            if self._list_type == 'ul':
                self.cell(6, 6, u'•', ln=0)
            elif self._list_type == 'ol':
                self.cell(6, 6, f'{self._list_count}.', ln=0)
        else:
            super().handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.cell(0, 2, '', ln=1)
            self.set_x(self.l_margin + self._list_indent + 2)
            self.multi_cell(0, 2, '', border='BLR', fill=True)
            self.set_x(self.l_margin + self._list_indent)
            self.set_text_color(0, 0, 0)
            self.set_fill_color(255, 255, 255)
            self._in_pre = False
            self.ln(3)
        elif tag == 'code' and self._in_inline_code:
            self.set_text_color(0, 0, 0)
            self.set_fill_color(255, 255, 255)
            self._in_inline_code = False
        elif tag == 'p':
            self.ln(4)
        elif tag in ['ul', 'ol']:
            self._in_list = False
            self._list_type = None
            self._list_count = 0
            self._list_indent -= 6
            self.ln(2)
        elif tag == 'li':
            self.ln(2)
        else:
            super().handle_endtag(tag)

    def handle_data(self, data):
        if self._in_pre:
            # Preserve all leading whitespace for code blocks
            lines = data.split('\n')
            for line in lines:
                self.set_x(self.l_margin + self._list_indent + 4)
                # Use a monospaced font and preserve indentation
                self.cell(0, 6, line.expandtabs(), ln=1)
        elif self._in_inline_code:
            self.cell(self.get_string_width(data) + 2, 6, data, border=1, ln=0, fill=True)
        else:
            # Remove stray encoding artifacts from normal text
            clean_data = data.replace('Â', '').replace('\xc2', '')
            super().handle_data(clean_data)

def convert_markdown_to_pdf(output_file):
    pdf = MyFPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.default_encoding = 'utf-8'
    pdf.core_fonts_encoding = 'utf-8'

    # Add Unicode font
    font_path = "fonts/DejaVu Sans/"
    pdf.add_font('DejaVu', '', font_path + 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', 'B', font_path + 'DejaVuSans-Bold.ttf')
    pdf.add_font('DejaVu', 'I', font_path + 'DejaVuSans-Oblique.ttf')
    pdf.add_font('DejaVu', 'BI', font_path + 'DejaVuSans-BoldOblique.ttf')

    # 1. Cover page
    cover_path = os.path.join("book", "cover.png")
    if os.path.exists(cover_path):
        pdf.add_page()
        # --- Fit cover image to A4 page (210x297mm) ---
        a4_width, a4_height = 210, 297
        with Image.open(cover_path) as img:
            img_w, img_h = img.size
            # Convert px to mm using 72 dpi (FPDF default)
            dpi = img.info.get('dpi', (72, 72))[0]
            img_w_mm = img_w * 25.4 / dpi
            img_h_mm = img_h * 25.4 / dpi
            scale = min(a4_width / img_w_mm, a4_height / img_h_mm)
            disp_w = img_w_mm * scale
            disp_h = img_h_mm * scale
            x = (a4_width - disp_w) / 2
            y = (a4_height - disp_h) / 2
        pdf.image(cover_path, x=x, y=y, w=disp_w, h=disp_h)
        pdf.ln(a4_height)  # Move to next page

    # 2. Table of Contents page (reserve it right after cover)
    pdf.add_page()
    toc_page = pdf.page_no()
    # Don't write TOC yet, just reserve the page

    # 3. Chapters
    chapters = get_chapter_files()
    toc_entries = []
    for idx, md_file in enumerate(chapters, 1):
        pdf.add_page()
        chapter_title = md_file.stem.replace('_', ' ').title()
        toc_entries.append((chapter_title, pdf.page_no()))

        # Convert markdown to HTML
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = pypandoc.convert_text(md_content, 'html', format='md')
        sanitized_html = sanitize_text(html_content)
        cleaned_html = clean_html_for_pdf(sanitized_html)

        pdf.set_font("DejaVu", '', 12)
        pdf.write_html(cleaned_html)

    # 4. Go back to TOC page and write TOC
    pdf.page = toc_page
    pdf.set_font("DejaVu", 'B', 18)
    pdf.cell(0, 10, "Table of Contents", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)
    pdf.set_font("DejaVu", '', 12)
    for title, page in toc_entries:
        clean_title = title.replace('\x95', '').replace('•', '')  # Remove problematic bullet chars
        pdf.cell(0, 8, f"{clean_title} .......... {page}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # 5. Output
    pdf.output(output_file)
    print(f"PDF created: {output_file}")

def convert_markdown_to_combined_markdown(output_file):
    """Combine all markdown files into a single markdown file"""
    chapters = get_chapter_files()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header
        outfile.write(f"# {BOOK_TITLE}\n\n")
        outfile.write(f"*By {AUTHOR}*\n\n")
        outfile.write("---\n\n")
        
        # Write each chapter
        for idx, md_file in enumerate(chapters, 1):
            chapter_title = md_file.stem.replace('_', ' ').title()
            outfile.write(f"## Chapter {idx}: {chapter_title}\n\n")
            
            with open(md_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write("\n\n---\n\n")
    
    print(f"Combined Markdown created: {output_file}")

def show_format_menu():
    """Show available output formats"""
    print("\nAvailable Output Formats:")
    print("1. EPUB (eBook format for Kindle, etc.)")
    print("2. HTML (Web format, opens in browser)")
    print("3. PDF (Portable Document Format)")
    print("4. Combined Markdown (Single markdown file)")
    print("5. All formats")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nSelect format (0-5): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5']:
                return choice
            else:
                print("Please enter a number between 0-5")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit(0)

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown files to various eBook formats.')
    parser.add_argument('-f', '--format', choices=['epub', 'html', 'pdf', 'md', 'all'], 
                       help='Output format (if not specified, interactive menu will be shown)')
    parser.add_argument('-o', '--output', help='Output file name (optional)')
    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Check if book directory exists
    if not BOOK_DIR.exists():
        print(f"Book directory '{BOOK_DIR}' not found!")
        print("Please ensure you have a 'book' folder with your markdown files.")
        return

    # Get chapter files
    chapters = get_chapter_files()
    if not chapters:
        print(f"No markdown files found in '{BOOK_DIR}'!")
        return

    print(f"Found {len(chapters)} chapters:")
    for chapter in chapters:
        print(f"   - {chapter.name}")

    # Determine format and output file
    if args.format:
        format_choice = args.format
    else:
        format_choice = show_format_menu()
        if format_choice == '0':
            return

    # Generate output filename if not provided
    if not args.output or args.output is None:
        base_name = BOOK_TITLE.lower().replace(' ', '_').replace(':', '').replace('-', '_')
        if format_choice == 'epub' or format_choice == '1':
            args.output = f"{base_name}.epub"
        elif format_choice == 'html' or format_choice == '2':
            args.output = f"{base_name}.html"
        elif format_choice == 'pdf' or format_choice == '3':
            args.output = f"{base_name}.pdf"
        elif format_choice == 'md' or format_choice == '4':
            args.output = f"{base_name}_combined.md"
        elif format_choice == 'all' or format_choice == '5':
            args.output = base_name

    # Prepend output directory to output file(s)
    def out_path(filename):
        return os.path.join(output_dir, filename)

    # Convert based on choice
    if format_choice == '1' or format_choice == 'epub':
        convert_markdown_to_epub(out_path(args.output))
    elif format_choice == '2' or format_choice == 'html':
        convert_markdown_to_html(out_path(args.output))
    elif format_choice == '3' or format_choice == 'pdf':
        convert_markdown_to_pdf(out_path(args.output))
    elif format_choice == '4' or format_choice == 'md':
        convert_markdown_to_combined_markdown(out_path(args.output))
    elif format_choice == '5' or format_choice == 'all':
        base_name = args.output
        convert_markdown_to_epub(out_path(f"{base_name}.epub"))
        convert_markdown_to_html(out_path(f"{base_name}.html"))
        convert_markdown_to_pdf(out_path(f"{base_name}.pdf"))
        convert_markdown_to_combined_markdown(out_path(f"{base_name}_combined.md"))
        print(f"All formats created with base name: {base_name}")

if __name__ == '__main__':
    main() 