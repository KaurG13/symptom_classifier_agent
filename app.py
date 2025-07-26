import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import streamlit as st

# 🔐 Directly set the API key
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]  # Replace with your real API key

# Model setup
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0.2)

# Classification logic
def classify_symptom(symptom: str) -> str:
    prompt = (
        "You are a helpful Medical Assistant. Classify the symptom below into one category:\n"
        "- General\n- Emergency\n- Mental Health\n\n"
        f"Symptom: {symptom}\n"
        "Respond only with one word: General, Emergency or Mental Health.\n"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

# Routing logic
def route_to_ward(category: str, symptom: str) -> str:
    if "general" in category.lower():
        return f"🩺 '{symptom}' seems general. Redirecting you to the General Ward."
    elif "emergency" in category.lower():
        return f"🚨 '{symptom}' is a medical emergency. Seek immediate help!"
    elif "mental" in category.lower():
        return f"🧠 '{symptom}' seems like a mental health issue. Connecting you with a counsellor."
    else:
        return f"⚠️ Could not classify symptom properly. Please try again."

# Streamlit UI
st.set_page_config(page_title="Symptom Classifier", page_icon="💊", layout="centered")
st.title("🩻 Medical Symptom Classifier")
st.markdown("Enter your symptom and we'll direct you to the correct ward.")

with st.form("symptom_form"):
    symptom = st.text_area("🔍 Enter your symptom:", height=100)
    submitted = st.form_submit_button("Classify")

if submitted and symptom:
    with st.spinner("Analyzing your symptom..."):
        category = classify_symptom(symptom)
        result = route_to_ward(category, symptom)
        st.success(f"🧾 Classification Result: {category}")
        st.info(result)
