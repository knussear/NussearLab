#!/usr/bin/env python3
"""
Helper script to convert publication data from CSV or BibTeX to HTML format for the Nussear Lab website.

Usage:
    python3 import_publications.py publications.csv
    python3 import_publications.py publications.bib

CSV Format:
    year,title,authors,journal,doi,pdf_url
    2024,Title Here,"Author A., Nussear K.",Journal Name,https://doi.org/...,

BibTeX Format:
    Standard BibTeX format from citation managers (Zotero, Mendeley, EndNote, etc.)

Output:
    Creates publications_output.html with formatted publication entries
"""

import csv
import sys
import html
import re


def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(text)


def parse_bibtex(content):
    """Parse BibTeX content and return list of publication dicts"""
    publications = []
    
    # Split into individual entries
    entries = re.findall(r'@\w+\{[^@]+\}', content, re.DOTALL)
    
    for entry in entries:
        pub = {}
        
        # Extract year
        year_match = re.search(r'year\s*=\s*[{"\']?(\d{4})[}"\']?', entry, re.IGNORECASE)
        if year_match:
            pub['year'] = year_match.group(1)
        
        # Extract title
        title_match = re.search(r'title\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE)
        if title_match:
            # Clean up title - remove extra braces and LaTeX commands
            title = title_match.group(1)
            title = re.sub(r'[{}]', '', title)
            title = re.sub(r'\\[a-zA-Z]+', '', title)
            pub['title'] = title.strip()
        
        # Extract authors
        author_match = re.search(r'author\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE)
        if author_match:
            authors = author_match.group(1)
            # Clean up author format
            authors = re.sub(r'\s+and\s+', ', ', authors)
            authors = re.sub(r'[{}]', '', authors)
            pub['authors'] = authors.strip()
        
        # Extract journal/booktitle
        journal_match = re.search(r'(?:journal|booktitle)\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE)
        if journal_match:
            journal = journal_match.group(1)
            journal = re.sub(r'[{}]', '', journal)
            pub['journal'] = journal.strip()
        
        # Extract volume
        volume_match = re.search(r'volume\s*=\s*[{"\']?(\d+)[}"\']?', entry, re.IGNORECASE)
        
        # Extract number/issue
        number_match = re.search(r'number\s*=\s*[{"\']?(\d+)[}"\']?', entry, re.IGNORECASE)
        
        # Extract pages
        pages_match = re.search(r'pages\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE)
        
        # Combine journal info with volume/issue/pages
        if pub.get('journal'):
            if volume_match:
                pub['journal'] += f", {volume_match.group(1)}"
                if number_match:
                    pub['journal'] += f"({number_match.group(1)})"
            if pages_match:
                pub['journal'] += f", {pages_match.group(1)}"
        
        # Extract DOI
        doi_match = re.search(r'doi\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE)
        if doi_match:
            doi = doi_match.group(1).strip()
            if not doi.startswith('http'):
                doi = f"https://doi.org/{doi}"
            pub['doi'] = doi
        
        # Extract URL (for PDF)
        url_match = re.search(r'url\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE)
        if url_match:
            pub['pdf_url'] = url_match.group(1).strip()
        
        # Only add if we have minimum required fields
        if pub.get('year') and pub.get('title'):
            publications.append(pub)
    
    return publications


def format_publication(pub):
    """Convert a publication dict to HTML format"""
    year = escape_html(pub.get('year', ''))
    title = escape_html(pub.get('title', ''))
    authors = escape_html(pub.get('authors', ''))
    journal = escape_html(pub.get('journal', ''))
    doi = pub.get('doi', '').strip()
    pdf_url = pub.get('pdf_url', '').strip()
    
    html_output = f'''            <div class="publication" data-year="{year}">
                <h3 class="pub-title">{title}</h3>
                <p class="pub-authors">{authors}</p>
                <p class="pub-journal"><em>{journal}</em></p>
                <p class="pub-year">{year}</p>'''
    
    # Add links if available
    if doi or pdf_url:
        html_output += '\n                <div class="pub-links">'
        if doi:
            html_output += f'\n                    <a href="{doi}" class="pub-link" target="_blank" rel="noopener">DOI</a>'
        if pdf_url:
            html_output += f'\n                    <a href="{pdf_url}" class="pub-link" target="_blank" rel="noopener">PDF</a>'
        html_output += '\n                </div>'
    
    html_output += '\n            </div>\n'
    return html_output


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 import_publications.py <file>")
        print("\nSupported formats:")
        print("  - CSV: publications.csv")
        print("  - BibTeX: publications.bib")
        print("\nCSV Format:")
        print("year,title,authors,journal,doi,pdf_url")
        print('2024,"Title","Author A., Nussear K.","Journal Name","https://doi.org/...","https://..."')
        print("\nBibTeX Format:")
        print("Standard BibTeX format from citation managers")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "publications_output.html"
    
    try:
        # Detect file format
        is_bibtex = input_file.lower().endswith('.bib')
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        if is_bibtex:
            print("Detected BibTeX format...")
            publications = parse_bibtex(content)
        else:
            print("Detected CSV format...")
            # Parse CSV
            import io
            csvfile = io.StringIO(content)
            reader = csv.DictReader(csvfile)
            publications = []
            
            for row in reader:
                if row.get('year') and row.get('title'):
                    publications.append(row)
        
        if not publications:
            print("Warning: No valid publications found in the input file")
            sys.exit(1)
        
        # Sort by year (newest first)
        publications.sort(key=lambda x: int(x.get('year', 0)), reverse=True)
        
        # Generate HTML
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("<!-- Copy the content below into publications.html -->\n")
            outfile.write("<!-- Paste inside the <section class=\"publications-list\" id=\"publications-container\"> section -->\n\n")
            
            for pub in publications:
                outfile.write(format_publication(pub))
                outfile.write('\n')
            
            outfile.write("<!-- End of generated publications -->\n")
        
        print(f"✓ Successfully converted {len(publications)} publications")
        print(f"✓ Output saved to: {output_file}")
        print("\nNext steps:")
        print("1. Open publications_output.html")
        print("2. Copy the generated HTML")
        print("3. Paste into publications.html inside the publications-container section")
        print("4. Remove the sample publications if desired")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        print("\nSupported formats: CSV (.csv) and BibTeX (.bib)")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
