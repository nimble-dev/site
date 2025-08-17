#!/usr/bin/env python3
"""
Generate search_index.json for gitbook manual.
This script extracts content from HTML files and creates a search index
in the format expected by the gitbook search plugin.
"""

import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_text(text):
    """Clean and normalize text content."""
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove code block markers and excessive punctuation
    text = re.sub(r'```[^```]*```', '', text)
    text = re.sub(r'`[^`]*`', '', text)
    return text

def extract_content_from_html(html_file):
    """Extract title and content from an HTML file."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract title from the <title> tag
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text()
        # Clean up title - remove " | NimbleUserManual.knit" suffix
        title = re.sub(r'\s*\|\s*NimbleUserManual\.knit\s*$', '', title)
    else:
        title = os.path.basename(html_file).replace('.html', '').replace('cha-', '').replace('-', ' ').title()
    
    # Extract main content from page-inner section
    page_inner = soup.find('div', class_='page-inner')
    if page_inner:
        # Remove navigation and non-content elements
        for element in page_inner.find_all(['nav', 'script', 'style']):
            element.decompose()
        
        # Get text content
        body_text = page_inner.get_text()
    else:
        # Fallback: try to get content from body
        body = soup.find('body')
        if body:
            # Remove sidebar and navigation
            for element in body.find_all(['div'], class_=['book-summary', 'book-header']):
                element.decompose()
            body_text = body.get_text()
        else:
            body_text = ""
    
    # Clean the extracted text
    body_text = clean_text(body_text)
    
    return title, body_text

def generate_search_index(manual_dir):
    """Generate search index for all HTML files in the manual directory."""
    search_data = []
    
    # Get all HTML files in the manual directory
    html_files = list(Path(manual_dir).glob('*.html'))
    
    # Filter out 404.html and other non-content files
    content_files = [f for f in html_files if not f.name.startswith('404')]
    
    for html_file in sorted(content_files):
        print(f"Processing {html_file.name}...")
        
        try:
            title, content = extract_content_from_html(html_file)
            
            # Create relative URL (filename without .html extension)
            url = html_file.name
            
            # Add to search data as [url, title, content]
            search_data.append([url, title, content])
            
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
            continue
    
    return search_data

def main():
    manual_dir = '/var/tmp/nimble-dev/website/manual'
    output_file = os.path.join(manual_dir, 'search_index.json')
    
    print("Generating search index for NIMBLE manual...")
    
    # Generate search data
    search_data = generate_search_index(manual_dir)
    
    # Write to search_index.json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(search_data, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"Generated search index with {len(search_data)} pages.")
    print(f"Search index saved to: {output_file}")
    
    # Show first entry as example
    if search_data:
        first_entry = search_data[0]
        print(f"\nExample entry:")
        print(f"URL: {first_entry[0]}")
        print(f"Title: {first_entry[1]}")
        print(f"Content (first 200 chars): {first_entry[2][:200]}...")

if __name__ == "__main__":
    main()
