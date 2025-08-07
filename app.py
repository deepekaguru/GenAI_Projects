import streamlit as st
from prompts import generate_drug_info
import re

# ----------------------------
# Section Splitter
# ----------------------------
def extract_sections(markdown_text):
    sections = {"use": "", "side": "", "precautions": "", "summary": ""}
    matches = re.split(r"\*\*(.*?)\*\*", markdown_text)
    for i in range(1, len(matches), 2):
        title = matches[i].lower()
        content = matches[i + 1].strip()
        if "what is it used for" in title:
            sections["use"] = content
        elif "common side effects" in title:
            sections["side"] = content
        elif "precautions" in title:
            sections["precautions"] = content
        elif "summary" in title:
            sections["summary"] = content
    return sections

# ----------------------------
# UI Config and Styling
# ----------------------------
st.set_page_config(page_title="DrugInfoGen – AI Medical Assistant", page_icon="💊", layout="centered")

st.markdown("""
    <style>
        .title {text-align: center; font-size: 42px; font-weight: bold;}
        .subtitle {text-align: center; font-size: 20px; color: #555;}
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 1.5em;
        }
        .stRadio > div {
            display: flex;
            gap: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Title and Mode
# ----------------------------
st.markdown("<div class='title'>💊 DrugInfoGen – Know Your Medicine</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Use this assistant to get medication info by drug or condition.</div>", unsafe_allow_html=True)

mode = st.radio("Select Search Mode:", ["Search by Drug", "Search by Condition"])

# ----------------------------
# Mode 1: Drug Search (typed input)
# ----------------------------
if mode == "Search by Drug":
    drug_name = st.text_input("Enter a drug name (e.g., ibuprofen):")
    if st.button("🔍 Generate Drug Info") and drug_name:
        with st.spinner("Getting drug details..."):
            raw_response = generate_drug_info(drug_name)
            sections = extract_sections(raw_response)

        st.markdown("## 📋 Drug Information")

        if sections["use"]:
            with st.expander("💊 What is it used for?", expanded=True):
                st.markdown(sections["use"])

        if sections["side"]:
            with st.expander("⚠️ Common Side Effects", expanded=False):
                st.markdown(sections["side"])

        if sections["precautions"]:
            with st.expander("🛑 Precautions", expanded=False):
                st.markdown(sections["precautions"])

        if sections["summary"]:
            with st.expander("🧾 Drug Summary", expanded=False):
                st.markdown(sections["summary"])

        st.markdown("### 🔗 References")
        slug = drug_name.replace(" ", "-").lower()
        st.markdown(f"- [Drugs.com](https://www.drugs.com/{slug}.html)")
        st.markdown(f"- [WebMD](https://www.webmd.com/drugs/2/search?query={slug})")

# ----------------------------
# Mode 2: Condition Search (dropdown)
# ----------------------------
# ----------------------------
# Mode 2: Condition Search (dropdown)
# ----------------------------
elif mode == "Search by Condition":
    common_conditions = [
    "fever",
    "headache",
    "cold and cough",
    "allergies",
    "heartburn",
    "indigestion",
    "nausea",
    "constipation",
    "diarrhea",
    "muscle pain",
    "back pain",
    "acne",
    "dry skin",
    "sore throat",
    "motion sickness"
    ]
    condition = st.selectbox("Select your medical condition:", common_conditions)

    if st.button("🔍 Find Related Drugs"):
        with st.spinner("Finding medications..."):
            prompt = (
                f"You are a helpful medical assistant. List 5 commonly prescribed drugs to treat {condition}. "
                "Only return the drug names in bullet points, one per line, starting with a dash (-)."
            )
            condition_response = generate_drug_info(condition, mode="condition")


        drug_names = [
            re.sub(r"^[\-\•\d\.\)]+", "", line).strip()
            for line in condition_response.split("\n")
            if re.match(r"^\s*[\-\•\d\.\)]", line)
        ]

        st.markdown("## 💊 Suggested Medications")
        if drug_names:
            for drug in drug_names:
                st.markdown(f"- {drug}")
        else:
            st.warning("No valid drug names found in the response.")

# ----------------------------
# Disclaimer
# ----------------------------
st.markdown("---")
st.markdown("🔒 _Disclaimer: This tool is for informational purposes only. Always consult a healthcare professional._")
