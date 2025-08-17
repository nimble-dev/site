#!/bin/bash

# Batch convert WordPress posts to Quarto format
# This script converts all HTML files in the posts/ directory

echo "Converting WordPress posts to Quarto format..."

# Create blog directory if it doesn't exist
mkdir -p blog

# Convert each post file
for file in posts/*; do
    if [ -f "$file" ]; then
        # Extract filename without path
        filename=$(basename "$file")
        
        # Skip if it's a directory or already processed
        if [ -d "$file" ]; then
            continue
        fi
        
        # Create output filename
        output="blog/${filename}.qmd"
        
        echo "Converting $file to $output"
        
        # Use the Python converter if available, otherwise create a basic conversion
        if command -v python3 &> /dev/null && [ -f convert_post.py ]; then
            python3 convert_post.py "$file" "$output"
        else
            # Basic conversion - extract title and create placeholder
            title=$(grep -o '<title>[^<]*' "$file" | sed 's/<title>//' | sed 's/ – NIMBLE//')
            
            if [ -z "$title" ]; then
                title=$(basename "$file")
            fi
            
            cat > "$output" << EOF
---
title: "$title"
description: "Converted from WordPress"
author: "NIMBLE Development Team"
date: "2024-01-01"
categories: [announcement]
---

This post was converted from the original WordPress site. 
The content needs to be manually reviewed and formatted.

Original file: $file

To complete the conversion:
1. Extract the main content from the HTML file
2. Convert HTML to Markdown format
3. Update the frontmatter with correct date and categories
4. Review and clean up the content
EOF
            echo "Created placeholder for $output"
        fi
    fi
done

echo "Conversion complete!"
echo "Note: Please review and edit the converted files in the blog/ directory"
echo "Update dates, categories, and content as needed."
