# site
Content for quarto version of r-nimble.org website

This is the converted Quarto version of the NIMBLE website, originally a WordPress site.

## About NIMBLE

NIMBLE is an R package for programming with BUGS models and compiling parts of R. It provides a system for building and sharing analysis methods for statistical models, especially hierarchical models and computationally-intensive methods.

## Website Structure

- `index.qmd` - Main homepage
- `about-us.qmd` - Team information
- `what-is-nimble.qmd` - Introduction to NIMBLE
- `download.qmd` - Installation instructions
- `documentation.qmd` - Links to manuals and guides
- `examples.qmd` - Example code and tutorials
- `blog/` - Blog posts and announcements
- `images/` - Static images and assets

## Building the Site

To build this Quarto website:

1. Install Quarto: https://quarto.org/docs/get-started/
2. Install required dependencies:
   ```bash
   # Install Quarto
   # Then render the site
   quarto render
   ```

3. Preview the site:
   ```bash
   quarto preview
   ```

## Configuration

The site configuration is in `_quarto.yml` which includes:
- Navigation structure
- Theme customization
- Output settings
- Blog listing configuration

## Customization

- `styles.css` - Custom CSS styles
- `custom.scss` - SCSS variables and additional styling
- `_quarto.yml` - Main configuration

## Original Content

This website was converted from WordPress HTML files. The original content has been preserved and adapted to Quarto format while maintaining the structure and information.

## Contributing

To add content:
1. Blog posts go in the `blog/` directory
2. Images go in the `images/` directory  
3. New pages can be added as `.qmd` files in the root
4. Update `_quarto.yml` to add new pages to navigation

## Links

- [NIMBLE GitHub Repository](https://github.com/nimble-dev/nimble)
- [NIMBLE Documentation](https://r-nimble.org/manual/cha-welcome-nimble.html)
- [CRAN Package](https://cran.r-project.org/package=nimble)
