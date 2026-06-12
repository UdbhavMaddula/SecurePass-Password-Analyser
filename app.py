import streamlit as st
from zxcvbn import zxcvbn
import re
import random
import pandas as pd

st.set_page_config(
    page_title="SecurePass",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
<style>
    /* Overall page */
    .stApp {
        background-color: #F7F8FA;
    }

    /* Main content width and font */
    .block-container {
        max-width: 700px;
        padding-top: 2.5rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Title */
    h1 {
        font-weight: 700;
        color: #1A1D29;
        letter-spacing: -0.5px;
    }

    /* Subheaders */
    h2, h3 {
        color: #2E323F;
        font-weight: 600;
        margin-top: 1.5rem;
    }

    /* Input fields */
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #E0E3E8;
        padding: 0.6rem 0.9rem;
        background-color: #FFFFFF;
    }

    .stTextInput input:focus {
        border-color: #5B6CFF;
        box-shadow: 0 0 0 1px #5B6CFF;
    }

    /* Checkbox */
    .stCheckbox {
        margin-top: 0.3rem;
    }

    /* Metric */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #ECEEF1;
        border-radius: 12px;
        padding: 1rem 1.2rem;
    }

    [data-testid="stMetricValue"] {
        color: #5B6CFF;
        font-weight: 700;
    }

    /* Progress bar */
    .stProgress > div > div {
        background-color: #5B6CFF;
        border-radius: 8px;
    }

    /* Tables */
    .stTable, table {
        border-radius: 10px;
        overflow: hidden;
    }

    table th {
        background-color: #F0F2F5 !important;
        color: #2E323F !important;
        font-weight: 600 !important;
    }

    /* Alert boxes - soften corners */
    .stAlert {
        border-radius: 10px;
    }

    /* Divider */
    hr {
        border-color: #E5E8EC;
    }

    /* Caption */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #8A8F9C;
    }
</style>
""", unsafe_allow_html=True)

st.image(
    "https://img.icons8.com/fluency/96/lock-2.png",
    width=80
)


st.title("SecurePass")
st.subheader("Password Security Assessment Tool")

st.write(
    "Analyze password strength, understand attack risks, and receive actionable security recommendations."
)

personal_word = st.text_input(
    "Personal Word to Avoid (Optional)",
    placeholder="Example: your name, pet name, username"
)

show_password = st.checkbox("Show Password")

if show_password:
    password = st.text_input("Enter Password")
else:
    password = st.text_input("Enter Password", type="password")

cyber_tips = [
    "Enable Multi-Factor Authentication (MFA) whenever possible.",
    "Never reuse passwords across multiple accounts.",
    "Use a password manager to generate unique passwords.",
    "Avoid using names, birthdays, and phone numbers.",
    "Long passphrases are often stronger than short complex passwords.",
    "Change passwords immediately after a breach."
]

if password:

    user_inputs = []

    if personal_word:
        user_inputs.append(personal_word)

    result = zxcvbn(password, user_inputs=user_inputs)

    z_score = result["score"]

    crack_time = result["crack_times_display"][
        "offline_slow_hashing_1e4_per_second"
    ]

    feedback = result["feedback"]

    checks = {
        "Minimum 8 Characters": len(password) >= 8,
        "Minimum 12 Characters": len(password) >= 12,
        "Uppercase Letter": bool(re.search(r"[A-Z]", password)),
        "Lowercase Letter": bool(re.search(r"[a-z]", password)),
        "Number": bool(re.search(r"\d", password)),
        "Special Character": bool(
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        ),
    }

    base_scores = {
        0: 10,
        1: 25,
        2: 45,
        3: 60,
        4: 70
    }

    security_score = base_scores[z_score]

    bonus = 0

    if checks["Minimum 8 Characters"]:
        bonus += 5

    if checks["Minimum 12 Characters"]:
        bonus += 5

    if checks["Uppercase Letter"]:
        bonus += 5

    if checks["Lowercase Letter"]:
        bonus += 5

    if checks["Number"]:
        bonus += 5

    if checks["Special Character"]:
        bonus += 5

    security_score += bonus

    penalties = 0
    attack_risks = []

    common_patterns = [
        "password",
        "admin",
        "welcome",
        "qwerty",
        "letmein"
    ]

    if any(pattern in password.lower() for pattern in common_patterns):
        penalties += 25
        attack_risks.append("Dictionary Attack")

    if re.search(r"(19|20)\d{2}", password):
        penalties += 15
        attack_risks.append("Social Engineering")

    if re.search(r"(123|234|345|456|567|678|789|012|abcd|qwer)", password.lower()):
        penalties += 20
        attack_risks.append("Sequential Pattern Attack")

    # Penalize "word + simple digits" pattern (e.g. name123, password1)
    word_then_digits = re.match(r"^[a-zA-Z]{3,}\d{1,4}$", password)
    if word_then_digits:
        penalties += 20
        if "Sequential Pattern Attack" not in attack_risks:
            attack_risks.append("Sequential Pattern Attack")

    if password.isdigit():
        penalties += 30
        attack_risks.append("Brute Force Attack")

    if personal_word and personal_word.lower() in password.lower():
        penalties += 35
        attack_risks.append("Personal Information Guessing")

    security_score -= penalties

    # Hard cap: short passwords can't be rated highly, regardless of zxcvbn score
    if len(password) < 10:
        security_score = min(security_score, 50)
    elif len(password) < 12:
        security_score = min(security_score, 65)

    security_score = max(0, min(security_score, 100))

    if security_score <= 39:
        strength = "Weak"
        risk_level = "High"

    elif security_score <= 59:
        strength = "Medium"
        risk_level = "Moderate"

    elif security_score <= 79:
        strength = "Strong"
        risk_level = "Low"

    else:
        strength = "Very Strong"
        risk_level = "Minimal"

    if not attack_risks:
        attack_risks.append("Low Risk")

    recommendations = []

    if len(password) < 12:
        recommendations.append("Use at least 12 characters.")

    if not checks["Special Character"]:
        recommendations.append("Add special characters.")

    if not checks["Uppercase Letter"] or not checks["Lowercase Letter"]:
        recommendations.append("Mix uppercase and lowercase letters.")

    if not checks["Number"]:
        recommendations.append("Add at least one number.")

    if personal_word and personal_word.lower() in password.lower():
        recommendations.append("Avoid using personal information.")

    if feedback["suggestions"]:
        for suggestion in feedback["suggestions"]:
            if suggestion not in recommendations:
                recommendations.append(suggestion)

    if strength in ["Weak", "Medium"]:
        recommendations.append(
            "Enable Multi-Factor Authentication."
        )

    st.header("Password Analysis")

    if strength == "Weak":
        st.error("Weak Password")

    elif strength == "Medium":
        st.warning("Medium Password")

    elif strength == "Strong":
        st.success("Strong Password")

    else:
        st.success(f"{strength} Password")

    st.metric(
        "Security Score",
        f"{security_score}/100"
    )

    st.progress(security_score / 100)

    st.write("Estimated Crack Time:")
    st.info(crack_time)

    st.subheader("Security Report")

    report = pd.DataFrame({
        "Metric": [
            "Password Strength",
            "Security Score",
            "Estimated Crack Time",
            "Attack Risk",
            "Risk Level",
            "MFA Recommendation"
        ],
        "Result": [
            strength,
            f"{security_score}/100",
            crack_time,
            ", ".join(attack_risks),
            risk_level,
            "Recommended"
            if strength != "Very Strong"
            else "Optional"
        ]
    })

    st.table(report)

    st.subheader("Password Checklist")

    checklist = pd.DataFrame({
        "Requirement": list(checks.keys()),
        "Status": [
            "Pass" if value else "Fail"
            for value in checks.values()
        ]
    })

    st.table(checklist)

    st.subheader("Suggestions")

    if recommendations:
        seen = set()
        for recommendation in recommendations:
            if recommendation not in seen:
                seen.add(recommendation)
                st.write(f"• {recommendation}")
    else:
        st.success("Excellent password practices.")

    st.subheader("Attack Awareness")

    st.write(
        f"Potential Attacks: {', '.join(attack_risks)}"
    )

    st.write(
        "Avoid predictable information and use unique passwords."
    )

    st.subheader("Security Best Practice")

    st.info(
        random.choice(cyber_tips)
    )

else:
    st.info(
        "Enter a password to begin analysis."
    )

st.divider()

st.caption(
    "Developed by Udbhav | SecurePass Password Security Assessment Tool"
)

st.link_button(
    "View Source Code",
    "https://github.com/UdbhavMaddula/SecurePass-Password-Analyser"
)

st.caption(
    "Passwords entered are analyzed locally and are not stored."
)
