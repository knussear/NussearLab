# Nussear Lab Website Guide

This guide explains how to update and maintain the Nussear Lab website.

## Website Structure

The website consists of five main pages:
- `index.html` - Homepage with lab overview
- `people.html` - Lab members and alumni
- `publications.html` - Research publications
- `projects.html` - Research projects
- `news.html` - Lab news and updates

## How to Update Content

### Adding Lab Members (people.html)

1. Open `people.html` in a text editor
2. Find the appropriate section (Graduate Students, Undergraduate Students, etc.)
3. Copy an existing person card and modify the details:

```html
<div class="person-card">
    <div class="person-info">
        <h3>Name Here</h3>
        <p class="person-role">Title/Position</p>
        <p class="person-bio">Brief description of research interests.</p>
        <p class="person-contact">
            <strong>Email:</strong> <a href="mailto:email@unr.edu">email@unr.edu</a>
        </p>
    </div>
</div>
```

### Adding Publications (publications.html)

1. Open `publications.html`
2. Add a new publication in the publications list section:

```html
<div class="publication" data-year="2025">
    <h3 class="pub-title">Your Paper Title</h3>
    <p class="pub-authors">Author, A., Author, B., & Nussear, K.</p>
    <p class="pub-journal"><em>Journal Name</em>, Volume(Issue), Pages.</p>
    <p class="pub-year">2025</p>
    <div class="pub-links">
        <a href="https://doi.org/..." class="pub-link">DOI</a>
        <a href="path/to/pdf" class="pub-link">PDF</a>
    </div>
</div>
```

**Important:** Set the `data-year` attribute correctly for the year filter to work.

### Adding Projects (projects.html)

1. Open `projects.html`
2. Add to either "Current Projects" or "Completed Projects" section:

```html
<div class="project-card">
    <h3 class="project-title">Project Name</h3>
    <p class="project-status status-active">Active</p>
    <!-- or use status-completed for completed projects -->
    <p class="project-description">
        Project description here.
    </p>
    <div class="project-meta">
        <p><strong>Duration:</strong> Start - End</p>
        <p><strong>Funding:</strong> Funding source</p>
        <p><strong>Collaborators:</strong> List collaborators</p>
    </div>
</div>
```

### Adding News Items (news.html)

1. Open `news.html`
2. Add a new news item at the top of the news feed (most recent first):

```html
<article class="news-item">
    <div class="news-date">Month Day, Year</div>
    <h2 class="news-title">News Headline</h2>
    <p class="news-content">
        News content here. You can add <a href="link">links</a> too.
    </p>
</article>
```

### Updating the Homepage (index.html)

Edit the welcome message and lab description in the `<section class="about">` section.

## Customizing Styles

All styles are in `css/style.css`. You can customize:
- Colors (see CSS variables at the top of the file)
- Fonts
- Spacing
- Layout

### Color Scheme

The default colors are defined as CSS variables:
```css
:root {
    --primary-color: #003366;      /* Dark blue */
    --secondary-color: #0066cc;    /* Medium blue */
    --accent-color: #c5a900;       /* Gold */
    --text-color: #333;            /* Dark gray */
    --light-bg: #f5f5f5;          /* Light gray */
}
```

Change these values to customize the color scheme.

## Deploying the Website

### GitHub Pages (Recommended)

1. Push all changes to your GitHub repository
2. Go to repository Settings > Pages
3. Select the branch to deploy (usually `main`)
4. Select the root folder `/`
5. Save and wait a few minutes for deployment

Your site will be available at: `https://username.github.io/repository-name/`

### Other Hosting Options

The website is static HTML/CSS/JavaScript, so it can be hosted on:
- Netlify
- Vercel
- Any web server
- University hosting services

Simply upload all files to your hosting service.

## File Organization

```
NussearLab/
├── index.html              # Homepage
├── people.html             # Lab members
├── publications.html       # Publications list
├── projects.html          # Research projects
├── news.html              # News and updates
├── css/
│   └── style.css          # All styles
├── js/
│   ├── main.js            # Main JavaScript
│   └── publications.js    # Publications filtering
├── README.md              # Repository info
└── WEBSITE_GUIDE.md       # This guide
```

## Best Practices

1. **Keep content up to date**: Regular updates keep the site relevant
2. **Add news regularly**: Post updates about publications, grants, and achievements
3. **Use consistent formatting**: Follow the examples when adding new content
4. **Test on mobile**: Check how the site looks on phones and tablets
5. **Backup before major changes**: Commit changes to git regularly

## Adding Features

### Adding a New Page

1. Create a new HTML file (e.g., `resources.html`)
2. Copy the structure from an existing page
3. Update the navigation in all pages to include the new page:

```html
<li><a href="resources.html">Resources</a></li>
```

### Adding Images

1. Create an `images` folder in the root directory
2. Add images to this folder
3. Reference them in HTML:

```html
<img src="images/photo.jpg" alt="Description">
```

### Adding a Contact Form

Consider using a third-party service like:
- Google Forms
- Formspree
- Netlify Forms

## Troubleshooting

**Navigation links not working?**
- Check that all HTML files are in the root directory
- Verify file names match the links

**Styles not loading?**
- Check that `css/style.css` exists
- Verify the path in the `<link>` tag is correct

**Year filter not working on publications?**
- Ensure each publication has a `data-year` attribute
- Check that `js/publications.js` is loaded

## Support

For questions about web development or hosting, contact your institution's IT support or consult web development documentation online.

## License

This website template can be freely used and modified for academic purposes.
