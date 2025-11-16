<img width="640" height="320" alt="peppol_extract_codes_list" src="https://github.com/user-attachments/assets/de89b5e4-3d2a-4752-8108-95e5f75db2fd" />

# PEPPOL - Extract the Codes List

Scrape the [PEPPOL BIS Billing](https://docs.peppol.eu/poacc/billing/3.0/) code list pages and export the code lists as JSON files.

This repository is a small utility project: it contains a single Python script that downloads the public PEPPOL BIS Billing code lists (such as country codes, currency codes, tax categories, invoice type codes, etc.) and turns them into machine‑friendly JSON that you can reuse in your own applications, validators, or integration layers.

## Requirements

- Python 3.8+ (any modern 3.x version should work)
- Network access to the PEPPOL BIS Billing documentation site
- Python dependencies used by the script (check the imports at the top of `scrape_peppol_codelists.py` and install any third‑party libraries with `pip`)

Typical dependencies for a scraper like this are:

```bash
pip install requests beautifulsoup4 lxml
```

but you should always align this with what the script actually imports.

## Installation

Clone the repository:

```bash
git clone https://github.com/Toenn-Vaot/peppol_extract_codes_list.git
cd peppol_extract_codes_list
```

(Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
# On Linux / macOS
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
```

Install the required Python packages with `pip` (as noted above):

```bash
pip install -r requirements.txt  # if you maintain one
# or manually:
pip install requests beautifulsoup4 lxml
```

## Usage

From the root of the repository, run:

```bash
python scrape_peppol_codelists.py
```

The script will:

1. Connect to the official PEPPOL BIS Billing 3.0 documentation site.
2. Follow the links to the various code list pages (e.g. ISO 3166-1 country codes, ISO 4217 currency codes, tax category codes, invoice type codes, etc.).
3. Parse the HTML tables that define each code list.
4. Export the data to one or more JSON files.

The exact output format (file names, directory layout, field names) is defined inside `scrape_peppol_codelists.py`. Common patterns are:

- one JSON file per code list, or
- a single JSON file containing several named lists.

Open the script to see the current behaviour and adjust the README if you change it.

### Example JSON shape (illustrative)

A typical JSON structure for a single code list might look like:

```json
{
  "code_list": "ISO 4217 Currency codes",
  "source": "https://docs.peppol.eu/poacc/billing/3.0/codelist/",
  "codes": [
    { "code": "EUR", "name": "Euro" },
    { "code": "USD", "name": "US Dollar" }
  ]
}
```

This is only an example; adapt it to the actual output produced by the script.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
