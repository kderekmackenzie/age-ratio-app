import numpy as np

# ------------------------------------------------------------
# Biological Age Estimation
# ------------------------------------------------------------

def estimate_biological_age(
    chronological_age: float,
    height_cm: float,
    weight_kg: float,
    resting_hr: float,
    activity_level: str,
    conditions: list
) -> float:
    """
    Estimate biological age using simple physiologic predictors.
    Lower is better.
    """

    bio_age = float(chronological_age)

    # BMI effect (U-shaped penalty)
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    # Ideal BMI around 22–24
    if bmi < 18.5:
        bio_age += 2
    elif bmi < 25:
        bio_age -= 2
    elif bmi < 30:
        bio_age += 2
    else:
        bio_age += 5

    # Resting heart rate (RHR)
    if resting_hr < 60:
        bio_age -= 3
    elif resting_hr <= 75:
        bio_age += 0
    else:
        bio_age += 4

    # Activity level
    level = activity_level.lower().strip()
    if level == "athlete":
        bio_age -= 5
    elif level == "moderately active":
        bio_age -= 2
    elif level == "mildly active":
        bio_age -= 1
    elif level == "sedentary":
        bio_age += 3

    # Health conditions penalty
    # User can expand this list or weight differently later.
    condition_penalty = {
        "hypertension": 3,
        "diabetes": 4,
        "smoker": 5,
        "obesity": 4,
        "heart-disease": 6,
    }

    for c in conditions:
        c_norm = c.lower().strip()
        if c_norm in condition_penalty:
            bio_age += condition_penalty[c_norm]

    # Bounds
    return float(np.clip(bio_age, 18, 100))


# ------------------------------------------------------------
# Financial Age Estimation (Updated Logic)
# ------------------------------------------------------------

def estimate_financial_age(net_worth: float, housing_status: str) -> float:
    """
    Estimate financial age by interpolating against a realistic median net-worth curve.
    Higher financial age = higher wealth maturity = good.

    Renting increases financial age slightly (penalty),
    home ownership decreases it slightly (boost).
    """

    # Median net worth by age (US + Canada blended reference curve)
    age_points = np.array([25, 30, 35, 40, 45, 50, 55, 60, 65, 70], dtype=float)
    networth_points = np.array([
        20000,     # age 25
        60000,     # age 30
        120000,    # age 35
        200000,    # age 40
        300000,    # age 45
        450000,    # age 50
        650000,    # age 55
        850000,    # age 60
        1000000,   # age 65
        1100000    # age 70
    ], dtype=float)

    nw = float(net_worth)

    # Clamp net worth to realistic boundaries of the curve
    nw_clamped = np.clip(nw, networth_points.min(), networth_points.max())

    # Linear interpolation: net worth → implied financial age
    financial_age = np.interp(nw_clamped, networth_points, age_points)

    # Housing adjustment (small, realistic)
    hs = housing_status.lower().strip()
    if hs == "own":
        financial_age -= 3       # homeownership boosts financial maturity
    else:
        financial_age += 3       # renting delays typical wealth accumulation

    # Reasonable output bounds
    return float(np.clip(financial_age, 18, 95))


# ------------------------------------------------------------
# Combined Ratio
# ------------------------------------------------------------

def compute_age_ratio(bio_age: float, financial_age: float) -> float:
    """
    Ratio where >1 is good.
    Higher financial age is desirable; lower biological age is desirable.
    """
    if bio_age <= 0:
        return 0.0
    return float(financial_age / bio_age)
