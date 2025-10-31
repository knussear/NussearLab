#!/usr/bin/env python3
"""
Helper script to convert publication data from CSV to HTML format for the Nussear Lab website.

Usage:
    python3 import_publications.py publications.csv

CSV Format:
    year,title,authors,journal,doi,pdf_url
    2024,Title Here,"Author A., Nussear K.",Journal Name,https://doi.org/...,

Output:
    Creates publications_output.html with formatted publication entries
"""

import csv
import sys
import html


def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(text)


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
        print("Usage: python3 import_publications.py publications.csv")
        print("\nCSV Format:")
        print("year,title,authors,journal,doi,pdf_url")
        print('2024,"Title","Author A., Nussear K.","Journal Name","https://doi.org/...","https://..."')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "publications_output.html"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            publications = []
            
            for row in reader:
                if row.get('year') and row.get('title'):
                    publications.append(row)
            
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
        print("\nCreate a CSV file with this format:")
        print("year,title,authors,journal,doi,pdf_url")
        print('2024,"Title","Author A., Nussear K.","Journal Name","https://doi.org/...","https://..."')
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
