import streamlit as st
import numpy as np
from algorithms import (
    estimate_biological_age,
    estimate_financial_age,
    compute_age_ratio,
)


# ------------------------------------------------------------
# Helper: Arrow rendering
# ------------------------------------------------------------
def render_arrow(delta: float, is_bio: bool = False):
    """
    Biological age: lower is better → green for negative delta.
    Financial age: higher is better → green for positive delta.
    """

    if is_bio:
        # Bio age: negative delta is good
        if delta < 0:
            return "↓", "green"
        elif delta > 0:
            return "↑", "red"
        else:
            return "→", "gray"
    else:
        # Financial age: positive delta is good
        if delta > 0:
            return "↑", "green"
        elif delta < 0:
            return "↓", "red"
        else:
            return "→", "gray"


# ------------------------------------------------------------
# Helper: Interpretation logic (quadrant-based)
# ------------------------------------------------------------
def interpret_results(chron_age, bio_age, fin_age):
    interpretations = []

    # ---- Biological Age vs Chronological Age ----
    if bio_age < chron_age - 3:
        interpretations.append(
            "Your biological age is significantly below your chronological age. "
            "This typically reflects strong cardiovascular fitness, favorable biomarkers, "
            "and generally robust metabolic health."
        )
    elif chron_age - 3 <= bio_age <= chron_age + 3:
        interpretations.append(
            "Your biological age aligns closely with your chronological age — generally balanced health. "
            "With targeted adjustments, you can push biological age lower."
        )
    else:
        interpretations.append(
            "Your biological age is above your chronological age. "
            "This commonly reflects elevated baseline stress markers, higher resting heart rate, "
            "lower activity levels, or lifestyle friction. There is opportunity to improve here."
        )

    # ---- Financial Age vs Biological Age ----
    if fin_age > bio_age + 5:
        interpretations.append(
            "Your financial age is substantially higher than your biological age. "
            "This is a very strong position: you are accumulating wealth faster than most people at your health-adjusted life stage."
        )
    elif bio_age - 5 <= fin_age <= bio_age + 5:
        interpretations.append(
            "Your financial age is roughly aligned with your biological age. "
            "This is stable, but improving savings rate or asset growth could move you above the curve."
        )
    else:
        interpretations.append(
            "Your financial age is below your biological age. "
            "This suggests under-accumulation relative to your health-adjusted stage of life. "
            "Increasing savings rate, reducing liabilities, or optimizing investment mix may help."
        )

    return "\n\n".join(interpretations)


# ------------------------------------------------------------
# Streamlit Page Layout
# ------------------------------------------------------------
st.set_page_config(page_title="Age Ratio App", layout="centered")

st.title("Biological & Financial Age Calculator")
st.write("Higher financial age = good. Lower biological age = good. The ratio tells you where you stand.")


# ------------------------------------------------------------
# Sidebar Inputs
# ------------------------------------------------------------
st.header("Inputs")

chron_age = st.number_input("Chronological Age", 18, 100, 40)

st.subheader("Biological Inputs")
height = st.number_input("Height (cm)", 120, 220, 175)
weight = st.number_input("Weight (kg)", 40, 200, 75)
resting_hr = st.number_input("Resting Heart Rate (BPM)", 40, 120, 65)

activity_level = st.selectbox(
    "Activity Level",
    ["Sedentary", "Mildly Active", "Moderately Active", "Athlete"],
)

conditions = st.multiselect(
    "Health Conditions",
    ["Hypertension", "Diabetes", "Smoker", "Obesity", "Heart-Disease", "Anxiety-Depression"],
)

st.subheader("Financial Inputs")
income = st.number_input("Annual Income", min_value=0, value=75000)
liquid_assets = st.number_input("Liquid Assets", min_value=0, value=20000)
illiquid_assets = st.number_input("Illiquid Assets", min_value=0, value=130000)
liabilities = st.number_input("Liabilities", min_value=0, value=0)
housing_status = st.selectbox("Housing Status", ["Rent", "Own"])

net_worth = liquid_assets + illiquid_assets - liabilities


# ------------------------------------------------------------
# Compute
# ------------------------------------------------------------
bio_age = estimate_biological_age(
    chron_age,
    height,
    weight,
    resting_hr,
    activity_level,
    conditions,
)

fin_age = estimate_financial_age(
    net_worth=net_worth,
    housing_status=housing_status,
)

ratio = compute_age_ratio(bio_age, fin_age)


# ------------------------------------------------------------
# Display Metrics
# ------------------------------------------------------------
st.header("Results")

# Biological age delta
bio_delta = bio_age - chron_age
bio_arrow, bio_color = render_arrow(bio_delta, is_bio=True)

# Financial age delta (vs bio age)
fin_delta = fin_age - bio_age
fin_arrow, fin_color = render_arrow(fin_delta, is_bio=False)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Biological Age",
        value=f"{bio_age:.1f}",
        delta=f"{bio_delta:+.1f} vs chronological",
        delta_color="inverse" if bio_delta < 0 else "normal"
    )

with col2:
    st.metric(
        label="Financial Age",
        value=f"{fin_age:.1f}",
        delta=f"{fin_delta:+.1f} vs biological",
        delta_color="normal" if fin_delta > 0 else "inverse"
    )

with col3:
    st.metric("Financial / Biological Ratio", f"{ratio:.2f}")


# ------------------------------------------------------------
# Interpretation Section
# ------------------------------------------------------------
st.header("Interpretation")
st.write(interpret_results(chron_age, bio_age, fin_age))
