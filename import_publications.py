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
    
    # Split into individual entries - handle nested braces
    # Find all @type{...} blocks, accounting for nested braces
    entries = []
    i = 0
    while i < len(content):
        # Look for @ followed by entry type
        match = re.search(r'@(\w+)\s*\{', content[i:])
        if not match:
            break
        
        start = i + match.start()
        brace_start = i + match.end() - 1  # Position of opening brace
        
        # Find matching closing brace
        brace_count = 1
        j = brace_start + 1
        while j < len(content) and brace_count > 0:
            if content[j] == '{':
                brace_count += 1
            elif content[j] == '}':
                brace_count -= 1
            j += 1
        
        if brace_count == 0:
            entries.append(content[start:j])
            i = j
        else:
            # Malformed entry, skip
            i = brace_start + 1
    
    def extract_field(entry, field_name):
        """Extract a field value from a BibTeX entry, handling nested braces"""
        # Match field = {value} or field = "value"
        pattern = rf'{field_name}\s*=\s*([{{"])'
        match = re.search(pattern, entry, re.IGNORECASE)
        if not match:
            return None
        
        delimiter = match.group(1)
        start_pos = match.end() - 1
        
        if delimiter == '{':
            # Handle nested braces
            brace_count = 1
            i = start_pos + 1
            while i < len(entry) and brace_count > 0:
                if entry[i] == '{':
                    brace_count += 1
                elif entry[i] == '}':
                    brace_count -= 1
                i += 1
            if brace_count == 0:
                return entry[start_pos + 1:i - 1].strip()
        else:  # delimiter == '"'
            # Find closing quote
            end_pos = entry.find('"', start_pos + 1)
            if end_pos != -1:
                return entry[start_pos + 1:end_pos].strip()
        
        return None
    
    for entry in entries:
        pub = {}
        
        # Extract year
        year_str = extract_field(entry, 'year')
        if year_str:
            year_match = re.search(r'(\d{4})', year_str)
            if year_match:
                pub['year'] = year_match.group(1)
        
        # Extract title
        title = extract_field(entry, 'title')
        if title:
            # Clean up title - remove extra braces and LaTeX commands
            # Remove all braces (repeat to handle nested braces)
            while '{' in title or '}' in title:
                title = re.sub(r'\{([^{}]*)\}', r'\1', title)
            title = re.sub(r'\\[a-zA-Z]+\s*', '', title)  # Remove LaTeX commands
            pub['title'] = title.strip()
        
        # Extract authors
        authors = extract_field(entry, 'author')
        if authors:
            # Clean up author format
            authors = re.sub(r'\s+and\s+', ', ', authors, flags=re.IGNORECASE)
            authors = re.sub(r'\{([^}]+)\}', r'\1', authors)  # Remove braces
            pub['authors'] = authors.strip()
        
        # Extract journal/booktitle
        journal = extract_field(entry, 'journal') or extract_field(entry, 'booktitle')
        if journal:
            journal = re.sub(r'\{([^}]+)\}', r'\1', journal)
            pub['journal'] = journal.strip()
        
        # Extract volume
        volume = extract_field(entry, 'volume')
        
        # Extract number/issue
        number = extract_field(entry, 'number')
        
        # Extract pages
        pages = extract_field(entry, 'pages')
        
        # Combine journal info with volume/issue/pages
        if pub.get('journal'):
            if volume:
                pub['journal'] += f", {volume}"
                if number:
                    pub['journal'] += f"({number})"
            if pages:
                pub['journal'] += f", {pages}"
        
        # Extract DOI
        doi = extract_field(entry, 'doi')
        if doi:
            doi = doi.strip()
            if not doi.startswith('http'):
                doi = f"https://doi.org/{doi}"
            pub['doi'] = doi
        
        # Extract URL (for PDF)
        url = extract_field(entry, 'url')
        if url:
            pub['pdf_url'] = url.strip()
        
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
        print("  - BibTeX: publications.bib or publications.biblatex")
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
        is_bibtex = input_file.lower().endswith('.bib') or input_file.lower().endswith('.biblatex')
        
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
