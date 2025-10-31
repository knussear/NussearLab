# Importing Publications from ResearchGate

This guide explains how to import your publications from ResearchGate into the website.

## Method 1: Manual Copy-Paste (Recommended)

ResearchGate doesn't provide a public API, so the easiest method is to manually copy publication information:

1. **Go to your ResearchGate profile** and view your publications list
2. **For each publication**, copy the following information:
   - Title
   - Authors (in proper citation format)
   - Journal/Conference name
   - Year
   - DOI link (if available)
   - PDF link (if you have it uploaded)

3. **Edit `publications.html`** and add each publication using this template:

```html
<div class="publication" data-year="YEAR">
    <h3 class="pub-title">Publication Title Here</h3>
    <p class="pub-authors">Author, A., Nussear, K., & Co-author, C.</p>
    <p class="pub-journal"><em>Journal Name</em>, Volume(Issue), Pages.</p>
    <p class="pub-year">YEAR</p>
    <div class="pub-links">
        <a href="https://doi.org/10.xxxx/xxxxx" class="pub-link">DOI</a>
        <a href="path/to/pdf" class="pub-link">PDF</a>
    </div>
</div>
```

4. **Important**: Replace `YEAR` in `data-year="YEAR"` with the actual publication year for filtering to work

## Method 2: Using the Import Helper Script (CSV or BibTeX)

We've created a Python script to help you generate the HTML from CSV or BibTeX files:

### Option A: From CSV File

**Step 1:** Create a file named `publications.csv` with your publication data:

```csv
year,title,authors,journal,doi,pdf_url
2024,Sample Publication Title,"Nussear K., Author A., Collaborator B.",Journal Name 10(2):123-145,https://doi.org/10.xxxx/xxxxx,
2023,Another Research Paper,"Author A., Nussear K., Researcher C.",Conservation Biology 15(3):200-215,https://doi.org/10.yyyy/yyyyy,https://example.com/paper.pdf
```

**Step 2:** Run the import script:

```bash
python3 import_publications.py publications.csv
```

### Option B: From BibTeX File

**Step 1:** Export your publications from your citation manager (Zotero, Mendeley, EndNote) as BibTeX format, or download BibTeX from ResearchGate:

```bibtex
@article{nussear2024sample,
  title={Sample Publication Title},
  author={Nussear, Kenneth and Author, A. and Collaborator, B.},
  journal={Journal Name},
  volume={10},
  number={2},
  pages={123--145},
  year={2024},
  doi={10.xxxx/xxxxx}
}
```

**Step 2:** Run the import script:

```bash
python3 import_publications.py publications.bib
```

### Step 3: Copy the output (for both options)

1. Open `publications_output.html`
2. Copy the generated publication divs
3. Paste them into `publications.html` in the `publications-container` section

## Method 3: Direct Export from Citation Managers

If you use citation managers like Zotero, Mendeley, or EndNote:

1. **Export your publications** to BibTeX format (.bib file)
2. **Use Method 2, Option B** above with the BibTeX file
3. The script automatically handles BibTeX formatting and converts it to HTML

## Exporting BibTeX from ResearchGate

ResearchGate allows you to export individual publications as BibTeX:

1. Go to your publication on ResearchGate
2. Click the "Cite" button
3. Select "BibTeX" format
4. Copy and paste into a `.bib` file
5. Repeat for all publications you want to import
6. Use Method 2, Option B above

**Pro tip:** If you have many publications, it's faster to use a citation manager:
1. Import your publications into Zotero, Mendeley, or EndNote
2. Export all publications as a single BibTeX file
3. Use the import script on that file

## Tips

- **Sort by year**: Publications are automatically sorted by year (newest first)
- **Update year filter**: If you have publications from years not in the dropdown, add those years to the filter in `publications.html` (lines 32-38)
- **Check data-year attribute**: The script automatically sets this correctly for filtering to work
- **ResearchGate links**: You can link directly to your ResearchGate publication pages if you don't have PDFs
- **BibTeX cleaning**: The script automatically cleans up LaTeX commands and formatting from BibTeX

## Example ResearchGate Publication Format

When copying from ResearchGate, publications typically look like:

```
Title: Effects of Climate Change on Desert Tortoise Populations
Authors: Kenneth E. Nussear, Todd C. Esque, et al.
Journal: Biological Conservation, 2023
```

Convert this to:

```html
<div class="publication" data-year="2023">
    <h3 class="pub-title">Effects of Climate Change on Desert Tortoise Populations</h3>
    <p class="pub-authors">Nussear, K.E., Esque, T.C., et al.</p>
    <p class="pub-journal"><em>Biological Conservation</em>, 2023</p>
    <p class="pub-year">2023</p>
    <div class="pub-links">
        <a href="https://doi.org/10.xxxx/xxxxx" class="pub-link">DOI</a>
    </div>
</div>
```

## Need Help?

If you have a large number of publications and need assistance with bulk import, consider:
1. Creating a spreadsheet with all publication data
2. Using the Python helper script (see below)
3. Or contact someone with Python/JavaScript experience to help automate the process

The key is getting your publication data into the format shown above, with the correct `data-year` attribute for the filtering feature to work.
