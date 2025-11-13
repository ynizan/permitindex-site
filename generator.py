#!/usr/bin/env python3
"""
PermitIndex Static Site Generator

This script generates static HTML pages for government transactions.
It reads data from CSV files and renders them using Jinja2 templates.

Directory Structure:
- /templates: Jinja2 templates
- /data: CSV data files
- /output: Generated HTML pages
- /static: Static assets (CSS, JS, images)

Usage:
    python generator.py
"""

import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import sys


class SiteGenerator:
    """Main site generator class"""

    def __init__(self, base_dir=None):
        """
        Initialize the site generator

        Args:
            base_dir: Base directory path (defaults to script location)
        """
        self.base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(self.base_dir, 'templates')
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.static_dir = os.path.join(self.base_dir, 'static')

        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

        # Statistics
        self.stats = {
            'pages_generated': 0,
            'errors': 0,
            'start_time': datetime.now()
        }

    def load_data(self, csv_file):
        """
        Load data from CSV file

        Args:
            csv_file: Path to CSV file

        Returns:
            pandas DataFrame with loaded data
        """
        csv_path = os.path.join(self.data_dir, csv_file)
        print(f"📂 Loading data from: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
            print(f"✓ Loaded {len(df)} records")
            return df
        except FileNotFoundError:
            print(f"✗ Error: CSV file not found: {csv_path}")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
            sys.exit(1)

    def generate_page(self, template_name, data, output_path):
        """
        Generate a single HTML page from template and data

        Args:
            template_name: Name of the Jinja2 template
            data: Dictionary of data to pass to template
            output_path: Full path where to save the generated HTML
        """
        try:
            # Load template
            template = self.env.get_template(template_name)

            # Render template with data
            html_content = template.render(**data)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✓ Generated: {output_path}")
            self.stats['pages_generated'] += 1

        except Exception as e:
            print(f"✗ Error generating page: {e}")
            self.stats['errors'] += 1

    def generate_transaction_pages(self):
        """Generate all transaction pages from CSV data"""
        print("\n🚀 Starting page generation...\n")

        # Load CSV data
        df = self.load_data('sample.csv')

        # Generate a page for each row in the CSV
        for idx, row in df.iterrows():
            # Convert row to dictionary
            data = row.to_dict()

            # Build output path based on jurisdiction and URL slug
            # Format: /output/{jurisdiction}/{url_slug}/index.html
            jurisdiction_slug = data['jurisdiction'].lower().replace(' ', '-')
            output_path = os.path.join(
                self.output_dir,
                jurisdiction_slug,
                f"{data['url_slug']}.html"
            )

            # Generate the page
            self.generate_page('transaction_page.html', data, output_path)

        print(f"\n✓ Generated {self.stats['pages_generated']} page(s)")

    def generate_sitemap(self):
        """Generate sitemap.xml with all page URLs"""
        print("\n🗺️  Generating sitemap.xml...")

        # Base URL for the site
        base_url = "https://permitindex.com"

        # Load data to get all URLs
        df = self.load_data('sample.csv')

        # Build sitemap XML
        sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        # Add homepage
        sitemap_content.append('  <url>')
        sitemap_content.append(f'    <loc>{base_url}/</loc>')
        sitemap_content.append('    <changefreq>daily</changefreq>')
        sitemap_content.append('    <priority>1.0</priority>')
        sitemap_content.append('  </url>')

        # Add transaction pages
        for idx, row in df.iterrows():
            jurisdiction_slug = row['jurisdiction'].lower().replace(' ', '-')
            url = f"{base_url}/{jurisdiction_slug}/{row['url_slug']}"

            sitemap_content.append('  <url>')
            sitemap_content.append(f'    <loc>{url}</loc>')
            sitemap_content.append('    <changefreq>weekly</changefreq>')
            sitemap_content.append('    <priority>0.8</priority>')
            sitemap_content.append('  </url>')

        sitemap_content.append('</urlset>')

        # Write sitemap
        sitemap_path = os.path.join(self.output_dir, 'sitemap.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sitemap_content))

        print(f"✓ Sitemap generated: {sitemap_path}")

    def generate_robots_txt(self):
        """Generate robots.txt with sitemap location"""
        print("\n🤖 Generating robots.txt...")

        robots_content = [
            "# PermitIndex robots.txt",
            "# Allow all crawlers",
            "",
            "User-agent: *",
            "Allow: /",
            "",
            "# Sitemap location",
            "Sitemap: https://permitindex.com/sitemap.xml"
        ]

        # Write robots.txt
        robots_path = os.path.join(self.output_dir, 'robots.txt')
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(robots_content))

        print(f"✓ Robots.txt generated: {robots_path}")

    def print_statistics(self):
        """Print generation statistics"""
        end_time = datetime.now()
        duration = (end_time - self.stats['start_time']).total_seconds()

        print("\n" + "=" * 60)
        print("📊 GENERATION STATISTICS")
        print("=" * 60)
        print(f"Pages generated: {self.stats['pages_generated']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Output directory: {self.output_dir}")
        print("=" * 60 + "\n")

    def generate(self):
        """Run the complete site generation process"""
        print("\n" + "=" * 60)
        print("🏛️  PERMITINDEX STATIC SITE GENERATOR")
        print("=" * 60)

        # Generate transaction pages
        self.generate_transaction_pages()

        # Generate sitemap
        self.generate_sitemap()

        # Generate robots.txt
        self.generate_robots_txt()

        # Print statistics
        self.print_statistics()

        if self.stats['errors'] == 0:
            print("✅ Site generation completed successfully!\n")
            return 0
        else:
            print("⚠️  Site generation completed with errors.\n")
            return 1


def main():
    """Main entry point"""
    generator = SiteGenerator()
    return generator.generate()


if __name__ == '__main__':
    sys.exit(main())
