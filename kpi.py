import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import os
from together import Together

# -------------------- CONFIGURATION --------------------
api_key = "0e4bf9de4a44967c7b8704363b972acff4bf52047782c0411e27d7ade8333c52"
model_name = "meta-llama/Llama-3-70b-chat-hf"  # Adjust model name from Together's supported list

client = Together(api_key=api_key)
st.set_page_config(page_title="Executive KPI AI Dashboard", layout="wide")

# -------------------- STREAMLIT UI --------------------
st.title("📊 AI Executive Dashboard - Forecasting and Intelligence")
st.markdown("AI-powered insights and trend forecasting for strategic decision-making.")

uploaded_file = st.file_uploader("Upload KPI Data (Excel or CSV)", type=["csv", "xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    # Read file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(tmp_path)
        else:
            df = pd.read_excel(tmp_path)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.success("✅ Data Loaded Successfully")
    st.subheader("Raw KPI Data")
    st.dataframe(df, use_container_width=True)

    # -------------------- DATA VISUALIZATION --------------------
    st.subheader("📈 KPI Visualizations")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if numeric_cols:
        for col in numeric_cols:
            fig, ax = plt.subplots()
            sns.lineplot(data=df, x=df.index, y=col, ax=ax)
            ax.set_title(f"Trend of {col}")
            st.pyplot(fig)
    else:
        st.warning("No numeric columns found to visualize.")

    # -------------------- AI-GENERATED REPORT --------------------
    st.subheader("🧠 Executive AI Report")

    system_prompt = (
        "You are a business intelligence analyst. Based on the uploaded KPI data, "
        "analyze trends, forecast potential business outcomes, detect anomalies, and suggest "
        "strategic recommendations. Be detailed and break your response into sections like Trends, Forecasts, Anomalies, and Recommendations."
    )

    try:
        summary_input = f"Here is the KPI data:\n{df.head(50).to_string()}"

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": summary_input}
            ]
        )

        ai_report = response.choices[0].message.content
        st.markdown("#### AI-Generated Detailed Report")
        st.markdown(ai_report)

    except Exception as e:
        st.error(f"Error generating AI report: {e}")

else:
    st.info("Please upload a KPI dataset to generate the dashboard and AI report.")
