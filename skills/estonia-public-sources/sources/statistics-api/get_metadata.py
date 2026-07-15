#!/usr/bin/env python3
"""
Get ESMS metadata for Statistics Estonia tables.

This script fetches comprehensive metadata (methodology, sources, quality, etc.)
for a given table ID from Statistics Estonia's ESMS metadata system.

Usage:
    python get_metadata.py TABLE_ID [--format FORMAT]

Arguments:
    TABLE_ID    Table identifier (e.g., IA001)

Options:
    --format    Output format: 'html' (default), 'simple', or 'text'
                - html: Full HTML with all markup (~55KB)
                - simple: Simplified HTML without unnecessary attributes (~18KB, 66% smaller)
                - text: Plain text only (~12KB, 77% smaller)

Examples:
    python get_metadata.py IA001
    python get_metadata.py IA001 --format simple
    python get_metadata.py IA001 --format text
"""

import sys
import json
import re
import urllib.request
import urllib.error
from html.parser import HTMLParser


class PageContainerExtractor(HTMLParser):
    """Extract content from <div class="page-container"> section."""

    def __init__(self):
        super().__init__()
        self.in_page_container = False
        self.depth = 0
        self.content = []

    def handle_starttag(self, tag, attrs):
        if self.in_page_container:
            self.content.append(self.get_starttag_text())
            self.depth += 1
        else:
            attrs_dict = dict(attrs)
            if tag == 'div' and 'page-container' in attrs_dict.get('class', ''):
                self.in_page_container = True
                self.depth = 1
                self.content.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.in_page_container:
            self.content.append(f'</{tag}>')
            self.depth -= 1
            if self.depth == 0:
                self.in_page_container = False

    def handle_data(self, data):
        if self.in_page_container:
            self.content.append(data)

    def handle_startendtag(self, tag, attrs):
        if self.in_page_container:
            self.content.append(self.get_starttag_text())

    def get_html(self):
        return ''.join(self.content)


def fetch_url(url, timeout=15):
    """Fetch URL content with error handling."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return None


def get_table_info_from_api(table_id):
    """Get table path from Statistics Estonia API search."""
    clean_id = table_id.replace('.PX', '')

    url = f'https://andmed.stat.ee/api/v1/en/stat?query={clean_id}'
    content = fetch_url(url)

    if not content:
        return None

    try:
        data = json.loads(content)
        # Find exact match
        for item in data:
            if item['id'].replace('.PX', '') == clean_id:
                return item
    except json.JSONDecodeError as e:
        print(f"Error parsing API response: {e}", file=sys.stderr)

    return None


def get_metadata_id_from_web(table_id, path):
    """Scrape metadata ID from table web page."""
    clean_id = table_id.replace('.PX', '')
    url_path = path.replace('/', '__').lstrip('__')
    url = f"https://andmed.stat.ee/en/stat/{url_path}/{clean_id}"

    content = fetch_url(url)
    if not content:
        return None

    # Extract metadata ID from ESMS link
    match = re.search(r'esms-metadata/(\d+)', content)
    if match:
        return match.group(1)

    return None


def extract_page_container_html(metadata_id):
    """Extract page-container div HTML from ESMS metadata page."""
    url = f"https://www.stat.ee/en/find-statistics/methodology-and-quality/esms-metadata/{metadata_id}"

    content = fetch_url(url)
    if not content:
        return None

    # Use HTML parser to extract page-container
    parser = PageContainerExtractor()
    parser.feed(content)

    html = parser.get_html()

    if not html:
        print("Warning: page-container div not found in HTML", file=sys.stderr)
        return None

    return html


def simplify_html(html):
    """
    Simplify HTML by removing unnecessary attributes and markup.
    Reduces size by ~66% while keeping structure.
    """
    # Remove breadcrumb
    html = re.sub(r'<nav class="breadcrumb".*?</nav>', '', html, flags=re.DOTALL)

    # Remove all data-* attributes
    html = re.sub(r'\s+data-[a-z-]+="[^"]*"', '', html)

    # Remove specific class patterns
    html = re.sub(r'\s+class="[^"]*vocabulary-statistical-activities-hint[^"]*"', '', html)
    html = re.sub(r'\s+class="embedded-entity"', '', html)
    html = re.sub(r'\s+class="taxonomy-term[^"]*"', '', html)
    html = re.sub(r'\s+class="clearfix[^"]*"', '', html)
    html = re.sub(r'\s+class="field[^"]*"', '', html)
    html = re.sub(r'\s+class="paragraph[^"]*"', '', html)
    html = re.sub(r'\s+class="table-wrap[^"]*"', '', html)

    # Remove attributes
    html = re.sub(r'\s+about="[^"]*"', '', html)
    html = re.sub(r'\s+id="taxonomy-term-\d+"', '', html)
    html = re.sub(r'\s+role="[^"]*"', '', html)
    html = re.sub(r'\s+aria-[a-z-]+="[^"]*"', '', html)

    # Clean up whitespace
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
    html = re.sub(r'  +', ' ', html)

    return html


def html_to_text(html):
    """
    Convert HTML to plain text.
    Reduces size by ~77% while keeping all content.
    """
    # Remove scripts and styles
    text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)

    # Convert to text
    text = re.sub(r'<[^>]+>', '\n', text)
    text = re.sub(r'\n\s*\n', '\n', text)

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)


def main():
    """Main entry point."""
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python get_metadata.py TABLE_ID [--format FORMAT]", file=sys.stderr)
        print("Example: python get_metadata.py IA001 --format simple", file=sys.stderr)
        sys.exit(1)

    table_id = sys.argv[1]

    # Check for format option
    output_format = 'html'
    if len(sys.argv) >= 4 and sys.argv[2] == '--format':
        output_format = sys.argv[3].lower()
        if output_format not in ['html', 'simple', 'text']:
            print(f"Error: Invalid format '{output_format}'. Use: html, simple, or text", file=sys.stderr)
            sys.exit(1)

    # Step 1: Get table info from API
    print(f"Fetching table info for {table_id}...", file=sys.stderr)
    table_info = get_table_info_from_api(table_id)

    if not table_info:
        print(f"Error: Table '{table_id}' not found in Statistics Estonia database", file=sys.stderr)
        sys.exit(1)

    print(f"Found: {table_info['title']}", file=sys.stderr)
    print(f"Path: {table_info['path']}", file=sys.stderr)

    # Step 2: Get metadata ID from web page
    print(f"Extracting metadata ID...", file=sys.stderr)
    metadata_id = get_metadata_id_from_web(table_info['id'], table_info['path'])

    if not metadata_id:
        print(f"Warning: No ESMS metadata found for table {table_id}", file=sys.stderr)
        print("This table may not have published methodology documentation.", file=sys.stderr)
        sys.exit(1)

    print(f"Metadata ID: {metadata_id}", file=sys.stderr)
    print(f"URL: https://www.stat.ee/en/find-statistics/methodology-and-quality/esms-metadata/{metadata_id}", file=sys.stderr)

    # Step 3: Extract page-container HTML
    print(f"Fetching ESMS metadata...", file=sys.stderr)
    html = extract_page_container_html(metadata_id)

    if not html:
        print("Error: Failed to extract metadata HTML", file=sys.stderr)
        sys.exit(1)

    # Apply format transformation
    if output_format == 'simple':
        html = simplify_html(html)
        print(f"Success! Simplified metadata HTML ({len(html)} characters, ~66% smaller)", file=sys.stderr)
    elif output_format == 'text':
        html = html_to_text(html)
        print(f"Success! Plain text metadata ({len(html)} characters, ~77% smaller)", file=sys.stderr)
    else:
        print(f"Success! Full metadata HTML ({len(html)} characters)", file=sys.stderr)

    print("", file=sys.stderr)

    # Output to stdout
    print(html)

    return 0


if __name__ == '__main__':
    sys.exit(main())
