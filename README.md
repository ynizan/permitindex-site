# PermitIndex - Static Site Generator

A Python-based static site generator for creating a comprehensive database of US government permits, licenses, and transactions.

## Project Overview

PermitIndex is a static site that helps users discover, compare, and apply for government permits across all US jurisdictions. The site provides detailed information about costs, processing times, requirements, and application procedures.

## Features

- 🔍 **Comprehensive Database**: Detailed information on government permits and licenses
- 📊 **Smart Search**: Find permits by jurisdiction, agency, or type
- ✅ **Status Indicators**: Online availability, API access, and MCP integration status
- 📱 **Mobile Responsive**: Works seamlessly on all devices
- 🔗 **SEO Optimized**: Full meta tags and JSON-LD structured data
- 🚀 **Fast Generation**: Static HTML for blazing-fast performance

## Project Structure

```
permit-index-site/
├── data/
│   ├── permits.csv          # Main permit database (18 columns)
│   └── sample.csv           # Legacy sample data (deprecated)
├── templates/
│   ├── index.html           # Homepage template
│   └── transaction_page.html # Individual permit page template
├── output/                   # Generated static HTML files
│   ├── index.html
│   ├── *.html               # Individual permit pages
│   ├── sitemap.xml
│   ├── robots.txt
│   └── data.json            # JSON export for search features
├── static/                   # Static assets (CSS, JS, images)
├── generator.py              # Main site generator script
└── requirements.txt          # Python dependencies
```

## Data Schema

The permits database (`data/permits.csv`) contains **18 columns** that capture comprehensive information about each government transaction:

### Column Definitions

| Column | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| `agency_short` | String | ✅ Yes | Short agency name (used as key) | "CA Dept of Public Health" |
| `request_type` | String | ✅ Yes | Type of permit/transaction (used as key) | "Food Truck Operating Permit" |
| `cost` | String | ✅ Yes | Cost range or fixed amount | "$500-800" or "Free" |
| `how_to_description` | Text | ✅ Yes | Detailed step-by-step application instructions | "1. Complete application... 2. Submit documents..." |
| `payment_form_url` | URL | ⚠️ Optional | Direct link to application/payment form | "https://agency.gov/apply" |
| `estimated_monthly_volume` | String | ✅ Yes | Estimated monthly application volume | "800-1200" or "500-1000" |
| `deadline_window` | String | ⚠️ Optional | Application deadline or renewal period | "Annual renewal by December 31st" |
| `effort_hours` | String | ✅ Yes | Estimated time to complete application | "4-6 hours" or "2-4 hours" |
| `online_available` | Boolean | ✅ Yes | Whether online application is available | "Yes" or "No" |
| `api_available` | Boolean | ✅ Yes | Whether API access is available | "Yes" or "No" |
| `mcp_available` | Boolean | ✅ Yes | Whether MCP integration is available | "Yes" or "No" |
| `related_pages` | String | ⚠️ Optional | Comma-separated list of related permit slugs | "california-business-license,california-sellers-permit" |
| `date_extracted` | Date | ✅ Yes | ISO date when data was collected | "2024-01-15" |
| `source_url` | URL | ⚠️ Optional | Source URL (internal only, not displayed) | "https://agency.gov/info" |
| `agency_full` | String | ✅ Yes | Full official agency name | "California Department of Public Health" |
| `eligibility` | Text | ✅ Yes | Who can apply and eligibility requirements | "Any individual or business operating a mobile food facility..." |
| `location_applicability` | String | ✅ Yes | Geographic scope of the permit | "Statewide (California)" or "City of San Francisco" |
| `document_requirements` | Text | ✅ Yes | Comma-separated list of required documents | "Business license, Vehicle inspection, Food handler certification" |

### Field Notes

**Primary Keys:**
- `agency_short` + `request_type` forms a composite key that uniquely identifies each permit
- URL slugs are auto-generated from these fields (e.g., "california-food-truck-permit")

**URL Structure:**
- Generated format: `/{state}-{permit-type}/`
- Example: `/california-food-truck-operating-permit/`

**Date Format:**
- All dates must be in ISO format: `YYYY-MM-DD`
- Used for sitemap lastmod dates

**Boolean Fields:**
- Must be exactly "Yes" or "No" (case-sensitive)
- Used for status indicators and statistics

**List Fields:**
- `related_pages`: Comma-separated, no spaces (will be split and linked)
- `document_requirements`: Comma-separated with spaces for readability

**Optional Fields:**
- `payment_form_url`: If provided, shows green "Apply Now" CTA button
- `deadline_window`: If provided, shows yellow deadline alert box
- `related_pages`: If provided, displays related permits section
- `source_url`: Internal tracking only, never displayed on site

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ynizan/permitindex-site.git
   cd permitindex-site
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python3 generator.py
   ```

## Usage

### Generating the Site

Run the generator to create all HTML pages:

```bash
python3 generator.py
```

This will:
- Load data from `data/permits.csv`
- Generate homepage at `output/index.html`
- Generate individual permit pages (e.g., `output/california-food-truck-permit.html`)
- Create `sitemap.xml` with lastmod dates
- Create `data.json` for potential search features
- Generate `robots.txt`

### Adding New Permits

1. **Add a row to `data/permits.csv`** with all 18 columns filled
2. **Follow the schema** as documented above
3. **Run the generator** to create updated pages
4. **Test the output** by viewing generated HTML files

### Preview Pages Locally

Use Python's built-in HTTP server:

```bash
cd output
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

### Taking Screenshots

Use the included screenshot scripts (requires Playwright):

```bash
# Install Playwright (one-time)
pip3 install playwright
python3 -m playwright install

# Take screenshots
python3 screenshot_homepage.py    # Homepage
python3 screenshot_permit.py      # Sample permit page
```

## Generated Pages

### Homepage (`/index.html`)
- Hero section with search bar
- Statistics dashboard (total permits, agencies, online access, API availability)
- Value proposition (3 benefits)
- Browse by agency cards
- Popular permits section
- Call-to-action

### Permit Pages (`/{slug}.html`)
Each permit page includes:
- **Key Metrics**: Cost, estimated effort, monthly volume
- **Apply Now CTA**: Green button linking to `payment_form_url` (if provided)
- **Eligibility Section**: Who can apply
- **Document Requirements**: Styled checklist with icons
- **How to Apply**: Timeline visualization with numbered steps
- **Related Permits**: Linked cards to related permits
- **Quick Facts Sidebar**: Agency info, costs, effort, location
- **Status Indicators**: Online/API/MCP availability (✅/❌)
- **Last Updated Date**: From `date_extracted` field

## SEO Features

- ✅ Comprehensive meta tags (title, description, keywords)
- ✅ Open Graph tags for social sharing
- ✅ Twitter Card tags
- ✅ Canonical URLs
- ✅ JSON-LD structured data:
  - BreadcrumbList
  - GovernmentService
  - HowTo
  - Organization
  - WebSite with SearchAction
- ✅ Semantic HTML5 structure
- ✅ Sitemap.xml with lastmod dates
- ✅ Robots.txt

## Development

### Requirements
- Python 3.7+
- pandas
- jinja2
- playwright (optional, for screenshots)

### Generator Features
- **Automatic URL slug generation** from agency + request type
- **Related pages linking** via slug references
- **Smart data export** to JSON (excludes internal fields)
- **Error handling** with detailed error messages
- **Statistics tracking** (pages generated, errors, duration)

### Customization

**Templates:**
- Edit `templates/index.html` for homepage layout
- Edit `templates/transaction_page.html` for permit pages
- Uses Tailwind CSS via CDN (easy to customize)

**Styling:**
- Tailwind CSS for rapid UI development
- Custom color scheme: Blue primary, green CTAs, yellow alerts
- Responsive breakpoints: mobile, tablet, desktop

**Data Processing:**
- Modify `generator.py` for custom data transformations
- Add new template variables in `generate_page()` method
- Extend CSV schema by adding columns (update templates too)

## Contributing

To add new permits:

1. **Research the permit** on official government websites
2. **Fill in all 18 columns** following the schema
3. **Use realistic data** (actual URLs, accurate costs, real requirements)
4. **Test locally** before committing
5. **Commit with descriptive message**

## Data Quality Guidelines

- ✅ Use official government sources
- ✅ Include complete, accurate information
- ✅ Update `date_extracted` when refreshing data
- ✅ Test all URLs before adding
- ✅ Write clear, step-by-step instructions
- ✅ Include all required documents
- ✅ Specify geographic applicability precisely

## Future Enhancements

- [ ] Client-side search using `data.json`
- [ ] Filter by cost, effort, location
- [ ] Permit comparison tool
- [ ] Email alerts for deadline reminders
- [ ] API for external integrations
- [ ] User reviews and ratings
- [ ] State-specific landing pages
- [ ] Agency profile pages

## License

© 2024 PermitIndex. All rights reserved.

## Support

For questions or issues:
- GitHub Issues: https://github.com/ynizan/permitindex-site/issues
- Email: contact@permitindex.com
- Documentation: https://permitindex.com/docs

---

**Last Updated:** 2024-01-15
**Version:** 2.0.0 (18-column schema)
