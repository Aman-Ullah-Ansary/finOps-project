import streamlit as st

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI Cloud FinOps Platform",
    page_icon="☁️",
    layout="wide",
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>

.main-title{
    font-size:52px;
    font-weight:800;
    color:#2563eb;
}

.subtitle{
    font-size:22px;
    color:#555;
}

.feature-card{
    background:#ffffff;
    padding:20px;
    border-radius:15px;
    border:1px solid #e5e7eb;
    margin-bottom:15px;
    color:#111827;
}

.feature-card h3{
    color:#111827;
    margin-bottom:10px;
}

.feature-card p{
    color:#4b5563;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Logo
# ----------------------------
st.image("assets/images/logo.png", width=170)

# ----------------------------
# Hero
# ----------------------------
st.markdown(
    '<p class="main-title">☁️ AI Cloud FinOps Platform</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Intelligent AWS Cost Monitoring, Forecasting and Optimization Platform</p>',
    unsafe_allow_html=True
)

st.divider()

# ----------------------------
# About
# ----------------------------
st.header("🚀 Platform Overview")

st.write("""
This platform helps organizations monitor and optimize AWS cloud costs using AI-powered analytics.

It combines forecasting, anomaly detection, intelligent recommendations, and cost optimization into a single dashboard.
""")

st.divider()

# ----------------------------
# KPI Cards
# ----------------------------
st.header("📌 Platform Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Modules", "5")
c2.metric("Cloud", "AWS")
c3.metric("AI Features", "3")
c4.metric("Version", "1.0")

st.divider()

# ----------------------------
# Features
# ----------------------------
st.header("✨ Features")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
<div class="feature-card">
<h3>📊 Dashboard</h3>
<p>Interactive AWS Cost Dashboard</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-card">
<h3>📈 Forecasting</h3>
<p>Predict future cloud costs using machine learning.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-card">
<h3>🚨 Anomaly Detection</h3>
<p>Identify unusual AWS spending spikes instantly.</p>
</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown("""
<div class="feature-card">
<h3>🤖 AI Recommendations</h3>
<p>Receive intelligent cost optimization suggestions.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-card">
<h3>💰 Cost Optimization</h3>
<p>Estimate monthly savings and reduce cloud waste.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-card">
<h3>📄 Reports</h3>
<p>Export PDF and Excel reports. (Coming Soon)</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ----------------------------
# Technology Stack
# ----------------------------
st.header("🛠 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.success("Python")
    st.success("Streamlit")
    st.success("Pandas")

with tech2:
    st.success("Plotly")
    st.success("Scikit-Learn")
    st.success("NumPy")

with tech3:
    st.success("AWS")
    st.success("FinOps")
    st.success("Machine Learning")

st.divider()

# ----------------------------
# Navigation
# ----------------------------
st.info(
"""
👈 Use the left sidebar to access:

• Dashboard

• Forecasting

• Anomaly Detection

• AI Recommendations

• Cost Optimization
"""
)

st.divider()

# ----------------------------
# Footer
# ----------------------------
st.markdown(
"""
<div class="footer">

© 2026 AI Cloud FinOps Platform

Built with ❤️ using Streamlit

</div>
""",
unsafe_allow_html=True
)