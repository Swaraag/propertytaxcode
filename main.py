from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from work import get_assessment, get_tax_rate, calculate_taxes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
def analyze(body: dict):
    pins = body.get("pins", [])
    results = []

    for pin in pins:
        assessment, error = get_assessment(pin)
        if error:
            results.append({"pin": pin, "error": error})
            continue

        rate_info = get_tax_rate(assessment["nbhd"])
        if not rate_info:
            results.append({"pin": pin, "error": f"No tax rate found for neighborhood {assessment['nbhd']}"})
            continue

        taxes = calculate_taxes(assessment["assessment"], rate_info["rate"])

        results.append({
            "pin": pin,
            "township": assessment["township"],
            "nbhd": assessment["nbhd"],
            "assessment": assessment["assessment"],
            "assessment_type": assessment["assessment_type"],
            "tax_year": assessment["tax_year"],
            "tax_rate": rate_info["rate"],
            "tax_rate_year": rate_info["year"],
            "equalization_factor": 3.0355,
            "estimated_taxes": taxes
        })

    return {"results": results}
