# Age Ratio App (Streamlit)

Estimate **Biological Age** and **Financial Age**, then compare them to your chronological age.
This app is for education only — not medical or financial advice.

## Overview

- **Biological Age** adjusts chronological age using BMI, resting heart rate (RHR), activity level, and optional health conditions.
- **Financial Age** infers an age from your **net-worth-to-income multiple** using a widely cited rule-of-thumb glidepath.


> -------- requires review --------  
> The `AGE_TO_INCOME_MULTIPLE` mapping in `algorithms.py` is a placeholder glidepath based on public rules of thumb (e.g., 1× income by 30, 2× by 35, 3× by 40, etc.).  
> You **must** validate/replace these with current, jurisdiction-appropriate benchmarks before production.

## Quickstart (Local)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a new **GitHub repository** (e.g., `age-ratio-app`).
2. Upload these files at the repo root:
   - `app.py`
   - `algorithms.py`
   - `requirements.txt`
   - `data/health_conditions.csv`
   - `README.md`
3. Go to Streamlit Community Cloud, select your repo and deploy.

## Project Structure

```
.
├── app.py
├── algorithms.py
├── requirements.txt
├── data
│   └── health_conditions.csv
└── README.md
```

## Methodology (Heuristic)

**Biological Age**
- BMI penalty vs. ideal ~22.
- RHR adjustment (lower is generally better to a point).
- Activity multiplier (athlete → largest downward adjustment).
- Health condition penalties (CSV-driven; customizable).

**Financial Age**
- Net worth = Liquid + Illiquid − Liabilities.
- Net-worth-to-income multiple compared to a glidepath:
  `(25,0.5), (30,1), (35,2), (40,3), (45,4), (50,6), (55,7), (60,8), (67,10)` → interpolated to an implied age.
- Renting adds +1 year to implied financial age (modest headwind).


## LLM Advice (Optional)

The app includes a **rule-based** guidance block. To upgrade with an LLM:
- Add your provider SDK and call it with the computed components (bio/fin).
- Provide **guardrails**: never give medical or individualized investment advice; keep it general.

Example sketch (pseudocode):

```python
# -------- requires review --------
from your_llm_sdk import Client

client = Client(api_key=...)

prompt = f"""User metrics:
- Bio age: {bio_age} (BMI {bmi}, RHR {rhr}, activity {activity}, conditions {conditions})
- Fin age: {fin_age} (NW {net_worth}, multiple {nw_multiple}, housing {housing})

Offer general, non-medical, non-financial-advice suggestions to narrow the gap.
"""

resp = client.generate(prompt)
st.write(resp.text)
```

# Age Ratio Lab

Run locally:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

Semantics: financial_age higher = good; biological_age lower = good.
Primary metric: financial_age - biological_age  ( > 1 => good ).

Replace AGE_TO_INCOME_MULTIPLE in algorithms.py with validated benchmarks before production.


## Disclaimers

- **Not medical/financial advice.** Educational heuristics only.
- Health and finance are context-dependent. Consult qualified professionals.
- Validate data sources before decision-making.

## License

MIT
