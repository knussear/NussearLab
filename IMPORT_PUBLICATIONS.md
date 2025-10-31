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

## Method 2: Using the Import Helper Script

We've created a Python script to help you generate the HTML from a CSV file:

### Step 1: Create a CSV file

Create a file named `publications.csv` with your publication data:

```csv
year,title,authors,journal,doi,pdf_url
2024,Sample Publication Title,"Nussear K., Author A., Collaborator B.",Journal Name 10(2):123-145,https://doi.org/10.xxxx/xxxxx,
2023,Another Research Paper,"Author A., Nussear K., Researcher C.",Conservation Biology 15(3):200-215,https://doi.org/10.yyyy/yyyyy,https://example.com/paper.pdf
```

### Step 2: Run the import script

```bash
python3 import_publications.py publications.csv
```

This will generate `publications_output.html` with all your publications formatted correctly.

### Step 3: Copy the output

1. Open `publications_output.html`
2. Copy the generated publication divs
3. Paste them into `publications.html` in the `publications-container` section

## Method 3: Export from Citation Manager

If you use a citation manager (Zotero, Mendeley, EndNote):

1. **Export your publications** to BibTeX format
2. **Use an online converter** or the provided Python script to convert BibTeX to HTML
3. **Paste the formatted HTML** into `publications.html`

## Tips

- **Sort by year**: Add newer publications at the top of the list
- **Update year filter**: If you have publications from years not in the dropdown, add those years to the filter in `publications.html` (lines 32-38)
- **Check data-year attribute**: This must match the actual year for filtering to work
- **ResearchGate links**: You can link directly to your ResearchGate publication pages if you don't have PDFs

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
