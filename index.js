async function analyze() {
            const raw = document.getElementById("pins").value.trim();
            if (!raw) { alert("Please enter at least one PIN."); return; }

            const pins = raw.split("\n").map(p => p.trim()).filter(p => p.length > 0);
            const analyzeTaxes = document.getElementById("analyzeTaxes").checked;
            const incomeApproach = document.getElementById("incomeApproach").checked;

            document.getElementById("loading").style.display = "block";
            document.getElementById("results").innerHTML = "";

            try {
                const response = await fetch("http://127.0.0.1:8000/analyze", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ pins, analyze_current_taxes: analyzeTaxes, income_approach: incomeApproach })
                });

                const data = await response.json();
                document.getElementById("loading").style.display = "none";
                renderResults(data.results);
            } catch (err) {
                document.getElementById("loading").style.display = "none";
                document.getElementById("results").innerHTML = `<p class="error">Failed to connect to backend. Make sure the server is running.</p>`;
            }
        }

        function renderResults(results) {
            const container = document.getElementById("results");
            if (!results.length) { container.innerHTML = "<p>No results.</p>"; return; }

            results.forEach(r => {
                if (r.error) {
                    container.innerHTML += `
                        <div class="result-card">
                            <h3>PIN: ${r.pin}</h3>
                            <p class="error">Error: ${r.error}</p>
                        </div>`;
                    return;
                }

                const taxes = r.estimated_taxes.toLocaleString("en-US", { style: "currency", currency: "USD" });
                const assessment = r.assessment.toLocaleString("en-US", { style: "currency", currency: "USD" });

                container.innerHTML += `
                    <div class="result-card">
                        <h3>PIN: ${r.pin}</h3>
                        <p><strong>Township:</strong> ${r.township}</p>
                        <p><strong>Neighborhood/Tax Code:</strong> ${r.nbhd}</p>
                        <p><strong>Assessment:</strong> ${assessment} (${r.assessment_type}, tax year ${r.tax_year})</p>
                        <p><strong>Tax Rate:</strong> ${r.tax_rate}% (${r.tax_rate_year})</p>
                        <p><strong>Equalization Factor:</strong> ${r.equalization_factor} (2024)</p>
                        <p><strong>Estimated Taxes:</strong> ${taxes}</p>
                        <div class="narrative">
                            The property with PIN ${r.pin} is located in ${r.township} township and is currently 
                            assessed at ${assessment}, which equates to estimated taxes of ${taxes}.
                        </div>
                    </div>`;
            });
        }