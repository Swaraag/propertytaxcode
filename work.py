import pdfplumber
import requests

PDF_PATH = "taxcodeRatesYearly.pdf"
EQUALIZATION_F = 3.0355 #https://tax.illinois.gov/research/news/2024-cook-county-final-multiplier.html
ASSESSOR_API = "https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json"

def get_assessment(pin):
    clean_pin = pin.replace("-", "")
    response = requests.get(ASSESSOR_API, params={"pin": clean_pin})
    data = response.json()

    if not data:
        return None, "No data found for this PIN"
    
    data = [record for record in data if record.get("mailed_tot") or record.get("certified_tot") or record.get("board_tot")]
    most_recent = max(data, key=lambda x: int(x["year"]))

    if most_recent.get("board_tot"):
        assessment = float(most_recent["board_tot"])
        assessment_type = "board"
    elif most_recent.get("certified_tot"):
        assessment = float(most_recent["certified_tot"])
        assessment_type = "certified"
    else:
        assessment = float(most_recent["mailed_tot"])
        assessment_type = "mailed"

    return {
        "pin": clean_pin,
        "tax_year": most_recent["year"],
        "township": most_recent.get("township_name"),
        "nbhd": most_recent.get("nbhd"),
        "assessment": assessment,
        "assessment_type": assessment_type
    }, None

def get_tax_rate(tax_code):
    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text or tax_code not in text:
                continue
            lines = text.split("\n")
            year_headers = None
            for line in lines:
                parts = line.strip().split()
                years_in_line = [int(p) for p in parts if p.isdigit() and len(p) == 4]
                if len(years_in_line) >= 3:
                    year_headers = years_in_line
                    break
            if not year_headers:
                continue
            for line in lines:
                parts = line.strip().split()
                if parts and parts[0] == tax_code:
                    rates = parts[1:]
                    if not rates:
                        return None
                    paired = list(zip(year_headers[-len(rates):], rates))
                    rate_map = {year: float(rate) for year, rate in paired}
                    most_recent_year = max(rate_map.keys())
                    return {
                        "rate": rate_map[most_recent_year],
                        "year": most_recent_year
                    }
    return None

def calculate_taxes(assessment, tax_rate):
    if assessment is not None and tax_rate is not None:
        return round((tax_rate / 100) * EQUALIZATION_F * assessment, 2)
    else:
        return -1