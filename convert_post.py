#!/usr/bin/env python3
"""
WordPress to Quarto Blog Post Converter

This script helps convert WordPress HTML files to Quarto markdown format.
It extracts the main content and creates proper YAML frontmatter.

Usage:
    python convert_post.py input.html output.qmd
"""

import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import html2text

def extract_title(soup):
    """Extract title from the HTML"""
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text().strip()
        # Remove "– NIMBLE" suffix if present
        title = re.sub(r'\s*–\s*NIMBLE\s*$', '', title)
        return title
    return "Untitled Post"

def extract_content(soup):
    """Extract main content from WordPress HTML"""
    # Look for common WordPress content containers
    content_selectors = [
        '.entry-content',
        '.post-content', 
        '.content',
        'article .entry-content',
        '.textwidget'
    ]
    
    content = None
    for selector in content_selectors:
        content = soup.select_one(selector)
        if content:
            break
    
    if not content:
        # Fallback: look for main content area
        main_tag = soup.find('main') or soup.find('article')
        if main_tag:
            content = main_tag
    
    if content:
        # Convert HTML to markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0  # Don't wrap lines
        markdown_content = h.handle(str(content))
        
        # Clean up the markdown
        markdown_content = re.sub(r'\n\n\n+', '\n\n', markdown_content)
        markdown_content = markdown_content.strip()
        
        return markdown_content
    
    return "Content could not be extracted."

def create_frontmatter(title, date=None):
    """Create YAML frontmatter for the blog post"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Guess categories based on title
    categories = ["announcement"]
    title_lower = title.lower()
    if "version" in title_lower and "released" in title_lower:
        categories = ["release", "announcement"]
    elif "bug" in title_lower:
        categories = ["bugfix", "announcement"]
    elif "course" in title_lower or "tutorial" in title_lower:
        categories = ["education", "announcement"]
    
    frontmatter = f"""---
title: "{title}"
description: ""
author: "NIMBLE Development Team"
date: "{date}"
categories: {categories}
---

"""
    return frontmatter

def convert_post(input_file, output_file):
    """Convert a WordPress HTML file to Quarto markdown"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title = extract_title(soup)
        content = extract_content(soup)
        frontmatter = create_frontmatter(title)
        
        # Combine frontmatter and content
        full_content = frontmatter + content
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"Successfully converted {input_file} to {output_file}")
        print(f"Title: {title}")
        
    except Exception as e:
        print(f"Error converting {input_file}: {e}")
        return False
    
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_post.py input.html output.qmd")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    convert_post(input_file, output_file)

if __name__ == "__main__":
    main()
