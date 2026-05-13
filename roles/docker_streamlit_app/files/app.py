import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Dashboard", layout="wide")

st.title("📊 Student Performance Dashboard")

# =========================================
# Default Dataset (Preloaded)
# =========================================
@st.cache_data
def load_default_data():
    np.random.seed(42)
    data = {
        "Student_ID": range(1, 101),
        "Hours_Studied": np.random.randint(1, 10, 100),
        "Sleep_Hours": np.random.randint(4, 9, 100),
    }
    df = pd.DataFrame(data)
    df["Marks"] = (
        df["Hours_Studied"] * 10
        + df["Sleep_Hours"] * 5
        + np.random.randint(-10, 10, 100)
    )
    return df

default_df = load_default_data()

# =========================================
# Sidebar Options
# =========================================
st.sidebar.header("Options")

data_source = st.sidebar.radio(
    "Choose Data Source",
    ["Use Default Dataset", "Upload Your CSV"]
)

# =========================================
# Data Selection
# =========================================
if data_source == "Upload Your CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("No file uploaded. Using default dataset.")
        df = default_df.copy()
else:
    df = default_df.copy()

# =========================================
# Show Original Data
# =========================================
st.subheader("📄 Original Dataset")
st.dataframe(df)

# =========================================
# KPIs (Analyzed Data)
# =========================================
st.subheader("📌 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Average Marks", round(df["Marks"].mean(), 2))
col2.metric("Max Marks", df["Marks"].max())
col3.metric("Avg Study Hours", round(df["Hours_Studied"].mean(), 2))

# =========================================
# Filters
# =========================================
st.sidebar.header("Filters")

hours_range = st.sidebar.slider(
    "Hours Studied",
    int(df["Hours_Studied"].min()),
    int(df["Hours_Studied"].max()),
    (int(df["Hours_Studied"].min()), int(df["Hours_Studied"].max()))
)

filtered_df = df[
    (df["Hours_Studied"] >= hours_range[0]) &
    (df["Hours_Studied"] <= hours_range[1])
]

# =========================================
# Analysis Section
# =========================================
st.subheader("📊 Data Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("### Study Hours vs Marks")
    fig1, ax1 = plt.subplots()
    ax1.scatter(filtered_df["Hours_Studied"], filtered_df["Marks"])
    ax1.set_xlabel("Hours Studied")
    ax1.set_ylabel("Marks")
    st.pyplot(fig1)

with col2:
    st.write("### Sleep Hours vs Marks")
    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_df["Sleep_Hours"], filtered_df["Marks"])
    ax2.set_xlabel("Sleep Hours")
    ax2.set_ylabel("Marks")
    st.pyplot(fig2)

# =========================================
# Distribution Analysis
# =========================================
st.subheader("📈 Distribution")

col3, col4 = st.columns(2)

with col3:
    st.write("### Marks Distribution")
    fig3, ax3 = plt.subplots()
    ax3.hist(filtered_df["Marks"], bins=10)
    ax3.set_xlabel("Marks")
    st.pyplot(fig3)

with col4:
    st.write("### Study Hours Distribution")
    fig4, ax4 = plt.subplots()
    ax4.hist(filtered_df["Hours_Studied"], bins=10)
    ax4.set_xlabel("Hours Studied")
    st.pyplot(fig4)

# =========================================
# Correlation
# =========================================
st.subheader("🔗 Correlation Matrix")

corr = filtered_df.corr(numeric_only=True)

fig5, ax5 = plt.subplots()
cax = ax5.matshow(corr)
plt.colorbar(cax)

ax5.set_xticks(range(len(corr.columns)))
ax5.set_yticks(range(len(corr.columns)))
ax5.set_xticklabels(corr.columns, rotation=45)
ax5.set_yticklabels(corr.columns)

st.pyplot(fig5)

# =========================================
# Download
# =========================================
st.subheader("⬇️ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

st.success("Dashboard Ready 🚀")

