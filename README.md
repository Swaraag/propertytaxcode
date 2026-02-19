# Cook County Property Tax Estimator

A prototype tool that estimates Cook County property taxes from a PIN. Built as a demo for Sarnoff Property Tax.

## What it does

- Accepts one or more Cook County 14-digit PINs (with or without dashes)
- Pulls assessment data from the Cook County Assessor's public API
- Selects the most recent assessment using the hierarchy: **Board of Review -> Certified -> Mailed**
- Looks up the most recent available tax rate from the Cook County Clerk's Tax Code Rate Summary PDF
- Calculates estimated taxes as: `(tax rate / 100) x equalization factor x assessment`
- Displays a formatted result card per PIN including the required narrative line

## Requirements

- Python 3.8+ (built in Python 3.14.2)
- The Cook County Clerk Tax Code Rate Summary PDF (see below)

## Setup

**1. Clone the repo**
```bash
git clone <your-repo-url>
cd <repo-folder>
```

**2. Install dependencies**
```bash
pip install fastapi uvicorn pdfplumber requests
```

**3. Download the Tax Rate PDF**

Download the Cook County Clerk Tax Code Rate Summary (10-year report) from:
https://www.cookcountyclerkil.gov/property-taxes/tax-extension-and-rates

Save it in the project root as `taxcodeRatesYearly.pdf`

**4. Start the backend**
```bash
uvicorn main:app --reload
```

**5. Open the frontend**

Open `index.html` directly in your browser. No additional server needed.

## Usage

- Enter one or more PINs in the text area, one per line
- PINs can be entered with or without dashes (e.g. `17-10-205-001-0000` or `17102050010000`)
- Check/uncheck the toggles as needed
- Click **Generate Report**

## Data Sources

| Data | Source |
|------|--------|
| Assessment values | [Cook County Assessor Open Data API](https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json) |
| Tax rates | Cook County Clerk Tax Code Rate Summary PDF (through 2023) |
| Equalization factor | Illinois Dept. of Revenue — 2024 final factor: **3.0355** |

## Notes on the prototype

- **PDF parsing** works for the happy path but would be made significantly more robust in production (handling merged cells, multi-page edge cases, missing tax codes)
- **Tax rates** only go through 2023 in the current PDF — the tool uses the most recent available year and displays which year was used
- **Income Approach Analysis** toggle is present in the UI but requires user-provided income/expense data — placeholder for full implementation
- The equalization factor is currently hardcoded to the 2024 final value (3.0355) and would be fetched dynamically in production